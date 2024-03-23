from typing import Annotated
from fastapi import FastAPI, Form, HTTPException,  Response

# Import login and database resources
from db import check_credentials

# Import jwt token generation resources
from jwt import create_token, get_token_seconds_exp

app = FastAPI()

"""
Returns greeting message. Used for testing

@rtype: json response
@returns: Returns greeting

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

@app.get("/")
def greet():
    return {'msg': 'Welcome'}


"""
Logins user

@type username: str
@param username: Provided username in form
@type password: str
@param password: Provided password in form
@rtype: json response
@returns: Returns message if login was successful

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

@app.post("/")
def login(response: Response, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    user_data = check_credentials(username, password)
    if user_data:

        token = create_token({'username': user_data['username']})
        token_exp_seconds = get_token_seconds_exp()
        response.set_cookie(key="access-token", value=token, max_age=token_exp_seconds)
        return user_data

    raise HTTPException(
                status_code=401,
                detail="No matching account was found"
            )