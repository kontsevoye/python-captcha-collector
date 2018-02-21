from re import match
from shutil import move
from settings import SUCCESS_CAPTCHAS_DIR
import os

def valid_code(code):
    return match(r"[0-9]{5}$", code)

def valid_picture(picture):
    return True

def move_picture(pic, code):
    current_path = os.getcwd()
    abs_path = "{}/{}".format(os.getcwd(), SUCCESS_CAPTCHAS_DIR)
    if not os.path.exists(abs_path):
        os.makedirs(abs_path)

    move(pic, "{}/{}.jpeg".format(SUCCESS_CAPTCHAS_DIR, code))
