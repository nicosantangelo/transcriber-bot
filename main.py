# pylint: disable=missing-module-docstring, missing-function-docstring
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)

from decode import transcribe

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARN
)


async def handle_voice(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    print("Got message", update.message.date)
    voice_path = await get_voice_path(update)

    await update.message.reply_text("Got it! Transcribing message. Hang in there cowboy")

    segments = transcribe(voice_path)

    for segment in segments:
        await update.message.reply_text(segment.text)


async def get_voice_path(update: Update):
    message_voice = update.message.voice
    file = await message_voice.get_file()
    return file.file_path


def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.run_polling(allowed_updates=Update.MESSAGE)



if __name__ == "__main__":
    main()
