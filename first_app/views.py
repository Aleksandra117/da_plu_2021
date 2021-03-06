from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import PositiveInt
from sqlalchemy.orm import Session

import crud, schemas, models
from database import get_db

router = APIRouter()


@router.get("/shippers/{shipper_id}", response_model=schemas.Shipper)
async def get_shipper(shipper_id: PositiveInt, db: Session = Depends(get_db)):
    db_shipper = crud.get_shipper(db, shipper_id)
    if db_shipper is None:
        raise HTTPException(status_code=404, detail="Shipper not found")
    return db_shipper


@router.get("/shippers", response_model=List[schemas.Shipper])
async def get_shippers(db: Session = Depends(get_db)):
    return crud.get_shippers(db)


@router.get("/suppliers", response_model=List[schemas.Supplier])
async def get_suppliers(db: Session = Depends(get_db)):
    return crud.get_suppliers(db)


@router.get("/suppliers/{supplier_id}", response_model=schemas.SupplierExtended)
async def get_supplier(supplier_id: PositiveInt, db: Session = Depends(get_db)):
    db_supplier = crud.get_supplier(db, supplier_id)
    if db_supplier is None:
        raise HTTPException(status_code=404)
    return db_supplier


@router.get("/suppliers/{supplier_id}/products", response_model=List[schemas.SupplierWithProduct], status_code=200)
async def get_supplier_and_products(supplier_id: PositiveInt, db: Session=Depends(get_db)):
    db_supplier = crud.get_supplier_and_products(db, supplier_id)
    if not db_supplier:
        raise HTTPException(status_code=404)
    return db_supplier


@router.get("/categories", response_model = List[schemas.Category], status_code = 200)
async def get_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


@router.post("/suppliers", response_model = schemas.SupplierExtended, status_code = 201)
def create_supplier(supplier_from_msg: schemas.SupplierCreate, db: Session = Depends(get_db)):
    db_created_supplier = crud.create_supplier(db, supplier_from_msg)
    return db_created_supplier


@router.delete("/suppliers/{supplier_id}", status_code = 204)
def delete_supplier(supplier_id = PositiveInt, db: Session=Depends(get_db)):
    s_id = db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id)
    is_id = db.query(s_id.exists()).scalar()
    if not is_id:
        raise HTTPException(404)
    else:
        crud.delete_supplier(db, supplier_id)


