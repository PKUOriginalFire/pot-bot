import nonebot
from nonebot import require, get_plugin_config, logger
from datetime import datetime
from .config import Config

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler


# --------------------------
# Author: Zachary Chen
# --------------------------


logger.info("----------- scheduler -----------")

config = get_plugin_config(Config)


def is_online(status: dict):
    online = status.get("online", False)
    for bot in status.get("bots", []):
        online = online or bot.get("online", False)
    return online


def send_status_notify(status: dict, online: bool):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Pot Bot Status"
    msg["From"] = config.smtp_username
    msg["To"] = config.mailto
    msg.attach(
        MIMEText(
            f"Bot is {'online' if online else 'offline'}\n"
            f"Current time: {datetime.now()}\n"
            f"Status: {status}",
            "plain",
        )
    )

    with smtplib.SMTP(config.smtp_server, config.smtp_port) as server:
        server.login(config.smtp_username, config.smtp_password)
        server.sendmail(config.smtp_username, config.mailto, msg.as_string())
        logger.info(f"send status notify to {config.mailto}")


last_online_status = True


@scheduler.scheduled_job("interval", minutes=5)
async def status_scheduler():
    global last_online_status
    logger.debug("status scheduler")
    if not nonebot.get_bots():
        return

    bot = nonebot.get_bot()
    status = await bot.get_status()
    online = is_online(status or {})
    if online != last_online_status:
        send_status_notify(status, online)
        last_online_status = online
