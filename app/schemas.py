from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int


class ProductResponse(ProductCreate):
    id: int

    class Config:
        orm_mode = True


class SaleCreate(BaseModel):
    product_id: int
    quantity: int


class SaleResponse(SaleCreate):
    id: int

    class Config:
        orm_mode = True
