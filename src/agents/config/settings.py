import os

from dotenv import load_dotenv

load_dotenv(override=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") 

if not GOOGLE_API_KEY:
    raise ValueError ("GOOGLE_API_KEY não encontrada no .env")
