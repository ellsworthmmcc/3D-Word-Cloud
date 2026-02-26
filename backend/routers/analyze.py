from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import JSON, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.models import models
from backend.database.database import get_db
from backend.schemas.schemas import ArticleCreate, ArticleResponse
from backend.scraper.url_processor import url_processor


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

    article_analysis = await url_processor(url=article.url)
    if article_analysis is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article unable to be processed"
        )

    new_article = models.Article(
        url=article.url,
        article_analysis=article_analysis,
    )
    db.add(new_article)
    await db.commit()
    await db.refresh(new_article)
    return new_article


@router.get(
  "",
  response_model=list[int],
)
async def get_article_analysis_ids(
  db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(models.Article.id)
        .order_by(models.Article.date_created),
    )
    article = result.scalars().all()
    return article


@router.get(
  "/{article_id}",
  response_model=ArticleResponse,
)
async def get_article_analysis(
  article_id: int,
  db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(models.Article)
        .where(models.Article.id == article_id)
    )
    article = result.scalars().first()
    if article:
        return article
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Article not found"
    )


@router.patch(
  "/{article_id}",
  response_model=ArticleResponse,
)
async def update_article_analysis(
  article_id: int,
  db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(models.Article)
        .where(models.Article.id == article_id)
    )
    article = result.scalars().first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found"
        )
    
    article_analysis = await url_processor(url=article.url)
    if article_analysis is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article unable to be processed"
        )
    
    article.article_analysis = article_analysis

    await db.commit()
    await db.refresh(article)
    return article


@router.delete(
  "/{article_id}",
  status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_article_analysis(
  article_id: int,
  db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(models.Article)
        .where(models.Article.id == article_id)
    )
    article = result.scalars().first()
    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    await db.delete(article)
    await db.commit()
