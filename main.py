from fastapi import FastAPI
from app.routers import category, products, review, permission, auth


app = FastAPI()
app.include_router(auth.router)


@app.get('/')
async def welcome() -> dict:
    return {'message': 'My e-commerce app'}


app.include_router(category.router)
app.include_router(products.router)
app.include_router(permission.router)
app.include_router(review.router)
