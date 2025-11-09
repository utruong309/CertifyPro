from pydantic import BaseModel, EmailStr
from datetime import date

class CertificationBase(BaseModel):
    type: str
    number: str
    issue_date: date
    expiry_date: date
    state: str
    user_id: int     # link to User


class CertificationCreate(CertificationBase):
    pass

class CertificationUpdate(BaseModel):
    type: str | None = None
    number: str | None = None
    issue_date: date | None = None
    expiry_date: date | None = None
    state: str | None = None


class CertificationResponse(CertificationBase):
    id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str
    department: str | None = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True