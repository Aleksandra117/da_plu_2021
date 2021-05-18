from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy import func

import models
import schemas


def get_shippers(db: Session):
    return db.query(models.Shipper).all()


def get_shipper(db: Session, shipper_id: int):
    return (
        db.query(models.Shipper).filter(models.Shipper.ShipperID == shipper_id).first()
    )

def get_suppliers(db: Session):
    return db.query(models.Supplier).all()

def get_supplier(db: Session, supplier_id: int):
    return (        
        db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id).first()
    )

def get_supplier_and_products(db: Session, supplier_id: int):
	return (
		db.query(models.Product).filter(models.Product.SupplierID == supplier_id).order_by(desc(models.Product.ProductID)).all()
	)

def get_categories(db: Session):
	return db.query(models.Category).all()

def create_supplier(db: Session, supplier_from_msg: schemas.SupplierCreate):
    max_id = db.query(func.max(models.Supplier.SupplierID)).scalar()
    supplier_from_msg.SupplierID = max_id + 1
    db_sup_from_msg = models.Supplier(**supplier_from_msg.dict())
    db.add(db_sup_from_msg)
    db.commit()
    db.refresh(db_sup_from_msg)
    return get_supplier(db, supplier_from_msg.SupplierID)

