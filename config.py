import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN مفقود. ضيفه بملف .env")

# اسم موديل Whisper المحلي (faster-whisper).
# tiny / base / small / medium / large-v3 — كل ما كبرت الدقة بتزيد بس بيبطأ.
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "small")

# اسم الموديل يلي حمّلته بـ Ollama (مثلاً: ollama pull llama3.2)
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
