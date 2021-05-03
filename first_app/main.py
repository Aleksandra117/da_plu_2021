from fastapi import FastAPI, Request, Response, Cookie, HTTPException, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha256

import datetime
import secrets


app=FastAPI()
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()


login = "4dm1n"
passwd = "NotSoSecurePa$$"
app.session_secret_key = "very constatn and random secret, best 64+ characters"
app.token_secret_key = "another secret also very constant and random and long"
app.session_token = None
app.token = None



@app.get("/hello", response_class=HTMLResponse)
def read_item(request: Request):

	t_date = datetime.date.today()
	today_date = t_date.strftime("%Y-%m-%d")
	return templates.TemplateResponse("index_task1.html.j2", {
		"request": request, "today_date": today_date})




@app.post("/login_session", status_code=201)
def logins(response: Response, credentials: HTTPBasicCredentials = Depends(security)):
	correct_username = secrets.compare_digest(credentials.username, login)
	correct_password = secrets.compare_digest(credentials.password, passwd)
	if (correct_username and correct_password):
		session_token = sha256(f"{correct_username}{correct_password}{app.session_secret_key}".encode()).hexdigest()
		#app.access_tokens.append(session_token)
		app.session_token = session_token
		response.set_cookie(key="session_token", value=session_token)
	else:
		raise HTTPException(status_code=401)



@app.post("/login_token", status_code=201)
def logint(credentials: HTTPBasicCredentials = Depends(security)):
	correct_username = secrets.compare_digest(credentials.username, login)
	correct_password = secrets.compare_digest(credentials.password, passwd)
	if (correct_username and correct_password):
		token_value = sha256(f"{correct_username}{correct_password}{app.token_secret_key}".encode()).hexdigest()
		app.token = token_value
		return {"token": token_value}
	else:
		raise HTTPException(status_code=401)

