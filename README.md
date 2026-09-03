# <img src="logo.png" alt="YETLoad Logo" width="80" style="vertical-align: middle;"> YETLoad — YouTube Video Downloader

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

## <img src="logo.png" width="60" style="vertical-align: middle;"> Como Executar o Projeto Localmente

### Pré-requisitos

* **Python 3.10+** instalado no sistema.
* **FFmpeg** instalado e adicionado às variáveis de ambiente (necessário para conversões de áudio e união de faixas de vídeo).

---

## 📄 Licença e Uso

Este projeto foi desenvolvido estritamente para fins educativos e de aprimoramento de portfólio em desenvolvimento web e integração de APIs. Respeite os direitos autorais dos criadores de conteúdo ao utilizar a ferramenta.

---

Desenvolvido por **Elton Campos**
