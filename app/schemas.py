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

