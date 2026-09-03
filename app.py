import asyncio
import os
import tempfile
import urllib.parse
import urllib.request
from urllib.parse import urlparse

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, Response, StreamingResponse
from pydantic import BaseModel
import yt_dlp

app = FastAPI()
tasks_progress = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIE_PATH = os.path.join(BASE_DIR, 'cookies.txt')


class InfoRequest(BaseModel):
  url: str


class DownloadRequest(BaseModel):
  url: str
  resolution: str
  task_id: str


def remove_file(path: str):
  if os.path.exists(path):
    os.remove(path)


def get_ydl_options(url: str, custom_opts=None):
  opts = {
      'quiet': True,
      'no_warnings': True,
      'http_headers': {
          'User-Agent': (
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
              ' (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
          )
      },
  }

  if 'youtube.com' in url or 'youtu.be' in url:
    if os.path.exists(COOKIE_PATH):
      opts['cookiefile'] = COOKIE_PATH

  if custom_opts:
    opts.update(custom_opts)

  return opts


@app.post('/api/info')
def get_video_info(data: InfoRequest):
  url = data.url.strip()
  if not (url.startswith('http://') or url.startswith('https://')):
    raise HTTPException(
        status_code=400, detail='URL inválida. Cole um link completo.'
    )

  try:
    ydl_opts = get_ydl_options(url)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(url, download=False)

    if not info:
      raise HTTPException(
          status_code=400, detail='Não foi possível obter informações do vídeo.'
      )

    video_id = info.get('id', '')
    resolutions = set()

    formats = info.get('formats') or []
    for f in formats:
      if isinstance(f, dict):
        height = f.get('height')
        vcodec = f.get('vcodec')
        if height and vcodec != 'none':
          resolutions.add(height)

    embed_url = None
    if 'youtube.com' in url or 'youtu.be' in url:
      embed_url = (
          f'https://www.youtube-nocookie.com/embed/{video_id}?autoplay=0'
      )
    elif 'tokyvideo.com' in url:
      parsed = urlparse(url)
      path = parsed.path.replace('/br/video/', '/video/')
      if path.startswith('/video/'):
        slug = path.replace('/video/', '')
        embed_url = f'https://www.tokyvideo.com/embed/{slug}'
      else:
        embed_url = f'https://www.tokyvideo.com/embed/{video_id}'

    direct_url = None
    for f in reversed(formats):
      if isinstance(f, dict):
        if (
            f.get('vcodec') != 'none'
            and f.get('acodec') != 'none'
            and f.get('url')
        ):
          direct_url = f.get('url')
          break

    if not direct_url and formats:
      last_format = formats[-1]
      if isinstance(last_format, dict):
        direct_url = last_format.get('url')

    proxy_stream_url = (
        f'/api/stream?url={urllib.parse.quote(direct_url)}'
        if direct_url
        else None
    )

    return {
        'title': info.get('title', 'Vídeo sem título'),
        'thumbnail': info.get('thumbnail'),
        'embed_url': embed_url,
        'direct_url': proxy_stream_url or direct_url,
        'resolutions': sorted(list(resolutions), reverse=True),
    }
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))


@app.get('/api/stream')
def stream_video(url: str):
  try:
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                ' (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            )
        },
    )
    response = urllib.request.urlopen(req, timeout=20)

    def iter_stream():
      while True:
        chunk = response.read(1024 * 512)
        if not chunk:
          break
        yield chunk

    headers = {
        'Content-Type': response.headers.get('Content-Type', 'video/mp4'),
        'Accept-Ranges': 'bytes',
    }
    return StreamingResponse(iter_stream(), headers=headers)
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


@app.get('/api/progress/{task_id}')
async def progress_stream(task_id: str):

  async def event_generator():
    while True:
      prog = tasks_progress.get(task_id, {'status': 'waiting', 'percent': 0})
      yield f"data: {prog.get('percent', 0)}|{prog.get('status', '')}\n\n"
      if prog.get('status') in ['finished', 'error']:
        tasks_progress.pop(task_id, None)
        break
      await asyncio.sleep(0.4)

  return StreamingResponse(event_generator(), media_type='text/event-stream')


@app.post('/api/download')
def download_video(data: DownloadRequest, background_tasks: BackgroundTasks):
  task_id = data.task_id
  tasks_progress[task_id] = {'status': 'downloading', 'percent': 0}

  def progress_hook(d):
    if d['status'] == 'downloading':
      total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
      downloaded = d.get('downloaded_bytes', 0)
      if total > 0:
        percent = int((downloaded / total) * 100)
        tasks_progress[task_id] = {'status': 'downloading', 'percent': percent}
    elif d['status'] == 'finished':
      tasks_progress[task_id] = {'status': 'converting', 'percent': 100}

  try:
    temp_dir = tempfile.mkdtemp()
    output_template = os.path.join(temp_dir, '%(title)s.%(ext)s')

    custom_opts = {
        'outtmpl': output_template,
        'progress_hooks': [progress_hook],
    }

    if data.resolution == 'audio_only':
      custom_opts['format'] = 'bestaudio/best'
      custom_opts['postprocessors'] = [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': '192',
      }]
    elif data.resolution == 'best' or not data.resolution.isdigit():
      custom_opts['format'] = 'bestvideo+bestaudio/best'
      custom_opts['merge_output_format'] = 'mp4'
    else:
      custom_opts['format'] = (
          f'bestvideo[height<={data.resolution}]+bestaudio/best[height<={data.resolution}]/best[height<={data.resolution}]/best'
      )
      custom_opts['merge_output_format'] = 'mp4'

    ydl_opts = get_ydl_options(data.url, custom_opts)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(data.url, download=True)
      file_name = ydl.prepare_filename(info)

    if data.resolution == 'audio_only':
      file_name = os.path.splitext(file_name)[0] + '.mp3'
    else:
      base = os.path.splitext(file_name)[0]
      if os.path.exists(base + '.mp4'):
        file_name = base + '.mp4'

    tasks_progress[task_id] = {'status': 'finished', 'percent': 100}
    background_tasks.add_task(remove_file, file_name)

    return FileResponse(
        path=file_name,
        filename=os.path.basename(file_name),
        media_type='application/octet-stream',
    )
  except Exception as e:
    tasks_progress[task_id] = {'status': 'error', 'percent': 0}
    raise HTTPException(status_code=500, detail=str(e))


@app.get('/', response_class=HTMLResponse)
def serve_home():
  with open('index.html', 'r', encoding='utf-8') as f:
    return f.read()


@app.get('/logo.png')
def get_logo():
  if os.path.exists('logo.png'):
    return FileResponse('logo.png', media_type='image/png')
  for f in os.listdir('.'):
    if f.lower().startswith('logo'):
      return FileResponse(f, media_type='image/png')
  return Response(status_code=404)