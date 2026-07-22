
<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0b2545,50:134074,100:00a86b&height=180&section=header&text=KhulasaAI&fontSize=60&fontColor=fff&animation=fadeIn&fontAlignY=38&desc=Meeting%20Summarizer%20Bot&descAlignY=58&descAlign=50"/>

<p>
  <b>Turn meeting recordings into clean summaries and actionable to-do lists — entirely on your own machine 🔒</b>
</p>

<p>
  <a href="https://t.me/KhulasaAI_bot">
    <img src="https://img.shields.io/badge/Telegram-@KhulasaAI__bot-0b2545?style=for-the-badge&logo=telegram&logoColor=white" />
  </a>
  <a href="https://python.org">
    <img src="https://img.shields.io/badge/Python-3.10+-134074?style=for-the-badge&logo=python&logoColor=white" />
  </a>
  <img src="https://img.shields.io/badge/Status-Active-00a86b?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-05668d?style=for-the-badge" />
</p>

</div>

<br/>

## 🔹 About

**KhulasaAI** is a privacy-first Telegram bot that turns meeting recordings into clean summaries and actionable to-do lists — entirely on your own machine. No paid APIs, no cloud transcription, no data ever leaves your computer.

Send a voice note or audio file to the bot, and get back:
- A concise, adaptive-length **summary** of the meeting
- A clean list of **Action Items**, with owners identified when mentioned
- A saved record of every meeting in a local SQLite database

<br/>

## ✨ Features

| | |
|---|---|
| 🔒 | 100% local processing — speech-to-text and summarization both run on your machine |
| 🎤 | Accurate Arabic transcription via faster-whisper |
| 🧠 | Local LLM summarization via Ollama — works with any chat model you have pulled locally |
| 📏 | Adaptive summary length — short meetings get tight summaries; long meetings get organized bullet lists |
| 🧩 | Map-reduce chunking for long meetings — avoids context-window truncation issues |
| 🗃️ | Local archive — every transcript, summary, and action item list is saved to SQLite |
| 🤖 | Simple Telegram UX — just send a voice note or audio file, no commands needed |

<br/>

## 🛠️ Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-134074?style=for-the-badge&logo=python&logoColor=white)
![Aiogram](https://img.shields.io/badge/Aiogram-00a86b?style=for-the-badge&logo=telegram&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-0b2545?style=for-the-badge&logo=ollama&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-05668d?style=for-the-badge&logo=sqlite&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-02c39a?style=for-the-badge&logo=ffmpeg&logoColor=white)

</div>

<br/>

## 📋 Requirements

- Python 3.10+
- [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) installed and available on your system `PATH`
- [Ollama](https://ollama.com/download) installed and running locally
- A Telegram bot token from [@BotFather](https://t.me/BotFather)

<br/>

## 🚀 Getting Started

**1. Clone the repo**
```bash
git clone [https://github.com/RamiDevX/KhulasaAI.git](https://github.com/RamiDevX/KhulasaAI.git)
cd KhulasaAI

```
**2. Create and activate a virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

```
**3. Install dependencies**
```bash
pip install -r requirements.txt

```
**4. Configure environment variables**
Create a .env file in the project root:
```env
BOT_TOKEN=your_telegram_bot_token_here
WHISPER_MODEL_SIZE=small
OLLAMA_MODEL=llama3.2
OLLAMA_URL=http://localhost:11434/api/chat

```
**5. Run the bot**
```bash
python bot.py

```
## 📂 Project Structure
```
KhulasaAI/
├── bot.py             # Telegram bot entry point & message handlers
├── transcription.py   # Local speech-to-text via faster-whisper
├── summarizer.py      # Local LLM summarization via Ollama
├── database.py        # SQLite persistence layer
├── config.py          # Environment-based configuration
├── requirements.txt
├── .env.example
└── README.md

```
## 📝 Notes
> [!NOTE]
> The first run downloads the faster-whisper model weights, so the first request takes longer than usual.
> 
> [!NOTE]
> For better Arabic output quality, consider using an Arabic-tuned model like command-r7b-arabic.
> 
> [!WARNING]
> Never commit your .env file or bot token to version control.
> 
<img width="100%" src="https://capsule-render.vercel.app/api?type=rect&color=0:0b2545,50:134074,100:00a86b&height=3"/>
## 👨‍💻 Developer
<div align="center">
**Rami Bitar**
<a href="https://github.com/RamiDevX">
<img src="https://img.shields.io/badge/GitHub-RamiDevX-0b2545?style=for-the-badge&logo=github&logoColor=white" />
</a>
<a href="https://t.me/ramidevx">
<img src="https://img.shields.io/badge/Telegram-@ramidevx-134074?style=for-the-badge&logo=telegram&logoColor=white" />
</a>
<a href="https://linkedin.com/in/rami-bitar-16479936b">
<img src="https://img.shields.io/badge/LinkedIn-Rami%20Bitar-00a86b?style=for-the-badge&logo=linkedin&logoColor=white" />
</a>



<sub>KhulasaAI © 2026</sub>
</div>
<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0b2545,50:134074,100:00a86b&height=100&section=footer"/>
