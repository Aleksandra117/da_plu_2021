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
    id_free = max_id + 1
    db_sup_from_msg = models.Supplier(SupplierID = id_free, CompanyName = supplier_from_msg.CompanyName, ContactName = supplier_from_msg.ContactName,
        ContactTitle = supplier_from_msg.ContactTitle, Address = supplier_from_msg.Address, City = supplier_from_msg.City, PostalCode = supplier_from_msg.PostalCode,
        Country = supplier_from_msg.Country, Phone = supplier_from_msg.Phone)
        
    db.add(db_sup_from_msg)
    db.commit()
    return db_sup_from_msg

def delete_supplier(db: Session, supplier_id: int):
    db_deleted = db.query(models.Supplier).filter(models.Supplier.SupplierID == supplier_id).delete()
    db.commit()