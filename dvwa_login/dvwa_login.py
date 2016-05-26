import requests
import re

loginurl = 'http://127.0.0.1/DVWA/login.php'
session = requests.session()


def get_headers():
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.86 Safari/537.36'
    headers = {'User-Agent': user_agent, 'Referer': 'http://127.0.0.1/DVWA/login.php',
               'Cache-Control': 'max-age=0',
               'Origin': 'http://127.0.0.1',
               'Upgrade-Insecure-Requests': '1',
               'Content-Type': 'application/x-www-form-urlencoded',
               }
    return headers


def get_token():
    index_page = session.get(loginurl, headers=get_headers())
    html = index_page.text
    ma = re.compile("['']\\w{32}[']")
    pa = ma.search(html)
    token = pa.group()
    token = token[1:-1]
    return token


def get_values():
    values = {
        'username': 'admin',
        'password': 'password',
        'Login': 'Login',
        'user_token': get_token(),
    }
    return values


def login():
    login_page = session.post(loginurl, headers=get_headers(), data=get_values())
    html_respon = login_page.text
    ma = re.compile("You have logged in as \'\w*\'")
    pa = ma.search(html_respon)
    try:
        msg = pa.group()
        print(msg)
    except Exception as e:
        print('登录失败')
if __name__ == '__main__':
    login()
