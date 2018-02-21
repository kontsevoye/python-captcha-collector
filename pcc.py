from settings import app
from iq import Iq
from flask import request, make_response, render_template, redirect, url_for
from helpers import valid_code, move_picture, valid_picture

@app.route("/")
def index():
    return redirect(url_for('solve'))

@app.route("/solve/<int:success>")
@app.route("/solve")
def solve(success=None):
    iq = Iq()
    picture = iq.get_captcha()

    # print('success', success)

    resp = make_response(render_template('solve.html', picture=picture, success=success))
    resp.set_cookie('iq-login', iq.login)
    resp.set_cookie('iq-pas', iq.pas)
    resp.set_cookie('iq-cook', iq.get_cookie())
    return resp

@app.route("/check", methods=['POST'])
def check():
    login = request.cookies.get('iq-login')
    pas = request.cookies.get('iq-pas')
    cook = request.cookies.get('iq-cook')

    iq = Iq()
    iq.set_cookie(cook)
    iq.login = login
    iq.pas = pas

    if request.method == 'POST':
        code = request.form['code']
        picture = request.form['picture']
        if valid_code(code) and valid_picture(picture):
            if iq.valid_code(code):
                move_picture(picture, code)
                return redirect(url_for('solve', success=1))
            else:
                return redirect(url_for('solve', success=0))
        else:
            return redirect(url_for('solve', success=2))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
