from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from app.models.base import TimestampMixin
from app.models.department import Department

class Rule(TimestampMixin, table=True):
    __tablename__ = "rules"

    id: Optional[int] = Field(default=None, primary_key=True)

    extension: Optional[str] = None   # eg: .pdf etc..
    keyword: Optional[str] = None     # eg: facture etc..

    department_id: int = Field(foreign_key="departments.id")

    department: Optional[Department] = Relationship()