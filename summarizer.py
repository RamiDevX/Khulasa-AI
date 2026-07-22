import json
import requests
from config import OLLAMA_MODEL, OLLAMA_URL

# كل جزء (chunk) بالحد الأقصى هيك عدد كلمات قبل ما نقسم النص
# رقم محافظ يضمن إنه كل جزء يضل جوا نافذة السياق (num_ctx) حتى مع البرومبت والناتج
CHUNK_WORD_LIMIT = 1500

# نافذة سياق أوسع من افتراضي Ollama (غالباً 2048) عشان ما ينقطع النص
NUM_CTX = 8192

# حرارة منخفضة نسبياً = ناتج أدق وأقل "ارتجال"، بيقلل الأخطاء الإملائية/النحوية
TEMPERATURE = 0.3

QUALITY_RULES = """
قواعد صارمة لازم تلتزم فيها:
- اكتب بالعربية الفصحى السليمة 100% إملائياً ونحوياً، بدون أي خطأ إملائي أو حرف ناقص أو زايد.
- لا تخترع معلومات مش موجودة بالنص، وإذا في جزء غير واضح تجاهله بدل ما تخمّن.
- ما تكرر نفس الفكرة بصيغ مختلفة.
"""

SYSTEM_PROMPT_CHUNK = """أنت مساعد بيحلل جزء واحد من تفريغ صوتي لاجتماع طويل (الاجتماع مقسوم لأجزاء متتالية).
مهمتك بس بهاد الجزء:
1. استخرج أهم النقاط والقرارات المذكورة (نقاط مختصرة، وحدة الفكرة بكل نقطة).
2. استخرج أي Action Items واضحة مع اسم المسؤول إذا انذكر.
""" + QUALITY_RULES + """
رد فقط بصيغة JSON صحيحة بهاد الشكل بالضبط، بدون أي نص إضافي قبلها أو بعدها:
{
  "key_points": ["string", "string", ...],
  "action_items": ["string", "string", ...]
}
"""

SYSTEM_PROMPT_FINAL_TEMPLATE = """أنت مساعد متخصص بتلخيص الاجتماعات.
بيوصلك نص خام (أو نقاط مستخرجة من اجتماع)، ومطلوب منك:
1. ملخص شامل يغطي أهم النقاط والقرارات يلي انأخدت. __LENGTH_INSTRUCTION__
2. لائحة Action Items واضحة وموحّدة (بدون تكرار)، وحدد المسؤول عن كل مهمة إذا انذكر بالاجتماع.
""" + QUALITY_RULES + """
رد فقط بصيغة JSON صحيحة وبهاد الشكل بالضبط، بدون أي نص إضافي قبلها أو بعدها:
{
  "summary": "string",
  "action_items": ["string", "string", ...]
}
"""


def _length_instruction(word_count: int) -> str:
    """بتحدد طول الملخص المطلوب حسب طول الاجتماع (عدد كلمات التفريغ)."""
    if word_count < 600:
        return "اجتماع قصير، خليه بـ 3-4 جمل بس."
    if word_count < 2500:
        return "اجتماع متوسط، اكتب 5-8 جمل."
    if word_count < 8000:
        return "اجتماع طويل نسبياً، اكتب 8-12 جملة أو نظّمه بنقاط رئيسية."
    return (
        "هاد اجتماع طويل جداً (عدة ساعات). ممنوع تحاول تغطي كل صغيرة وكبيرة. "
        "لخّص بس أهم المحاور والقرارات المفصلية بشكل نقاط مرتبة (12-18 نقطة كحد أقصى)، "
        "واهمل أي تفاصيل ثانوية أو نقاشات جانبية."
    )


def _normalize_action_item(item) -> str:
    """بتحوّل أي شكل يرجعه الموديل (string أو dict) لسطر نصي واحد موحّد."""
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        # الموديل أحياناً بيرجّع {"task": "...", "owner": "..."} بدل string خام
        task = item.get("task") or item.get("item") or item.get("description") or ""
        owner = item.get("owner") or item.get("responsible") or item.get("assignee")
        if owner:
            return f"{task} ({owner})".strip()
        return str(task).strip() or json.dumps(item, ensure_ascii=False)
    return str(item)


def _call_ollama(system_prompt: str, user_content: str) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                "stream": False,
                "format": "json",  # Ollama بيضمن يرجع JSON صحيح بهاد الوضع
                "options": {
                    "temperature": TEMPERATURE,
                    "num_ctx": NUM_CTX,
                },
            },
            timeout=900,  # 15 دقيقة عشان الاجتماعات الطويلة
        )
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "ما قدرت أوصل لـ Ollama. تأكد إنه سيرفر Ollama شغّال على هاد الجهاز "
            f"(جرّب: ollama serve) وإنه الموديل '{OLLAMA_MODEL}' محمّل (ollama pull {OLLAMA_MODEL})."
        )

    response.raise_for_status()
    return response.json()["message"]["content"]


def _split_into_chunks(transcript: str, chunk_word_limit: int = CHUNK_WORD_LIMIT) -> list[str]:
    words = transcript.split()
    return [
        " ".join(words[i:i + chunk_word_limit])
        for i in range(0, len(words), chunk_word_limit)
    ]


def summarize_transcript(transcript: str) -> dict:
    """يرسل النص المفرّغ لموديل محلي عبر Ollama ويرجع dict فيه الملخص وAction Items.

    للاجتماعات الطويلة (أكتر من CHUNK_WORD_LIMIT كلمة)، بيتقسم النص لأجزاء (map)،
    كل جزء بيتلخص لوحده، وبعدين كل الأجزاء بتتجمع بملخص نهائي واحد (reduce).
    هيك بنتجنب مشكلة نافذة السياق المحدودة وبنضمن تغطية الاجتماع كامل.
    """
    words = transcript.split()
    total_words = len(words)
    length_instruction = _length_instruction(total_words)

    if total_words <= CHUNK_WORD_LIMIT:
        # اجتماع قصير/متوسط - طلب واحد مباشر
        final_prompt = SYSTEM_PROMPT_FINAL_TEMPLATE.replace("__LENGTH_INSTRUCTION__", length_instruction)
        content = _call_ollama(final_prompt, transcript)
        parsed = json.loads(content)
    else:
        # اجتماع طويل - map: نلخص كل جزء عالحدة
        chunks = _split_into_chunks(transcript)
        all_key_points = []
        all_partial_actions = []

        for chunk in chunks:
            chunk_content = _call_ollama(SYSTEM_PROMPT_CHUNK, chunk)
            try:
                chunk_parsed = json.loads(chunk_content)
            except json.JSONDecodeError:
                continue
            all_key_points.extend(chunk_parsed.get("key_points", []) or [])
            all_partial_actions.extend(chunk_parsed.get("action_items", []) or [])

        # reduce: نجمع كل النقاط المستخرجة ونطلب ملخص نهائي موحّد منها
        combined_notes = (
            "نقاط مستخرجة من أجزاء الاجتماع:\n"
            + "\n".join(f"- {p}" for p in all_key_points)
            + "\n\nAction Items مستخرجة من الأجزاء:\n"
            + "\n".join(f"- {a}" for a in all_partial_actions)
        )

        final_prompt = SYSTEM_PROMPT_FINAL_TEMPLATE.replace("__LENGTH_INSTRUCTION__", length_instruction)
        content = _call_ollama(final_prompt, combined_notes)
        parsed = json.loads(content)

    # نضمن إنه action_items دايماً list of strings، بغض النظر شو رجّع الموديل فعلياً
    raw_items = parsed.get("action_items", []) or []
    parsed["action_items"] = [_normalize_action_item(i) for i in raw_items]

    return parsed