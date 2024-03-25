from jwt import decode_token
from db import get_user
from bcrypt import gensalt, hashpw, checkpw
import re


"""
Checks if user is login using the provided jwt token

@type token: str
@param token: token to be checked
@rtype: dict or None
@returns: dict (user data)-> User login, None-> User is not login

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

def is_login(token):
    if token:
        decoded_data = decode_token(token)
        if decoded_data:
            for key in decoded_data:
                if key == 'username':
                    username = decoded_data['username']
                    user = get_user(username)
                    if user:
                        return user

    return None

"""
Hashes password given by input

@type raw_password: str
@param raw_password: Password to be hashed
@rtype: str
@returns: Hashed password

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

def hash_password(raw_password):
    try:
        bytes = raw_password.encode('utf-8')
        salt = gensalt()

        hash = hashpw(bytes, salt).decode('utf-8')

        return hash

    except Exception:
        return None


"""
Check if given raw guessed password match hashed password

@type guessed_password: str
@param guessed_password: Raw password to be checked
@type hashed_password: str
@param hashed_password: Hashed password
@rtype: Boolean
@returns: True -> passwords match, False -> passwords do not match

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""


def check_password(guessed_password, hashed_password):
    try:
        guessed_bytes = guessed_password.encode('utf-8')
        hash_bytes = hashed_password.encode('utf-8')

        return checkpw(guessed_bytes, hash_bytes)
    except Exception:
        return False


"""
Validates if given email string is valid

@type hashed_password: email
@param hashed_password: email to be checked
@rtype: Boolean
@returns: True -> Email is valid, False -> Email is not valid

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""


def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
        return True

    return False
