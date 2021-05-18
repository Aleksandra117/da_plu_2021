from sqlalchemy.orm import Session
from sqlalchemy import desc

import models


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

