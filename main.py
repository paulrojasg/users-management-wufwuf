from typing import Annotated
from fastapi import FastAPI, Form, HTTPException

# Import login and database resources
from db import get_user

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

@type email: str
@param email: Provided email in form
@type password: str
@param password: Provided password in form
@rtype: json response
@returns: Returns message if login was successful

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

@app.post("/")
def login(email: Annotated[str, Form()], password: Annotated[str, Form()]):
    if get_user(email, password):
        return {'msg':'You are in'}
    raise HTTPException(
                status_code=401,
                detail="No matching account was found"
            )