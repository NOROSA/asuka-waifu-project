from __future__ import annotations

import asyncio
import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from .config import settings
from .agent import ask_asuka_sync

logger = logging.getLogger(__name__)

class TsundereBot:
    def __init__(self):
        self.application = (
            ApplicationBuilder()
            .token(settings.telegram_bot_token)
            .concurrent_updates(True)
            .build()
        )

        self.application.add_handler(CommandHandler("start", self._cmd_start))
        self.application.add_handler(CommandHandler("help", self._cmd_help))
        self.application.add_handler(
            MessageHandler(filters.TEXT & (~filters.COMMAND), self._handle_message)
        )

    async def _cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("¿Qué miras, baka? ¡Escribe algo si te atreves!")

    async def _cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Habla conmigo y ya. No necesito manual, ¿vale? ʕ•ᴥ•ʔ")

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_msg = update.message.text
        logger.info("%s dice: %s", update.effective_user.username, user_msg)
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, ask_asuka_sync, user_msg)
        await update.message.reply_text(response)

    def run(self):
        logger.info("Bot en marcha – esperando mensajes…")
        self.application.run_polling()