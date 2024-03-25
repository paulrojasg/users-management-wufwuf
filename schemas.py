from pydantic import BaseModel

class LoginDataSchema(BaseModel):
    username: str
    password: str

class CreateUserSchema(BaseModel):
    username: str
    email: str
    password: str
    age: str | None
    name: str | None
    lastname: str | None
    role: str