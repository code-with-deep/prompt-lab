import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask settings
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not DEBUG and not SECRET_KEY:
        raise ValueError("SECRET_KEY is not set in production environment.")
    if DEBUG and not SECRET_KEY:
        SECRET_KEY = 'dev-secret-key-for-development-only'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Database: Read from env for production (e.g. PostgreSQL on Render),
    # fall back to SQLite for local development
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///playground.db')

    # LLM API Key (Groq only)
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')

    # Default LLM parameters
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_TOKENS = 1024
    DEFAULT_TOP_P = 0.9

    # Port
    PORT = int(os.getenv('PORT', 5000))