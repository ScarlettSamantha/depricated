from TransHelp import app
from werkzeug.security import generate_password_hash, check_password_hash


def generate_password(passwd: str) -> str:
    return generate_password_hash(password=passwd, method=app.config['SECURITY_PASSWORD_METHOD'],
                                  salt_length=app.config['SECURITY_PASSWORD_SALT_LENGTH'])


def check_password(hash_passwd: str, raw_passwd: str) -> bool:
    return check_password_hash(hash_passwd, raw_passwd)


def get_hash_length() -> int:
    t = 0
    if app.config['SECURITY_PASSWORD_METHOD'] == 'pbkdf2:sha256':
        t += 80
    elif app.config['SECURITY_PASSWORD_METHOD'] == 'pbkdf2:sha512':
        t += 144
    t += app.config['SECURITY_PASSWORD_METHOD'].__len__()
    t += str(app.config['SECURITY_PASSWORD_SALT_LENGTH']).__len__()
    return int(t)
