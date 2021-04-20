from fastapi import FastAPI
from pydantic import BaseModel
import datetime
from datetime import timedelta

app = FastAPI()
app.patient_id = 1

@app.get("/")
def root():
	return {"message": "Hello world!"}

@app.post('/method', status_code=201)
def method():
	return {"method": "POST"}

@app.get('/method', status_code=200)
def method():
	return {"method": "GET"}

@app.put('/method', status_code=200)
def method():
	return {"method": "PUT"}

@app.options('/method', status_code=200)
def method():
	return {"method": "OPTIONS"}

@app.delete('/method', status_code=200)
def method():
	return {"method": "DELETE"}

class Patient(BaseModel):
	id: Optional[int] = None
	name:str
	surname:str
	register_date: Optional[int] = None
	vaccination_date: Optional[int] = None
	
@app.post('/register', status_code=201)
def register_patient(patient: Patient):
	if patient.id is None:
		patient.id = app.patient_id
		app.patient_id +=1

	r_date = datetime.date.today()
	sr_date = r_date.strftime("%Y-%m-%d")
	patient.register_date = sr_date
	
	ns_length = len(patient.name.replace(" ", ""))+len(patient.surname.replace(" ", ""))
	date_delta = timedelta(days=+ns_length)
	vac_date = r_date + date_delta
	s_vac_date = vac_date.strftime("%Y-%m-%d")
	patient.vaccination_date = s_vac_date

	return patient 