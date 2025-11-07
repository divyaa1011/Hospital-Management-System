"""Simple scraper using requests + BeautifulSoup."""

import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def fetch_page_title(url: str) -> dict:
    try:
        resp = requests.get(url, timeout=8)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        logger.info("scraped page", extra={"url": url, "title": title})
        return {"url": url, "title": title}
    except Exception as exc:
        logger.exception("scrape failed")
        return {"url": url, "title": "", "error": str(exc)}
