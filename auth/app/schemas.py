from pydantic import BaseModel, EmailStr
from typing import List, Optional

# --- Esquemas para Roles ---
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True

# --- Esquemas para Usuarios ---
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    roles: List[str] = [] # Al crear un usuario se puede especificar una lista de nombres de roles

class User(UserBase):
    id: int
    is_active: bool
    roles: List[Role] = []

    class Config:
        orm_mode = True

# --- Esquemas para Autenticación (JWT) ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
