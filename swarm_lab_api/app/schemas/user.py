from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    full_name: str  # Agregar el campo de nombre completo

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str