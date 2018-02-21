import requests
import re
import os
import imghdr
import hashlib
import string
from random import randint, choice
from settings import TEST_ID, CAPTCHAS_DIR

class IqException(Exception):
    """Base exception class in this module."""
    pass

class AuthError(IqException):
    """Auth exceptions in this module."""
    pass

class CaptchaError(IqException):
    """Captcha exceptions in this module."""
    pass

class LogoutError(IqException):
    """Logout exceptions in this module."""
    pass

class RegisterError(IqException):
    """Register exceptions in this module."""
    pass

class Iq:
    def __init__(self, login="", pas="", cookie=""):
        self.test_id = TEST_ID
        self.captchas_dir = CAPTCHAS_DIR
        self.authenticated = False
        self.login = login
        self.pas = pas
        self.pas = cookie
        self.session = requests.Session()

    def auth(self):
        if self.login == "" or self.pas == "":
            r = self.register(random=True)
        else:
            r = self.session.post("http://iq.karelia.ru/index.php",
                data={'login': self.login, 'pas': self.pas})
            regex = r"{}".format(self.login)
            matches = re.findall(regex, r.text)
            if len(matches) != 2:
                raise AuthError('shit in auth')
            # print('auth success')
            self.authenticated = True

        if self.is_account_locked(r.text):
            # print('acc locked')
            self.logout()
            r = self.register(random=True)
        # else:
            # print('acc normal')
        return r

    def logout(self):
        r = self.session.get("http://iq.karelia.ru/index.php?logout=1")
        if self.is_unauthorized(r.text):
            # print('logout complete')
            self.authenticated = False
        else:
            # print('logout failed')
            raise CaptchaError('shit in logout')

    def __random_generator(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(choice(chars) for x in range(size))

    def __generate_person(self):
        name = "{} {} {}".format(self.__random_generator(6, string.ascii_uppercase), self.__random_generator(6, string.ascii_uppercase), self.__random_generator(6, string.ascii_uppercase))
        login = self.__random_generator(15, string.ascii_uppercase)
        pas = self.__random_generator(15)
        #return {"name": name, "login": login, "pas": pas}
        return name, login, pas

    def register(self, login="", name="", pas="", random=True):
        if random == True or (login == "" or name == "" or pas == ""):
            name, login, pas = self.__generate_person()
            # print("name, login, pas", name, login, pas)

        r = self.session.get("http://iq.karelia.ru/register.php")
        regex = r"agreement.*value=.(\d+)."
        matches = re.findall(regex, r.text)
        # print(matches)
        if len(matches) != 1:
            raise RegisterError('shit in register')
        
        agreement = matches[0]
        r = self.session.post("http://iq.karelia.ru/register.php",
            data={'agreement': agreement, "name": name, "login": login, "pas": pas, "pas1": pas, "subm": "Зарегистрироваться"})
        
        # print(r.text)
        if self.is_authorized(r.text, login):
            # print('krasivo zaregalsya')
            self.login = login
            self.pas = pas
            self.authenticated = True
            return r
        else:
            raise RegisterError('shit in register #2')

    def get_captcha_link(self):
        if not self.authenticated:
            self.auth()

        r = self.session.get("http://iq.karelia.ru/enter.php?t_id={}".format(self.test_id))
        regex = r"code.php.[0-9]*"
        matches = re.findall(regex, r.text)
        if len(matches) != 1:
            raise CaptchaError('shit in get_captcha_link')
        # print('get_captcha_link success')
        captcha_link = matches[0]
        # print(captcha_link)
        return captcha_link

    def __calculate_hash(self, content):
        h = hashlib.sha256()
        h.update(content)
        return h.hexdigest()

    def get_captcha(self):
        captcha_link = self.get_captcha_link()

        r = self.session.get("http://iq.karelia.ru/{}".format(captcha_link))
        current_path = os.getcwd()
        abs_captchas_path = "{}/{}".format(os.getcwd(), self.captchas_dir)
        if not os.path.exists(abs_captchas_path):
            os.makedirs(abs_captchas_path)

        pic_hash = self.__calculate_hash(r.content)
        abs_pic_path = "{}/{}.jpeg".format(abs_captchas_path, pic_hash)
        rel_pic_path = "{}/{}.jpeg".format(self.captchas_dir, pic_hash)

        if os.path.isfile(abs_pic_path):
            while True:
                rand = randint(10000, 99999999)
                abs_pic_path = "{}/{}{}.jpeg".format(abs_captchas_path, pic_hash, rand)
                rel_pic_path = "{}/{}{}.jpeg".format(self.captchas_dir, pic_hash, rand)
                if not os.path.isfile(abs_pic_path):
                    break        

        with open(abs_pic_path, 'wb') as f:
            f.write(r.content)

        if imghdr.what(abs_pic_path) != 'jpeg':
            raise CaptchaError('shit in get_captcha')

        # print('get_captcha success')
        # print(rel_pic_path)
        return rel_pic_path

    def valid_code(self, code):
        r = self.session.post("http://iq.karelia.ru/enter.php?t_id={}".format(self.test_id),
            data={'code': code})
        regex = r"check2click"
        matches = re.findall(regex, r.text)
        # print(matches)
        # print(r.text)
        if len(matches) == 2:
            return True
        else:
            return False

    def is_account_locked(self, page):
        regex = r"доступ ограничен"
        matches = re.findall(regex, page)
        # print(matches)
        if len(matches) > 0:
            return True
        else:
            return False

    def is_unauthorized(self, page):
        regex = r"доступ после авторизации"
        matches = re.findall(regex, page)
        # print(matches)
        if len(matches) > 0:
            return True
        else:
            return False

    def is_authorized(self, page, login):
        regex = r"<font color=green>{}</font".format(login)
        matches = re.findall(regex, page)
        # print(matches)
        if len(matches) > 0:
            return True
        else:
            return False

    def get_cookie(self):
        return self.session.cookies['iq']

    def set_cookie(self, cookie):
        self.session.cookies['iq'] = cookie
