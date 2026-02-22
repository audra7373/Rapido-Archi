from sqlmodel import SQLModel, Field
from typing import Optional
from app.models.base import TimestampMixin



class Users(TimestampMixin, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name : str = Field(index=True, unique=True)
    password_hash:str
    role : str =Field(default="user") # user or admin
    