from dotenv import load_dotenv
import requests
import os

load_dotenv()

api_key = os.getenv("ANAKIN_API_KEY")
app_id = os.getenv("ANAKIN_APP_ID")

url = f"https://api.anakin.ai/v1/quickapps/{app_id}/runs"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "inputs": {
        "Inputs1": "Product: Wireless Bluetooth Earbuds, Price: $29.99, Rating: 4.2 stars, 1500 reviews"
    }
}

response = requests.post(url, headers=headers, json=payload)

print("Status Code:", response.status_code)
print("Response:", response.text)