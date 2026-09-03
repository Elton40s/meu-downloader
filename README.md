# 🚀 YETLoad — YouTube Video Downloader

> **Baixe vídeos e áudios do YouTube com velocidade, simplicidade e sem distrações.**

O **YETLoad** é um ecossistema leve, intuitivo e moderno para download de mídias da web. Projetado com foco em **experiência do usuário (UX)** e alta eficiência de processamento, a plataforma entrega conversões rápidas de vídeo (MP4) e áudio (MP3/M4A) com uma interface fluida, responsiva e com suporte nativo a múltiplos idiomas e temas.

---

## ⚡ Destaques & Diferenciais

* **⚡ Download em Poucos Cliques:** Cole a URL e baixe em questão de segundos.
* **🎥 Seleção Flexível de Qualidade:** Suporte a múltiplas resoluções em MP4 e extração direta de áudio em MP3.
* **🌗 Interface Adaptável (Light/Dark Mode):** Alternância instantânea de tema com persistência visual fluida.
* **🌍 Suporte Multilíngue:** Interface traduzida nativamente para Português, Inglês e Espanhol.
* **📊 Progresso em Tempo Real:** Acompanhamento do status de download/conversão via Server-Sent Events (SSE).
* **📱 Design Mobile-First:** Layout totalmente responsivo com suporte nativo para colagem rápida de links no celular.

---

## 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia | Função no Projeto |
| :--- | :--- | :--- |
| **Frontend** | HTML5 / CSS3 (Pure) | Componentização moderna sem frameworks pesados, garantindo carregamento ultrarrápido |
| **Frontend** | JavaScript (Vanilla ES6+) | Manipulação dinâmica do DOM, Clipboard API e comunicação em tempo real via SSE |
| **Backend** | Python 3.10+ | Linguagem base para lógica de manipulação e automação |
| **Backend** | FastAPI | Framework assíncrono de alta performance para a construção da API |
| **Core Engine** | `yt-dlp` | Mecanismo principal de extração e processamento das mídias |

---

## 📂 Estrutura do Projeto

```text
yetload/
├── static/          # Arquivos estáticos (Logo, CSS e assets)
├── templates/       # Páginas HTML (index.html)
├── main.py          # Servidor FastAPI e rotas da API (/api/info, /api/download)
├── requirements.txt # Dependências Python



## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos

* **Python 3.10+** instalado no sistema.
* **FFmpeg** instalado e adicionado às variáveis de ambiente (necessário para conversões de áudio e união de faixas de vídeo).

### Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/yetload.git](https://github.com/seu-usuario/yetload.git)
   cd yetload
└── README.md        # Documentação do projeto

Crie e ative o ambiente virtual:

        Linux / macOS:
        Bash

        python3 -m venv venv
        source venv/bin/activate

        Windows (PowerShell):
        PowerShell

        python -m venv venv
        .\venv\Scripts\Activate.ps1

    Instale as dependências:
    Bash

    pip install -r requirements.txt

    Inicie a aplicação:
    Bash

    uvicorn main:app --reload

    Acesse no navegador:
    Abra a URL http://127.0.0.1:8000

📄 Licença e Uso

Este projeto foi desenvolvido estritamente para fins educativos e de aprimoramento de portfólio em desenvolvimento web e integração de APIs. Respeite os direitos autorais dos criadores de conteúdo ao utilizar a ferramenta.

Desenvolvido por Elton Campos


Quer ajustar mais alguma frase ou já está pronto para commitar no GitHub?
