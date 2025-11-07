"""Simple configuration file."""

import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("HMS_DATABASE_URI", "sqlite:///hms.sqlite")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SMTP_SERVER = os.getenv("HMS_SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("HMS_SMTP_PORT", 587))
    FROM_EMAIL = os.getenv("FROM_EMAIL", "lasyareddypulilasyareddypuli@gmail.com")
    APP_PASSWORD = os.getenv("APP_PASSWORD", "pxwvdygqfwqhkytz")
    TO_EMAIL = os.getenv("TO_EMAIL", "lasyareddypulilasyareddypuli@gmail.com")

    BATCH_SIZE = int(os.getenv("HMS_BATCH_SIZE", 10))

    LOG_FILE = os.getenv("HMS_LOG_FILE", "hms.log")
    LOG_LEVEL = os.getenv("HMS_LOG_LEVEL", "INFO")
