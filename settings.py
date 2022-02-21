import os
from dotenv import load_dotenv
load_dotenv()

#  Environment variables
TOKEN = os.getenv("TOKEN")
DATA_CHANNEL_ID = int(os.getenv("DATA_CHANNEL_ID"))

#  Bot settings
ACTIVATION_WORD = "sr! "
ACTIVATION_SYMBOL = "!"
STARTUP_MESSAGE = "No Fear! Sr.Engenheiro here!"
MAX_RECORD_FILES = 500
ALLOWED_NOTE_CHARACTERS = 240