
import pytz 
_key_stock_signals_alerts = (
    "cprsignals.alerts"  # Can be anything. Has to match with "key" in your TradingView alert message. Lenh cancel, close
)
# Telegram Settings
send_telegram_alerts = True
telegram_alert_config = {
    "cprsignals.alerts": {
        "bot_token" : "5332543721:AAFaa6R56v4vwXPunxWa42AP0JGxHsh4ELI",
        "channel_id" : -838839150 #-1001871812714  #-839791639
    }
}
# _bot_token =  "" # Bot token. Get it from @Botfather
# _channelid_stock_signals =  # -1001871812714 # Channel ID (ex. -1001487568087)
# _channel_stocksignals = "stocksignals" 
# channel_2 = -1001522073506 # Channel ID (ex. -1001487568087)
# channel_swing = -1001578432315
# channel_long = -1001631403498
# channel_private= -1001654109065

# Discord Settings
send_discord_alerts = False
discord_webhook = ""  # Discord Webhook URL (https://support.discordapp.com/hc/de/articles/228383668-Webhooks-verwenden)

# Slack Settings
send_slack_alerts = False
slack_webhook = ""  # Slack Webhook URL (https://api.slack.com/messaging/webhooks)

# Curl Settings
send_curl_alerts = False
curl_webhook = "http://127.0.0.1:8888/frostybot"  

# Twitter Settings
send_twitter_alerts = False
tw_ckey = ""
tw_csecret = ""
tw_atoken = ""
tw_asecret = ""

# Email Settings
send_email_alerts = False
email_sender = ""  # Your email address
email_receivers = ["", ""]  # Receivers, can be multiple
email_subject = "Trade Alert!"

email_port = 465  # SMTP SSL Port (ex. 465)
email_host = ""  # SMTP host (ex. smtp.gmail.com)
email_user = ""  # SMTP Login credentials
email_password = ""  # SMTP Login credentials

IST = pytz.timezone('Asia/Kolkata')