import os
from urllib.parse import quote_plus

# Database configuration
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = quote_plus(os.getenv("POSTGRES_PASSWORD", "yourpassword"))
DB_NAME = os.getenv("POSTGRES_DB", "marketplace_db")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")

SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

# File upload configuration
basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir, "uploads")
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB max upload size
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
