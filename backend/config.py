# Configuration settings
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DB_PATH = "vault.db"

MAX_UPLOAD_SIZE_MB = 10

ALLOWED_FILE_TYPES = ["image/png", "image/jpeg", "application/pdf"]

RENT_YEARS_DEFAULT = 5
