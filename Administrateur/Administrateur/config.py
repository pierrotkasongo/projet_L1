import string
import random

def generate_password():
    characters = list(string.ascii_lowercase)
    random.shuffle(characters)
    password = []
    for i in range(5):
        password.append(random.choice(characters))
    random.shuffle(password)
    return ''.join(password)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'cabmubenesha71@gmail.com'
EMAIL_HOST_PASSWORD = 'wntdovwvjknclufl'
EMAIL_PORT = 587
