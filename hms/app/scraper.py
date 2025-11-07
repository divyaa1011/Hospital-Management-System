"""Simple web scraper using requests + BeautifulSoup.

Fetches page title, meta description, and top 3 headlines.
"""

import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


def fetch_page_title(url: str) -> dict:
    """
    Fetch the title, description, and headlines from a given web page.

    Args:
        url (str): The URL of the webpage to scrape.

    Returns:
        dict: A dictionary containing:
            - 'url': the requested URL
            - 'title': text inside <title> tag
            - 'description': content from <meta name="description">
            - 'headlines': list of up to 3 h1/h2 headlines
            - 'error': error message (if scraping fails)
    """
    try:
        # 1️⃣ Download page
        resp = requests.get(url, timeout=8)
        resp.raise_for_status()

        # 2️⃣ Parse HTML content
        soup = BeautifulSoup(resp.text, "html.parser")

        # 3️⃣ Extract title
        title = soup.title.string.strip() if soup.title and soup.title.string else ""

        # 4️⃣ Extract meta description
        desc_tag = soup.find("meta", attrs={"name": "description"})
        description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else ""

        # 5️⃣ Extract top 3 headlines (h1 or h2)
        headlines = []
        for tag in soup.find_all(["h1", "h2"]):
            text = tag.get_text(strip=True)
            if text:
                headlines.append(text)
            if len(headlines) >= 3:
                break

        # 6️⃣ Log and return
        logger.info("scraped page", extra={"url": url, "title": title})
        return {
            "url": url,
            "title": title,
            "description": description,
            "headlines": headlines
        }

    except Exception as exc:
        # Handles all network or parsing errors gracefully
        logger.exception("scrape failed")
        return {"url": url, "title": "", "description": "", "headlines": [], "error": str(exc)}
