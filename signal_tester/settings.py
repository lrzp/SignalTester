import os

from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Absolute direction of an application
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SQLite specific variables
SQLITE_DB_FILE = os.path.join(BASE_DIR, os.environ.get('SQLITE_DB_FILE'))
DB_INPUT_TABLE = os.environ.get('DB_INPUT_TABLE')
DB_OUTPUT_TABLE = os.environ.get('DB_OUTPUT_TABLE')
