from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
	return {"message": "Hello world!"}

@app.post('/method', status_code=201)
def method():
	return {"method": "POST"}

@app.get('/method', status_code=200)
def method():
	return {"method": "GET"}