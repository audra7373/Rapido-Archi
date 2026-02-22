from sqlmodel import SQLModel, Field
from typing import Optional
from app.models.base import TimestampMixin

class Department(TimestampMixin, table=True):
    
    __tablename__ ="departments"
    
    id: Optional[int] = Field(default=None,primary_key=True)
    name: str =Field(index=True, unique=True)
    target_path: str #chemin du departement
    