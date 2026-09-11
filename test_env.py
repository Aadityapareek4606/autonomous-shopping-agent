from dotenv import load_dotenv
import os

load_dotenv()

google_key = os.getenv("GOOGLE_API_KEY")
anakin_key = os.getenv("ANAKIN_API_KEY")
anakin_app_id = os.getenv("ANAKIN_APP_ID")

print("GOOGLE_API_KEY loaded:", bool(google_key))
print("ANAKIN_API_KEY loaded:", bool(anakin_key))
print("ANAKIN_APP_ID loaded:", bool(anakin_app_id))