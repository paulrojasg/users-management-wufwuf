from pydantic import BaseModel


"""
Schema used for validating login data

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""
class LoginDataSchema(BaseModel):
    username: str
    password: str


"""
Schema used for validating creating user form

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""
class CreateUserSchema(BaseModel):
    username: str
    email: str
    password: str
    age: str | None
    name: str | None
    lastname: str | None
    role: str


"""
Schema used for validating edit user form

@author: Paul Rodrigo Rojas G. (paul.rojas@correounivalle.edu.co)
"""
class EditUserSchema(BaseModel):
    username: str
    email: str
    password: str
    age: str | None
    name: str | None
    lastname: str | None
    role: str