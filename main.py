from typing import Annotated
from fastapi import FastAPI, Form, HTTPException, Response, Header
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from schemas import LoginDataSchema

Jinja2_template = Jinja2Templates(directory="templates")

# Import login and database resources
from db import check_credentials

# Import jwt token generation resources
from jwt import create_token, get_token_seconds_exp

# Import utils
from utils import is_login

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
Returns message if user is login. Used for testing

@rtype: json response
@returns: Returns message if login

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

@app.get('/require_login')
def require_login(access_token: Annotated[str | None, Header()] = None):
    if is_login(access_token):
        return {'msg': 'You are login'}
    else:
        return {'msg': 'Not login'}

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
def login(response: Response, data: LoginDataSchema):
    username = data.username
    password = data.password
    user_data = check_credentials(username, password)
    if user_data:

        token = create_token({'username': user_data['username']})
        token_exp_seconds = get_token_seconds_exp()
        response.set_cookie(key="access-token", value=token, max_age=token_exp_seconds)

        # Filter dictionary
        filtered_data = {}
        for key in user_data:
            if key in ('username', 'email', 'name', 'lastname', 'age'):
                filtered_data[key] = user_data[key]

        return filtered_data

    raise HTTPException(
                status_code=401,
                detail="No matching account was found"
            )



"""
Sample Login Form

@rtype: Html response
@returns: Returns html form

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""


@app.get("/login_form", response_class=HTMLResponse)
def get_login_form(request: Request):
    return Jinja2_template.TemplateResponse("index.html",  {"request": request})


"""
Receive sample login form

@type response: Response
@param response: Response object
@type username: str
@param username: Provided username in form
@type password: str
@param password: Provided username in form
@rtype: Html response
@returns: Login credentials validations

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

@app.post("/login_form")
def post_login_form(response: Response, username: Annotated[str, Form()], password: Annotated[str, Form()]):
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