from faster_whisper import WhisperModel
from config import WHISPER_MODEL_SIZE

# بيتحمّل مرة وحدة لما يبلش البوت، وبيضل بالذاكرة لكل الطلبات بعدين.
# device="cpu" يشتغل بأي جهاز. إذا عندك GPU بيدعم CUDA، بدّلها لـ "cuda" وبتصير أسرع بكتير.
model = WhisperModel(WHISPER_MODEL_SIZE, device="cpu", compute_type="int8")


def transcribe_audio(file_path: str) -> str:
    """يحوّل ملف صوتي لنص محلياً عبر faster-whisper - بدون API ولا إنترنت."""
    segments, _ = model.transcribe(file_path, language="ar")
    return " ".join(segment.text.strip() for segment in segments)