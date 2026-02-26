from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ArticleBase(BaseModel):
    url: str = Field(min_length=1, max_length=150)


class ArticleCreate(ArticleBase):
    pass


class ArticleResponse(ArticleBase):
    model_config = ConfigDict(from_attributes=True)

    url: str
    date_posted: datetime
