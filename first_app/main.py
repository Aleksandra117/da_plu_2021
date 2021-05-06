import sqlite3
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.on_event("startup")
async def startup():
	app.db_connection = sqlite3.connect("northwind.db")
	app.db_connection.text_factory = lambda b: b.decode(errors="ignore")  # northwind specific 


@app.on_event("shutdown")
async def shutdown():
	app.db_connection.close()



@app.get("/categories", status_code = 200)
async def categories_view():
	app.db_connection.row_factory = sqlite3.Row
	data = app.db_connection.execute(
		"SELECT CategoryID, CategoryName FROM Categories ORDER BY CategoryID").fetchall()

	return {"categories": [{"id": x['CategoryID'], "name": x["CategoryName"]} for x in data]}


@app.get("/customers", status_code = 200)
async def customers_view():
	app.db_connection.row_factory = sqlite3.Row
	data = app.db_connection.execute(
		"SELECT CustomerID, CompanyName, Address, PostalCode, City, Country From Customers ORDER BY CustomerID").fetchall()

	return {"customers": [{"id": x['CustomerID'], "name": x["CompanyName"], "full_address": f"{x['Address']} {x['PostalCode']} {x['City']} {x['Country']}"} for x in data]}


@app.get("/products/{products_id}")
async def single_product(products_id: int):
	app.db_connection.row_factory = sqlite3.Row
	data = app.db_connection.execute(
		"SELECT ProductID, ProductName FROM Products WHERE ProductID = :products_id",
		{'products_id': products_id}).fetchone()
	print(data[1])
	print(data['ProductName'])
	
	if not data:
		raise HTTPException(status_code = 404)


	return {"id": data["ProductID"], "name": data["ProductName"]}
