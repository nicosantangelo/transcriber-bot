# pylint: disable=missing-module-docstring, missing-function-docstring
import os
import time
import logging
import typing
import telegram
import telegram.ext as t_ext
import decode

# from telegram import ext as telegram_ext

# from telegram.ext import (
#     ApplicationBuilder,
#     ContextTypes,
#     MessageHandler,
#     filters,
#     CallbackContext,
# )


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARN
)


async def handle_voice(
    update: telegram.Update, _context: t_ext.ContextTypes.DEFAULT_TYPE
) -> None:
    file = await update.message.voice.get_file()
    await transcribe_file(update.message, file)


async def handle_audio(
    update: telegram.Update, _context: t_ext.ContextTypes.DEFAULT_TYPE
) -> None:
    file = await update.message.audio.get_file()
    await transcribe_file(update.message, file)


async def transcribe_file(message: telegram.Message, file: telegram.File):
    start_time = time.time()
    await message.reply_text("Got it! Transcribing message. Hang in there cowboy")

    for segment in decode.transcribe(file.file_path):
        await message.reply_text(segment.text)

    end_time = time.time()
    await message.reply_text("Took: " + str(round(end_time - start_time)) + " seconds")


def start_bot(token: str):
    application = t_ext.ApplicationBuilder().token(token).build()
    application.add_handler(t_ext.MessageHandler(t_ext.filters.VOICE, handle_voice))
    application.add_handler(t_ext.MessageHandler(t_ext.filters.AUDIO, handle_audio))
    application.add_error_handler(handle_error)
    print("Bot Started")
    application.run_polling(allowed_updates=telegram.Update.MESSAGE)


async def handle_error(_: typing.Optional[object], __: t_ext.CallbackContext):
    # We're already logging via the global logging object
    return


def main():
    token = os.environ["TOKEN"]
    start_bot(token)


if __name__ == "__main__":
    main()
