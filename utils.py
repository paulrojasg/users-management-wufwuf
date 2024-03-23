from jwt import decode_token
from db import get_user


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