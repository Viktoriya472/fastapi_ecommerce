from pydantic import BaseModel, ConfigDict


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str


class CreateProduct(BaseModel):
    name: str
    description: str
    price: int
    image_url: str
    stock: int
    category: int


class CreateCategory(BaseModel):
    name: str
    parent_id: int | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "String",
                "parent_id": None,
            }
        }
    )
