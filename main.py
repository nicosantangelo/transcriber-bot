# pylint: disable=missing-module-docstring, missing-function-docstring
import os
import time
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
    print("Got message")
    message = update.message
    file = await message.voice.get_file()
    start_time = time.time()
    await message.reply_text("Got it! Transcribing message. Hang in there cowboy")

    for segment in transcribe(file.file_path):
        await message.reply_text(segment.text)

    end_time = time.time()
    await message.reply_text("Took: " + str(round(end_time - start_time)) + " seconds")


def main():
    token = os.environ["TOKEN"]
    application = ApplicationBuilder().token(token).build()
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("Bot started")
    application.run_polling(allowed_updates=Update.MESSAGE)


if __name__ == "__main__":
    main()
