from fastapi import FastAPI

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

