import string
import random

LETTERS = string.ascii_letters
NUMBERS = string.digits
PUNCTUATION = string.punctuation

def get_password_length():
    '''Получаем желаемую длину пароля'''
    length = input("How long do you want your password: ")
    return int(length)

def generate_password(length = 8):
    printable = f'{LETTERS}{NUMBERS}{PUNCTUATION}'
    printable = list(printable)
    random.shuffle(printable)

    random_pass = random.choices(printable, k=length)
    return ''.join(random_pass)

if __name__ == '__main__':
    print(generate_password(get_password_length()))
