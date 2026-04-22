import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database: Use SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///playground.db'
    
    
    GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
    
    # Default LLM parameters
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_TOKENS = 1024
    DEFAULT_TOP_P = 0.9
    
    # Port
    PORT = int(os.getenv('PORT', 5000))