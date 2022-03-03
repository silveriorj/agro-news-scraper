from os import link
from pydantic import BaseModel

from datetime import datetime
from typing import List, Optional


class News(BaseModel):
    title: str
    content: str
    link: str
    date: str
