# ----------------------------------------------- #
# Plugin Name           : TradingView-Webhook-Bot #
# Author Name           : fabston                 #
# File Name             : handler.py              #
# ----------------------------------------------- #

import smtplib
import ssl
from email.mime.text import MIMEText
import requests


from telegram import Bot

from webhook.config import settings

async def send_message(msg, id):
    config = settings.telegram_alert_config[id]
    if settings.send_telegram_alerts:
        tg_bot = Bot(token=config["bot_token"])
        try:
            await tg_bot.sendMessage(
                config["channel_id"],
                msg
                .encode("latin-1", "backslashreplace")
                .decode("unicode_escape"),
                parse_mode="HTML",
                disable_web_page_preview=True
            )
        except Exception as e:
            print("[X] Telegram Error:\n>", e)

def send_message_to_channel(msg, channel_, token_):
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
