"""
Anakin AI integration module.
This module sends product data to a custom Anakin Quick App for AI-powered analysis.
Note: Requires an Anakin Pro plan for live API access.
"""
from dotenv import load_dotenv
import requests
import os

load_dotenv()

ANAKIN_API_KEY = os.getenv("ANAKIN_API_KEY")
ANAKIN_APP_ID = os.getenv("ANAKIN_APP_ID")

def analyze_with_anakin(product_summary: str) -> str:
    """
    Sends scraped product data to an Anakin Quick App for AI analysis
    and returns a recommendation.
    """
    url = f"https://api.anakin.ai/v1/quickapps/{ANAKIN_APP_ID}/runs"
    headers = {
        "Authorization": f"Bearer {ANAKIN_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {"inputs": {"Inputs1": product_summary}}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        return f"Anakin API error: {e}"
    except requests.exceptions.RequestException as e:
        return f"Anakin connection error: {e}"