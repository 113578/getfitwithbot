import os
from dotenv import load_dotenv


load_dotenv()


PYTHONPATH = os.getenv('PYTHONPATH')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENWEATHERMAP_TOKEN = os.getenv('OPENWEATHERMAP_TOKEN')
NUTRITIONIX_ID = os.getenv('NUTRITIONIX_ID')
NUTRITIONIX_TOKEN = os.getenv('NUTRITIONIX_TOKEN')
APININJAS_TOKEN = os.getenv('APININJAS_TOKEN')
