"""
Anakin AI (anakin.io) URL Scraper integration.
Uses Anakin's real-time scraping API to fetch clean, structured content
from a product page — used to verify/enrich shopping agent results.
"""
from dotenv import load_dotenv
import requests
import os
import time

load_dotenv()

ANAKIN_API_KEY = os.getenv("ANAKIN_API_KEY")

def scrape_url_with_anakin(url: str) -> str:
    """
    Submits a URL to Anakin's scraper, polls for the result,
    and returns the cleaned markdown content.
    """
    headers = {
        "X-API-Key": ANAKIN_API_KEY,
        "Content-Type": "application/json"
    }

    submit_resp = requests.post(
        "https://api.anakin.io/v1/url-scraper",
        headers=headers,
        json={
            "url": url,
            "country": "in",
            "formats": ["markdown"]
        },
        timeout=15
    )
    
    submit_resp.raise_for_status()
    job_id = submit_resp.json().get("jobId")

    if not job_id:
        return "Error: No job ID returned from Anakin."

    for _ in range(15):
        time.sleep(2)
        poll_resp = requests.get(
            f"https://api.anakin.io/v1/url-scraper/{job_id}",
            headers=headers,
            timeout=15
        )
        poll_resp.raise_for_status()
        data = poll_resp.json()
        if data.get("status") == "completed":
            return data.get("markdown", "No content returned.")
        elif data.get("status") == "failed":
            return f"Anakin scrape failed: {data.get('error')}"

    return "Timed out waiting for Anakin to finish scraping."