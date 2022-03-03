from pydantic import BaseModel


class News(BaseModel):
    title: str
    content: str
    link: str
    date: str
