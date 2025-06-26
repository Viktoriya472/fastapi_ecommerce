from fastapi import APIRouter, status, Depends, HTTPException
from app.backend.db_depends import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import insert, select, update
from app.schemas import CreateProduct
from app.models.products import Product
from app.models.category import Category
from slugify import slugify


router = APIRouter(prefix='/products', tags=['product'])


@router.get('/')
async def all_products(db: Annotated[Session, Depends(get_db)]):
    products = db.scalars(select(Product).join(Category).where(
        Product.is_active == True,
        Category.is_active == True,
        Product.stock > 0)).all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no products"
        )
    return products


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(db: Annotated[Session, Depends(get_db)],
                         create_product: CreateProduct):
    category = db.scalar(select(Category).where(
        Category.id == create_product.category))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'
        )
    db.execute(insert(Product).values(
        name=create_product.name,
        slug=slugify(create_product.name),
        description=create_product.description,
        price=(create_product.price),
        image_url=create_product.image_url,
        category_id=create_product.category,
        rating=0.0,
        stock=create_product.stock
    ))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.get('/{category_slug}')
async def product_by_category(db: Annotated[Session, Depends(get_db)], category_slug: str):
    category = db.scalar(select(Category).where(Category.slug == category_slug))
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Category not found'
        )
    subcategories = db.scalars(select(Category).where(Category.parent_id == category.id)).all()
    list_categories = [category.id] + [i.id for i in subcategories]
    products_category = db.scalars(select(Product).where(
        Product.category_id.in_(list_categories),
        Product.is_active == True,
        Product.stock > 0)).all()
    return products_category


@router.get('/detail/{product_slug}')
async def product_detail(db: Annotated[Session, Depends(get_db)], product_slug: str):
    product = db.scalar(select(Product).where(
        Product.slug == product_slug,
        Product.is_active == True,
        Product.stock > 0))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no product'
        )
    return product


@router.put('/{product_slug}')
async def update_product(db: Annotated[Session, Depends(get_db)],
                         product_slug: str, update_product: CreateProduct):
    product = db.scalar(select(Product).where(Product.slug == product_slug))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no product found'
        )
    category = db.scalar(select(Category).where(Category.id == update_product.category))
    if category is None:
        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'
        )
    db.execute(update(Product).where(Product.slug == product_slug).values(
        name=update_product.name,
        slug=slugify(update_product.name),
        description=update_product.description,
        price=(update_product.price),
        image_url=update_product.image_url,
        category_id=update_product.category,
        stock=create_product.stock
    ))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product update is succesful'
    }


@router.delete('/{product_slug}')
async def delete_product(db: Annotated[Session, Depends(get_db)], product_slug: str):
    product = db.scalar(select(Product).where(Product.slug == product_slug,
                                              Product.is_active == True))
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There is no product found"
        )
    db.execute(update(Product).where(Product.slug == product_slug).values(
        is_active=False))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Product delete is successful'
    }
