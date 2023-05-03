from string import ascii_letters
import random


def secret_key_generator(length):
    key = list()
    for _ in range(int(length)):
        key.append(random.choice(ascii_letters))
    return ''.join(key)
