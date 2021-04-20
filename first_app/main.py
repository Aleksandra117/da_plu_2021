from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import datetime
from datetime import timedelta
from typing import Optional
from collections import Counter
import string

app = FastAPI()
app.patient_id = 1
app.patients = []

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

polish_letters = ['ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ź', 'ż','Ą', 'Ć', 'Ę', 'Ł', 'Ń', 'Ó', 'Ś', 'Ź', 'Ż']
all_letters = string.ascii_letters
for polish_letter in polish_letters:
	all_letters = all_letters + polish_letter
	
def count_letters(word, valid_letters=all_letters):
    count = Counter(word)
    return sum(count[letter] for letter in valid_letters)

@app.post('/register', status_code=201)
def register_patient(patient: Patient):
	if patient.id is None:
		patient.id = app.patient_id
		app.patient_id +=1

	r_date = datetime.date.today()
	sr_date = r_date.strftime("%Y-%m-%d")
	patient.register_date = sr_date

	ns_length =  count_letters(patient.name) + count_letters(patient.surname)
	date_delta = timedelta(days=+ns_length)
	vac_date = r_date + date_delta
	s_vac_date = vac_date.strftime("%Y-%m-%d")
	patient.vaccination_date = s_vac_date
	app.patients.append(patient)

	return patient 

@app.get('/patient/{patient_id}', status_code=200)
def patient_view(patient_id):
	if int(patient_id) < 1:
		raise HTTPException(status_code = 400)
	for p in app.patients:
		if p.id == int(patient_id):
			return app.patients[p.id-1]
	raise HTTPException(status_code = 404)