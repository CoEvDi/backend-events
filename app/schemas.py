from pydantic import BaseModel
from typing import Optional


class InputEvent(BaseModel):
    title: str
    preview: str
    description: str
    start_date: str
    end_date: str
    start_time: str
    end_time: str
    location: str
    site_link: str
    additional_info: str
    guests_info: str

class EditedEvent(BaseModel):
    title: Optional[str] = None
    preview: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    location: Optional[str] = None
    site_link: Optional[str] = None
    additional_info: Optional[str] = None
    guests_info: Optional[str] = None
