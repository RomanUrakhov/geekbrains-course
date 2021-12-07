import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

secret_token = os.getenv('SECRET_TOKEN')
