from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
from backend.database import get_db
from backend.schemas import ArticleCreate, ArticleResponse


router = APIRouter()


@router.post(
  "",
  response_model=ArticleResponse,
  status_code=status.HTTP_201_CREATED,
)
async def analyze_article(
  article: ArticleCreate,
  db: Annotated[AsyncSession, Depends(get_db)]
):
    # TODO
    # add URL cleaning
    result = await db.execute(
        select(models.Article).where(models.Article.url == article.url),
    )
    existing_article = result.scalars().first()
    if existing_article:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article already processed",
        )

    # TODO
    # scrap article, process it, save alongside article,
    # return that information instead

    new_article = models.Article(
        url=article.url,
    )
    db.add(new_article)
    await db.commit()
    await db.refresh(new_article)
    return new_article
