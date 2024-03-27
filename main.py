from typing import Annotated
from fastapi import FastAPI, Form, HTTPException, Response, Header
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from schemas import LoginDataSchema, CreateUserSchema, EditUserSchema, DeleteUserSchema

Jinja2_template = Jinja2Templates(directory="templates")

# Import login and database resources
from db import check_credentials, check_role_permission, create_user, hash_password
from db import edit_user, get_user, delete_user

# Import jwt token generation resources
from jwt import create_token, get_token_seconds_exp

# Import utils
from utils import is_login, validate_email, validate_role, validate_age

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

@type data: Pydantic schema
@param data: LoginDataSchema
@rtype: json response
@returns: Returns message if login was successful

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

@app.post("/")
def login_request(response: Response, data: LoginDataSchema):
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
Creates user

@type data: Pydantic schema
@param data: CreateUserSchema
@type token: str
@param token: jwt token
@rtype: http response
@returns: Tells if creation was successful

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

@app.post("/create/user", status_code=201)
def create_user_request(data: CreateUserSchema, token: Annotated[str | None, Header()] = None):
    current_user = is_login(token)

    # Checks login
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    forbidden_exc = HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    # Checks create_user permission
    if not check_role_permission(current_user['role'], ['create_user']):
        raise forbidden_exc

    target_role = data.role

    if not validate_role(target_role):
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )


    # Checks create_user permission for specific role
    if not check_role_permission(current_user['role'], [f'create_{target_role}_user']):
        raise forbidden_exc


    # Checks email format
    if not validate_email(data.email):
        raise HTTPException(
            status_code=400,
            detail="Invalid email"
        )

    if not validate_age(data.age):
        raise HTTPException(
                status_code=400,
                detail="Invalid age"
            )

    # Encrypts password
    data.password = hash_password(data.password)

    if not data.password:
        raise HTTPException(
            status_code=400,
            detail="Invalid password"
        )

    result = create_user(data.model_dump())['status']

    if result  == 'success':
        return {'msg':'User created successfully'}
    elif result == 'username':
        raise HTTPException(
            status_code=400,
            detail="Username already in use"
        )
    elif result == 'email':
        raise HTTPException(
            status_code=400,
            detail="Email already in use"
        )
    elif result == 'role':
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )


    raise HTTPException(
            status_code=400,
            detail="Something went wrong"
        )


"""
Edit an user's account

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

@app.put("/edit/user", status_code=200)
def edit_user_request(data: EditUserSchema, token: Annotated[str | None, Header()] = None):

    current_user = is_login(token)

    # Checks login
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    forbidden_exc = HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    current_role = current_user['role']

    target_user = get_user(data.username)

    # Checks edit_user permission
    if not check_role_permission(current_role, ['edit_user']):
        raise forbidden_exc

    target_role = data.role

    if not validate_role(target_role):
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    if current_user['username'] == data.username:
        # User editing itself
        if not check_role_permission(current_role, ['edit_own_user']):
            raise forbidden_exc

        if target_role != current_user['role']:
            raise HTTPException(
                status_code=403,
                detail="You cannot change your own role"
            )
    else:
        # User editing someone else's account

        if target_user:

            current_target_user_role = target_user['role']


            if not check_role_permission(current_role, [f'edit_{current_target_user_role}_user']):
                raise forbidden_exc

            # User changing another user's role
            if current_target_user_role != target_role:
                if not check_role_permission(current_role, [f'grant_{target_role}_role']):
                    raise forbidden_exc

        else:
            raise HTTPException(
                status_code=401,
                detail="That user does not exist"
            )


    # Checks if email will be changed
    current_target_user_email = target_user['email']
    if current_target_user_email != data.email:
        if not validate_email(current_target_user_email):
            raise HTTPException(
                status_code=400,
                detail="Invalid email"
            )
    else:
        data.email = None

    if not validate_age(data.age):
        raise HTTPException(
                status_code=400,
                detail="Invalid age"
            )

    # Checks if new password is set
    password = data.password
    if password == "":
        data.password = None
    else:
        data.password = hash_password(password)

    result = edit_user(data.model_dump())['status']

    if result  == 'success':
        return {'msg':'User updated successfully'}
    elif result == 'username':
        raise HTTPException(
            status_code=400,
            detail="Could not find user"
        )
    elif result == 'email':
        raise HTTPException(
            status_code=400,
            detail="Email already in use"
        )
    elif result == 'role':
        raise HTTPException(
            status_code=400,
            detail="Invalid role"
        )

    raise HTTPException(
            status_code=400,
            detail="Something went wrong"
        )


"""
Deletes an user account

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

@app.delete("/delete/user", status_code=200)
def delete_user_request(data: DeleteUserSchema, token: Annotated[str | None, Header()] = None):
    current_user = is_login(token)

    # Checks login
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    forbidden_exc = HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    current_role = current_user['role']

    # Checks delete_user permission
    if not check_role_permission(current_role, ['delete_user']):
        raise forbidden_exc

    target_user = get_user(data.username)

    # Trying to delete own account
    if data.username == current_user['username']:
        if not check_role_permission(current_role, ['delete_own_user']):
            raise forbidden_exc
    else:
        # Trying to delete accont of someone else
        if target_user:
            current_target_user_role = target_user['role']

            if not check_role_permission(current_role, [f'delete_{current_target_user_role}_user']):
                raise forbidden_exc

        else:
            raise HTTPException(
                status_code=401,
                detail="That user does not exist"
            )

    result = delete_user(target_user['username'])['status']

    if result  == 'success':
        return {'msg':'User deleted successfully'}
    elif result == 'username':
        raise HTTPException(
            status_code=400,
            detail="Could not find user"
        )

    raise HTTPException(
            status_code=400,
            detail="Something went wrong"
        )

"""
Checks if login user has some certain permissions

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""

@app.get("/check/role/permission", status_code=200)
def check_permission_request(token: Annotated[str | None, Header()] = None):
    pass


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