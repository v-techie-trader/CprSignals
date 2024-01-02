# ----------------------------------------------- #
# Plugin Name           : TradingView-Webhook-Bot #
# Author Name           : fabston                 #
# File Name             : handler.py              #
# ----------------------------------------------- #

import smtplib
import ssl
from email.mime.text import MIMEText

import logging

from telegram import Bot
from telegram.error  import BadRequest
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
from webhook.config import settings
logger = logging.getLogger(__name__)

from telegram.error  import BadRequest
async def send_message(msg, chat_id, topic,id="cprsignals.alerts",):
    config = settings.telegram_alert_config[id]
    if settings.send_telegram_alerts:
        tg_bot = Bot(token=config["bot_token"])
        try:
            logger.info(f"sending message {config} to topic {topic}")
            await tg_bot.sendMessage(
                chat_id,
                msg
                .encode("latin-1", "backslashreplace")
                .decode("unicode_escape"),
                parse_mode="HTML",
                disable_web_page_preview=True,
                message_thread_id=topic
            )
        except BadRequest as e:
            logger.error("[X] Telegram Error:\n>", e)
            logger.info(f"sending message {config} without topic")
            await tg_bot.sendMessage(
                chat_id,
                msg
                .encode("latin-1", "backslashreplace")
                .decode("unicode_escape"),
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
        except Exception as e:
            logger.error("[X] Telegram Error:\n>", e)


async def send_photo(msg, filename, topic,id="cprsignals.alerts",):
    config = settings.telegram_alert_config[id]
    if settings.send_telegram_alerts:
        tg_bot = Bot(token=config["bot_token"])
        try:
            await tg_bot.sendPhoto(
                config["channel_id"],
                # msg
                # .encode("latin-1", "backslashreplace")
                # .decode("unicode_escape"),
                photo=open(filename, 'rb'),
                message_thread_id=topic
            )
        except Exception as e:
            print("[X] Telegram Error:\n>", e)       

async def send_document(chat_id, filename,topic, msg="", id="cprsignals.alerts",):
    config = settings.telegram_alert_config[id]
    if settings.send_telegram_alerts:
        tg_bot = Bot(token=config["bot_token"])
        try:
            await tg_bot.send_document(
                chat_id,
                caption=msg,
                document=open(filename, 'rb'),
                message_thread_id=topic
            )
        except Exception as e:
            print("[X] Telegram Error:\n>", e)      

def send_message_to_channel(msg, channel_, token_, topic):
    if settings.send_telegram_alerts:
        tg_bot = Bot(token=token_)
        # try:
        #     tg_bot.sendMessage(
        #         channel_,
        #         msg
        #         .encode("latin-1", "backslashreplace")
        #         .decode("unicode_escape"),
        #         parse_mode="HTML",
        #         disable_web_page_preview=True
        #     )
        # except Exception as e:
        #     print("[X] Telegram Error:\n>", e)

def send_alert(data):
    if settings.send_telegram_alerts:
        tg_bot = Bot(token=settings._bot_token)
        try:
            tg_bot.sendMessage(
                data["telegram"],
                data["msg"]
                .encode("latin-1", "backslashreplace")
                .decode("unicode_escape"),
                parse_mode="MARKDOWN",
            )
        except KeyError:
            tg_bot.sendMessage(
                settings.channel_1,
                data["msg"]
                .encode("latin-1", "backslashreplace")
                .decode("unicode_escape"),
                parse_mode="MARKDOWN",
            )
        except Exception as e:
            print("[X] Telegram Error:\n>", e)

    if settings.send_email_alerts:
        try:
            email_msg = MIMEText(
                data["msg"].replace("*", "").replace("_", "").replace("`", "")
            )
            email_msg["Subject"] = settings.email_subject
            email_msg["From"] = settings.email_sender
            email_msg["To"] = settings.email_sender
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(
                settings.email_host, settings.email_port, context=context
            ) as server:
                server.login(settings.email_user, settings.email_password)
                server.sendmail(
                    settings.email_sender, settings.email_receivers, email_msg.as_string()
                )
                server.quit()
        except Exception as e:
            print("[X] Email Error:\n>", e)
