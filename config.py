import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Gmail API Configuration
GMAIL_CLIENT_SECRET_FILE = os.getenv('GMAIL_CLIENT_SECRET_FILE')
GMAIL_SCOPES = os.getenv('GMAIL_SCOPES').split(',')

# OpenAI API Key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
