import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_TOKEN
from transcription import transcribe_audio
from summarizer import summarize_transcript
from database import init_db, save_meeting

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


DEV_KEYBOARD = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="👨‍💻 مطوّر البوت", url="https://t.me/ramidevx")]
    ]
)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "أهلاً فيك! 👋\n\n"
        "أنا بوت *KhulasaAI* — بساعدك تلخّص اجتماعاتك بسرعة وبدون تعب.\n\n"
        "🎯 *شو بعمل بالضبط؟*\n"
        "بتبعتلي أي تسجيل صوتي أو ملف صوت لاجتماع، وأنا:\n"
        "1️⃣ بحوّل الصوت لنص كامل (تفريغ صوتي).\n"
        "2️⃣ بحلل النص وبطلعلك ملخص مختصر وواضح.\n"
        "3️⃣ بستخرجلك لائحة *Action Items* مع تحديد المسؤول عن كل مهمة (إذا انذكر بالاجتماع).\n\n"
        "📌 *نقاط مهمة قبل ما تبلش:*\n"
        "• كل شي بيصير محلياً على جهازك — ما في أي بيانات بتطلع عبر الإنترنت.\n"
        "• الاجتماعات الطويلة بتاخد وقت أطول شوي بالمعالجة، فضل صبور 🙂\n"
        "• لأفضل نتيجة، خلي التسجيل واضح وبعيد عن الضجيج قد الإمكان.\n"
        "• بمجرد ما تخلص المعالجة، بترجعلك النتيجة تلقائياً هون بالشات.\n\n"
        "جاهز؟ ابعتلي الملف الصوتي وخلينا نبلش! 🎧"
    )
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=DEV_KEYBOARD)


@dp.message(F.voice | F.audio)
async def handle_audio(message: Message):
    status_msg = await message.answer("🎧 عم أحمّل وأحوّل الصوت لنص...")

    file = message.voice or message.audio
    file_info = await bot.get_file(file.file_id)
    local_path = os.path.join(DOWNLOAD_DIR, f"{file.file_id}.ogg")
    await bot.download_file(file_info.file_path, local_path)

    try:
        transcript = transcribe_audio(local_path)
        await status_msg.edit_text("🧠 عم ألخص الاجتماع...")

        result = summarize_transcript(transcript)
        summary = result.get("summary", "")
        action_items = result.get("action_items", [])

        save_meeting(message.from_user.id, transcript, summary, action_items)

        reply = f"📝 *ملخص الاجتماع:*\n{summary}\n\n"
        if action_items:
            reply += "✅ *Action Items:*\n"
            reply += "\n".join(f"• {item}" for item in action_items)
        else:
            reply += "ما في Action Items واضحة بهاد الاجتماع."

        await status_msg.edit_text(reply, parse_mode="Markdown")
    except Exception as e:
        logging.exception("Error processing meeting audio")
        await status_msg.edit_text(f"⚠️ صار في خطأ أثناء المعالجة: {e}")
    finally:
        if os.path.exists(local_path):
            os.remove(local_path)


async def main():
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())