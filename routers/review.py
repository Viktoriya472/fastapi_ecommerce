from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, func
from app.backend.db_depends import get_db
from app.models.review import Review
from app.models.products import Product
from app.schemas import CreateReview
from app.routers.auth import get_current_user


router = APIRouter(prefix='/reviews', tags=['review'])


@router.get('/')
async def all_reviews(db: Annotated[AsyncSession, Depends(get_db)]):
    review = await db.scalars(select(Review).where(
        Review.is_active == True))
    return review.all()


@router.get('/{product_id}')
async def products_reviews(db: Annotated[AsyncSession, Depends(get_db)],
                           product_id: int):
    product = await db.scalar(select(Product).where(
        Product.id == product_id,
        Product.is_active == True))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product found'
        )
    review = await db.scalars(select(Review).where(
        Review.product_id == product_id, Review.is_active == True))
    return review.all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_review(db: Annotated[AsyncSession, Depends(get_db)],
                     create_review: CreateReview,
                     get_user: Annotated[dict, Depends(get_current_user)]):
    if not get_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You must be auth user for this'
        )
    else:
        product = await db.scalar(select(Product).where(
            Product.id == create_review.product_id))
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no product found'
            )
        await db.execute(insert(Review).values(
                comment=create_review.comment,
                grade=create_review.grade,
                product_id=create_review.product_id,
                user_id=get_user.get('id'),
            ))
        review_grade = await db.scalar(select(func.avg(Review.grade)).where(
            Review.product_id == create_review.product_id))
        product.rating = round(review_grade, 1)
        await db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
        }


@router.post('/{review_id}')
async def delete_reviews(db: Annotated[AsyncSession, Depends(get_db)],
                         review_id: int,
                         get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.get('is_admin'):
        review = await db.scalar(select(Review).where(
            Review.id == review_id, Review.is_active == True))
        if review is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='There is no category found'
            )
        await db.execute(update(Review).where(
            Review.id == review_id).values(is_active=False))
        await db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Review delete is successful'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='You must be admin user for this'
        )
