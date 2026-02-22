from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from app.models.base import TimestampMixin

class FileLog(TimestampMixin, table=True):
    __tablename__ = "file_logs"

    id: Optional[int] = Field(default=None, primary_key=True)

    filename: str
    source_path: str
    destination_path: Optional[str] = None

    status: str  # SUCCESS / FAILED
    error_message: Optional[str] = None

    processed_at: datetime = Field(default_factory=datetime.utcnow)