import random
import string


def get_code():
    return random.randint(1000, 9999)


def generate_random_token():
    # Generate a random 6-digit token
    return ''.join(random.choices(string.digits, k=6))
