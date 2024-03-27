from jwt import decode_token
from db import get_user
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

"""
Validates age

@type role: str
@param role: Age in string format to be checked
@rtype: Boolean
@returns: True -> Age is valid, False -> Age is not valid

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""


def validate_age(age):
    try:
        if not age.isdigit():
            return False

        num_age = int(age)

        if num_age < 0 or num_age > 150:
            return False

        return True

    except Exception as e:
        print(e)
        return False
