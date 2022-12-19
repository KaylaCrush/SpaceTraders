import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("USERNAME")
TOKEN = os.getenv("TOKEN")
IMAGE_FOLDER = os.getenv("IMAGE_FOLDER")
