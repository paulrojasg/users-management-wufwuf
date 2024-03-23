from jose import jwt
from datetime import datetime, timedelta
from db import get_user

#
import random
import string

TOKEN_EXP_SECONDS = 20 # To be put in .env
SECRET_KEY = ''.join(random.choices(string.ascii_uppercase, k=5)) # To be put in .env

"""
Generates jwt token

@type data: dict
@param data: Data to be included in Token
@rtype: str
@returns: Returns jwt token

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

def create_token(data: dict):
    data_token = data.copy()
    data_token["exp"] = datetime.now() + timedelta(seconds=TOKEN_EXP_SECONDS)
    token_jwt = jwt.encode(data_token, key=SECRET_KEY, algorithm="HS256")
    return token_jwt


"""
Retrieves TOKEN_EXP_SECONDS

@rtype: int
@returns: Retrieves token expiration seconds

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

def get_token_seconds_exp():
    return TOKEN_EXP_SECONDS

"""
Checks if given token is valid

@type token: str
@param token: JWT token to be checked
@rtype: boolean
@returns: Returns True if token is valid, returns False if not

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

# def check_login_token(token):
#     try:
#         data_user = jwt.decode(token, key=SECRET_KEY, algorithms=["HS256"])
#         if get_user(data_user["email"], db_users) is None:
#             return RedirectResponse("/", status_code=302)
#         return Jinja2_template.TemplateResponse("dashboard.html", {"request": request})
#     except Exception:
#         pass
#     return Jinja2_template.TemplateResponse("dashboard.html", {"request": request})