from jwt import decode_token
from db import get_user
from bcrypt import gensalt, hashpw, checkpw


"""
Checks if user is login using the provided jwt token

@type token: str
@param token: token to be checked
@rtype: Boolean
@returns: True -> User is login, False -> User is not login

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

def is_login(token):
    decoded_data = decode_token(token)
    if decoded_data:
        for key in decoded_data:
            if key == 'username':
                username = decoded_data['username']
                if get_user(username):
                    return True

    return False
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
