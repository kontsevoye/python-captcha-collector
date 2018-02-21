from dotenv import load_dotenv
from os.path import join, dirname
from flask import Flask
import os

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path, verbose=True)

LOGIN = os.environ.get("LOGIN")
PAS = os.environ.get("PAS")
COOKIE_KEY = os.environ.get("COOKIE_KEY")
TEST_ID = os.environ.get("TEST_ID")
CAPTCHAS_DIR = os.environ.get("CAPTCHAS_DIR")
SUCCESS_CAPTCHAS_DIR = os.environ.get("SUCCESS_CAPTCHAS_DIR")
APP_NAME = os.environ.get("APP_NAME")

app = Flask(APP_NAME)
