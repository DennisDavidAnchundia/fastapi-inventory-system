from fastapi import FastAPI

from . import models, schemas
from .auth import create_access_token
# from .database import Base, engine, get_db
from .routers import products, sales

# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Inventory System",
    description="API empresarial para gestión de inventario y ventas",
    version="1.0.0",
)

app.include_router(products.router)
app.include_router(sales.router)


@app.get("/")
def root():
    return {"message": "Inventory API running"}


@app.post("/login")
def login(user: schemas.UserLogin):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user:
        db_user = models.User(username=user.username, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    token = create_access_token({"sub": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
