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
	
	if not data:
		raise HTTPException(status_code = 404)


	return {"id": data["ProductID"], "name": data["ProductName"]}



@app.get("/employees", status_code = 200)
async def employees_view(limit: int = 0, offset: int = 0, order: str = "EmployeeID"):
	app.db_connection.row_factory = sqlite3.Row
	em_limit = limit
	em_offset = offset
	em_order = order
	order_list = ["first_name", "last_name", "city", "EmployeeID"]
	if em_order not in order_list:
		raise HTTPException(status_code = 400)
	if em_order != "EmployeeID":
		em_order = em_order.title().replace("_", "")
	data = app.db_connection.execute(
		f"SELECT EmployeeID, LastName, FirstName, City From Employees ORDER BY {em_order} LIMIT {em_limit} OFFSET {em_offset}").fetchall()

	return {"employees": [{"id": x["EmployeeID"], "last_name": x["LastName"], "first_name": x["FirstName"], "city": x["City"]} for x in data]}



@app.get("/products_extended", status_code = 200)
async def product_view():
	app.db_connection.row_factory = sqlite3.Row
	data = app.db_connection.execute('''
		SELECT  Products.ProductID, Products.ProductName, Categories.CategoryName, Suppliers.CompanyName
		FROM Products JOIN Categories ON Products.CategoryID = Categories.CategoryID
		JOIN Suppliers ON Products.SupplierID = Suppliers.SupplierID
		ORDER BY Products.ProductID;
		''').fetchall()

	return {"products_extended": [{"id": x['ProductID'], "name": x["ProductName"], "category": x["CategoryName"], "supplier": x["CompanyName"]} for x in data]}


@app.get("/products/{id}/orders", status_code=200)
async def orders_view(id: int):
	app.db_connection.row_factory = sqlite3.Row
	data = app.db_connection.execute(
		"""
		SELECT Orders.OrderID, Customers.CompanyName, `Order Details`.Quantity, `Order Details`.UnitPrice, `Order Details`.Discount
		FROM Orders JOIN  Customers ON Orders.CustomerID = Customers.CustomerID
		JOIN `Order Details` ON Orders.OrderID = `Order Details`.OrderID
		WHERE Orders.OrderID = :id
		ORDER BY Orders.OrderID
		""",
		{"id": id},
	).fetchall()

	if not data:
		raise HTTPException(status_code=404)

	total_price_list = []
	for x in data:
		t_price = (x["UnitPrice"] * x["Quantity"]) - (x["Discount"] * (x["UnitPrice"] * x["Quantity"]))
		total_price = round(t_price,2)
		total_price_list.append(total_price)

	return {
		"orders": [
			{
				"id": x["OrderID"],
				"customer": x["CompanyName"],
				"quantity": x["Quantity"],
				"total_price": total_price_list[i],
			}
			for i, x in enumerate(data)
		]
	}

