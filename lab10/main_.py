import asyncio
import logging
import os
from typing import Any

import requests
from telegram import Update
from telegram.ext import (Application, ContextTypes,
                          MessageHandler, filters)

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = "7687972992:AAGJNdajKIHbcYNGPm7fPX1aWKYrpAAILlk"
VK_TOKEN = "vk2.a._YUbjPu0AVZYqxIMEkCik-poeTdv7Lr2AOfF_tCnfXVUzJQmHiEfFA3x4QIDlEBBPjrgYl9cl3pA_IoDzdNoUZ4vqUj9zuB60uwqfK5bHHYyE8ADYyJ1GwLZAyMyTH7WN45yrBUnbWT_JxDbxFQdPyHf0MK67ELVrKqn7iObjTPeDWwBQ2TD8-XYVkXML9Qb6LPJXknEPu4HWWOpIoF1clE8B7-bPK179X-cIVT5mYNdCIn0EjYD24oCZ2AxoN8K"
VK_USER_ID = "183219734"
VK_API_VERSION = "5.131"

if not all((TELEGRAM_TOKEN, VK_TOKEN, VK_USER_ID)):
    raise RuntimeError(
        "Отсутствуют переменные окружения TELEGRAM_TOKEN, VK_TOKEN или VK_USER_ID")

# ---------------------------------------------------------------------------
# VK API helpers
# ---------------------------------------------------------------------------
VK_ENDPOINT = "https://api.vk.com/method/"

def vk_api(method: str, **params: Any) -> dict:
    """Вызов метода VK API (HTTP GET)."""
    payload = {
        "access_token": VK_TOKEN,
        "v": VK_API_VERSION,
        **params,
    }
    url = f"{VK_ENDPOINT}{method}"
    logger.debug("VK API %s %s", method, payload)
    response = requests.get(url, params=payload, timeout=10)
    response.raise_for_status()
    data = response.json()
    if "error" in data:
        raise RuntimeError(f"VK API error: {data['error']}")
    return data["response"]

def comment_last_post(message: str) -> None:
    wall_resp = vk_api("wall.get", owner_id=VK_USER_ID, count=5)
    items = wall_resp.get("items")
    if not items:
        logger.warning("На стене нет постов — комментарий не отправлен.")
        return
    post_id = items[1]["id"]
    vk_api("wall.createComment", owner_id=VK_USER_ID, post_id=post_id, message=message)
    logger.info("Комментарий добавлен к посту %s", post_id)

# ---------------------------------------------------------------------------
# Telegram bot handlers
# ---------------------------------------------------------------------------
async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик входящих текстовых сообщений."""
    message_text = update.effective_message.text or ""
    user = update.effective_user.full_name if update.effective_user else "?"
    logger.info("Получено сообщение от %s: %s", user, message_text)
    await update.message.reply_text("Пересылаю ваше сообщение во ВКонтакте…")
    try:
        comment_last_post(message_text)
        await update.message.reply_text("✅ Комментарий опубликован!")
    except Exception as exc:
        logger.exception("Не удалось опубликовать комментарий")
        await update.message.reply_text(f"❌ Ошибка: {exc}")

# ---------------------------------------------------------------------------
# Entrypoint (без asyncio.run — чтобы не дублировать event loop)
# ---------------------------------------------------------------------------

def main() -> None:
    """Создаёт Application и запускает polling (блокирует поток)."""
    app: Application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Обрабатываем только обычные текстовые сообщения (без команд)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    logger.info("Бот запущен. Ожидаю сообщения…")
    # Эта функция сама создаёт и управляет event‑loop, поэтому
    # дополнительный asyncio.run не нужен и вызывал исключение
    app.run_polling()

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Завершение работы бота.")
