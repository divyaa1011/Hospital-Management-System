"""Simple email sending with background thread."""

import smtplib
from email.mime.text import MIMEText
from threading import Thread
import logging
from .config import Config

logger = logging.getLogger(__name__)

def _send_email_sync(to_address: str, subject: str, body: str) -> bool:
    if not Config.FROM_EMAIL or not Config.APP_PASSWORD:
        logger.warning("Email not configured; skipping.")
        return False

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = Config.FROM_EMAIL
    msg["To"] = to_address

    try:
        with smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT, timeout=10) as smtp:
            smtp.starttls()
            smtp.login(Config.FROM_EMAIL, Config.APP_PASSWORD)
            smtp.send_message(msg)
        logger.info("email sent", extra={"to": to_address, "subject": subject})
        return True
    except Exception as exc:
        logger.exception("failed to send email")
        return False

def send_email_background(to_address: str, subject: str, body: str) -> None:
    Thread(target=_send_email_sync, args=(to_address, subject, body), daemon=True).start()
