import random
import string

def generate_username(first_name):
    # Generate a base username from the first name
    base_username = first_name.lower().replace(' ', '_')

    # Append a random 4-digit number to the base username
    random_digits = ''.join(random.choices(string.digits, k=4))
    username = f"{base_username}{random_digits}"

    return username


def generate_otp( number = 6 ):
    # Generate a unique alphanumeric 6-digit code
    return ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=number))