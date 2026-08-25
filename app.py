import os
import uuid
import asyncio
import tempfile
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

# Dicionário em memória para armazenar o progresso das tarefas
tasks_progress = {}

class InfoRequest(BaseModel):
    url: str

class DownloadRequest(BaseModel):
    url: str
    resolution: str
    task_id: str

def remove_file(path: str):
    if os.path.exists(path):
        os.remove(path)

@app.post("/api/info")
def get_video_info(data: InfoRequest):
    try:
        ydl_opts = {"quiet": True, "no_warnings": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.url, download=False)
            resolutions = set()
            for f in info.get("formats", []):
                height = f.get("height")
                vcodec = f.get("vcodec")
                if height and vcodec != "none":
                    resolutions.add(height)
            
            return {
                "title": info.get("title"),
                "thumbnail": info.get("thumbnail"),
                "resolutions": sorted(list(resolutions), reverse=True)
            }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/progress/{task_id}")
async def progress_stream(task_id: str):
    async def event_generator():
        while True:
            prog = tasks_progress.get(task_id, {"status": "waiting", "percent": 0})
            yield f"data: {prog.get('percent', 0)}|{prog.get('status', '')}\n\n"
            if prog.get("status") in ["finished", "error"]:
                # Limpa a memória após concluir
                tasks_progress.pop(task_id, None)
                break
            await asyncio.sleep(0.4)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/api/download")
def download_video(data: DownloadRequest, background_tasks: BackgroundTasks):
    task_id = data.task_id
    tasks_progress[task_id] = {"status": "downloading", "percent": 0}

    def progress_hook(d):
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            if total > 0:
                percent = int((downloaded / total) * 100)
                tasks_progress[task_id] = {"status": "downloading", "percent": percent}
        elif d['status'] == 'finished':
            tasks_progress[task_id] = {"status": "converting", "percent": 100}

    try:
        temp_dir = tempfile.mkdtemp()
        output_template = os.path.join(temp_dir, "%(title)s.%(ext)s")
        
        if data.resolution == "audio_only":
            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": output_template,
                "progress_hooks": [progress_hook],
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
                "quiet": True,
                "no_warnings": True
            }
        else:
            ydl_opts = {
                "format": f"bestvideo[height<={data.resolution}]+bestaudio/best[height<={data.resolution}]",
                "merge_output_format": "mp4",
                "outtmpl": output_template,
                "progress_hooks": [progress_hook],
                "quiet": True,
                "no_warnings": True
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(data.url, download=True)
            file_name = ydl.prepare_filename(info)
            
            if data.resolution == "audio_only":
                file_name = os.path.splitext(file_name)[0] + ".mp3"
            elif not file_name.endswith(".mp4"):
                file_name = os.path.splitext(file_name)[0] + ".mp4"

        tasks_progress[task_id] = {"status": "finished", "percent": 100}
        background_tasks.add_task(remove_file, file_name)

        return FileResponse(
            path=file_name,
            filename=os.path.basename(file_name),
            media_type="application/octet-stream"
        )
    except Exception as e:
        tasks_progress[task_id] = {"status": "error", "percent": 0}
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
def serve_home():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()