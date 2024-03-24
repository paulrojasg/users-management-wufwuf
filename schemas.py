from pydantic import BaseModel
from typing import Annotated
from fastapi import Form

class LoginDataSchema(BaseModel):
    username: str
    password: str