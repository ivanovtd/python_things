import string
import random
import argparse
LETTERS = string.ascii_letters
NUMBERS = string.digits
PUNCTUATION = string.punctuation


def generate_password(length: int, is_use_punctuation_symbols: bool) -> str:
    printable = f'{LETTERS}{NUMBERS}{PUNCTUATION}' if is_use_punctuation_symbols else f'{LETTERS}{NUMBERS}' 
    printable = list(printable)
    random.shuffle(printable)

    random_pass = random.choices(printable, k=length)
    return ''.join(random_pass)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Password generator by ivanovtd")
    parser.add_argument("-l", "--length", type=int, help="Enter length of password", default=10)
    parser.add_argument("-s", help="Use special chars",
                        action="store_true")
    args = parser.parse_args()
    print(generate_password(args.length, args.s))
