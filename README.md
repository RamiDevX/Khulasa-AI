# KhulasaAI 🎙️

**KhulasaAI** is a privacy-first Telegram bot that turns meeting recordings into clean summaries and actionable to-do lists — entirely on your own machine. No paid APIs, no cloud transcription, no data ever leaves your computer.

Send a voice note or audio file to the bot, and get back:
- A concise, adaptive-length **summary** of the meeting
- A clean list of **Action Items**, with owners identified when mentioned
- A saved record of every meeting in a local SQLite database

---

## ✨ Features

- 🔒 **100% local processing** — speech-to-text and summarization both run on your machine. Nothing is sent to a third-party API.
- 🎤 **Accurate Arabic transcription** via [faster-whisper](https://github.com/SYSTRAN/faster-whisper), with the language explicitly pinned to Arabic for higher accuracy.
- 🧠 **Local LLM summarization** via [Ollama](https://ollama.com) — works with any chat model you have pulled locally (e.g. `llama3.2`, or Arabic-tuned models like `command-r7b-arabic`).
- 📏 **Adaptive summary length** — a 5-minute check-in and a 4-hour strategy meeting are summarized differently. Short meetings get a tight 3–4 sentence summary; long meetings get an organized, high-level bullet list instead of an unreadable wall of text.
- 🧩 **Map-reduce chunking for long meetings** — transcripts are split into chunks, summarized individually, then merged into one coherent final summary. This avoids context-window truncation issues that would otherwise cause long meetings to be summarized incompletely.
- 🗃️ **Local archive** — every transcript, summary, and action item list is saved to a local SQLite database (`meetings.db`) for later reference.
- 🤖 **Simple Telegram UX** — just send a voice note or audio file, no commands needed.

---

## 🏗️ How it works

```
Voice note / audio file
        │
        ▼
┌───────────────────┐
│  faster-whisper    │   local speech-to-text (Arabic)
└───────────────────┘
        │  transcript
        ▼
┌───────────────────┐
│   Ollama (LLM)      │   local summarization
│  short → 1 pass     │
│  long  → map-reduce │
└───────────────────┘
        │  { summary, action_items }
        ▼
┌───────────────────┐
│     SQLite DB       │   local archive
└───────────────────┘
        │
        ▼
   Telegram reply
```

---

## 📋 Prerequisites

### 1. Python 3.10+
Make sure Python and `pip` are installed and available on your PATH.

### 2. ffmpeg
Required by faster-whisper to read audio files.

```bash
# Ubuntu / Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
choco install ffmpeg
```

### 3. Ollama
Download and install Ollama from [ollama.com/download](https://ollama.com/download), then pull a model:

```bash
ollama pull llama3.2
```

> 💡 For meaningfully better Arabic output quality, consider an Arabic-tuned model instead, e.g. `ollama pull command-r7b-arabic`, and set `OLLAMA_MODEL` accordingly in `.env`.

Make sure the Ollama server is running before starting the bot (it usually runs automatically in the background after installation, or start it manually with `ollama serve`).

### 4. A Telegram bot token
Create a bot via [@BotFather](https://t.me/BotFather) on Telegram and grab your token.

---

## 🚀 Getting started

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/KhulasaAI.git
cd KhulasaAI

# 2. (Recommended) create a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Open .env and set your BOT_TOKEN (the rest have sensible defaults)

# 5. Run the bot
python bot.py
```

Once running, open Telegram, start a chat with your bot, and send `/start` — then just send a voice note or audio file.

---

## ⚙️ Configuration

All configuration is read from `.env` (see `.env.example`):

| Variable | Description | Default |
|---|---|---|
| `BOT_TOKEN` | Your Telegram bot token from BotFather | *(required)* |
| `WHISPER_MODEL_SIZE` | faster-whisper model size: `tiny` / `base` / `small` / `medium` / `large-v3` — bigger models are more accurate but slower | `small` |
| `OLLAMA_MODEL` | The local Ollama model used for summarization | `llama3.2` |
| `OLLAMA_URL` | Ollama's chat API endpoint | `http://localhost:11434/api/chat` |

---

## 📁 Project structure

```
KhulasaAI/
├── bot.py             # Telegram bot entry point & message handlers
├── transcription.py   # Local speech-to-text via faster-whisper
├── summarizer.py       # Local LLM summarization via Ollama (adaptive length, map-reduce)
├── database.py        # SQLite persistence layer
├── config.py           # Environment-based configuration
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📝 Notes & limitations

- **First run is slower** — faster-whisper downloads its model weights once, then caches them locally.
- **CPU by default** — transcription runs on CPU. If you have an NVIDIA GPU with CUDA support, change `device="cpu"` to `device="cuda"` in `transcription.py` for a significant speed-up.
- **File size limits** — the standard Telegram Bot API allows downloading files up to 20 MB. For longer recordings, consider running a [local Bot API server](https://core.telegram.org/bots/api#using-a-local-bot-api-server) or splitting the audio beforehand.
- **Long meeting processing time** — very long meetings (multiple hours) take proportionally longer to transcribe and summarize; this is expected given everything runs locally rather than on cloud infrastructure.

---

## 🗺️ Roadmap

- [ ] `/history` command to browse recently saved meetings
- [ ] Export summaries as PDF or downloadable files
- [ ] Auto-sync Action Items to Google Sheets / Notion
- [ ] Speaker diarization (identify who said what)

---

## 👨‍💻 Developer

Built by [@ramidevx](https://t.me/ramidevx). Feel free to reach out with questions or feedback.

## 📄 License

This project is available under the MIT License — feel free to use, modify, and distribute it.
