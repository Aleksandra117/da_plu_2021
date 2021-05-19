from pydantic import BaseModel, PositiveInt, constr
from typing import Optional, Any, Union


class Shipper(BaseModel):
    ShipperID: PositiveInt
    CompanyName: constr(max_length=40)
    Phone: constr(max_length=24)

    class Config:
        orm_mode = True


class Supplier(BaseModel): 
    SupplierID: PositiveInt
    CompanyName: constr(max_length=40)

    class Config:
        orm_mode = True


class SupplierExtended(BaseModel): 
    SupplierID: PositiveInt
    CompanyName: constr(max_length=40)
    ContactName: constr(max_length=30)
    ContactTitle: constr(max_length=30)
    Address: constr(max_length=60)
    City: constr(max_length=15)
    Region: Optional[constr(max_length=15)]
    PostalCode: constr(max_length=10)
    Country: constr(max_length=15)
    Phone: constr(max_length=24)
    Fax: Optional[constr(max_length=24)] = None
    HomePage: Optional[str] = None
    class Config:
        orm_mode = True



class SupplierCreate(BaseModel): 
    CompanyName: constr(max_length=40)
    ContactName: Optional[constr(max_length=30)]
    ContactTitle: Optional[constr(max_length=30)]
    Address: Optional[constr(max_length=60)]
    City: Optional[constr(max_length=15)]
    PostalCode: Optional[constr(max_length=10)]
    Country: Optional[constr(max_length=15)]
    Phone: Optional[constr(max_length=24)]
    class Config:
        orm_mode = True



class Category(BaseModel):
    CategoryID: PositiveInt
    CategoryName: Optional[constr(max_length = 15)]

    class Config:
        orm_mode = True


class SupplierWithProduct(BaseModel):
    ProductID: PositiveInt
    ProductName: constr(max_length=40)
    Category: Category
    Discontinued: int

    class Config:
        orm_mode = True


