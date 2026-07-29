from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..dependencies import verify_token

router = APIRouter(prefix="/sales", tags=["Sales"])


@router.post("/", response_model=schemas.SaleResponse)
def create_sale(
    sale: schemas.SaleCreate,
    db: Session = Depends(get_db),
    user=Depends(verify_token),
):
    product = db.query(models.Product).filter(models.Product.id == sale.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < sale.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    product.stock -= sale.quantity
    db_sale = models.Sale(**sale.dict())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale


@router.get("/", response_model=list[schemas.SaleResponse])
def list_sales(db: Session = Depends(get_db)):
    return db.query(models.Sale).all()
