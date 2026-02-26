from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ArticleBase(BaseModel):
    url: str = Field(min_length=1, max_length=2000)


class ArticleCreate(ArticleBase):
    pass


class ArticleResponse(ArticleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    url: str
    article_analysis: dict[str, int]
    date_created: datetime
