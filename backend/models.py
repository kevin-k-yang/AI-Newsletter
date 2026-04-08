from pydantic import BaseModel
from typing import Literal


class Substory(BaseModel):
    id: str
    title: str
    summary: str
    url: str


class SectionSummary(BaseModel):
    section: Literal["sports", "tech", "finance", "world"]
    summary: str
    substories: list[Substory]


class DailyDigest(BaseModel):
    date: str
    sections: list[SectionSummary]


class Feedback(BaseModel):
    article_id: str
    reaction: Literal["like", "dislike"]
    timestamp: str
