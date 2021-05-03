from fastapi import FastAPI, Request, Response, Cookie, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from hashlib import sha256

import datetime

app=FastAPI()
templates = Jinja2Templates(directory="templates")

login = "4dm1n"
passwd = "NotSoSecurePa$$"
app.session_token = None
app.token = None



@app.get("/hello", response_class=HTMLResponse)
def read_item(request: Request):

	t_date = datetime.date.today()
	today_date = t_date.strftime("%Y-%m-%d")
	return templates.TemplateResponse("index_task1.html.j2", {
		"request": request, "today_date": today_date})




@app.post("/login_session", status_code=201)
def logins(user: str, password: str, response: Response):
	if (login == user and password == passwd):
		session_token = sha256(f"{user}{password}".encode()).hexdigest()
		app.session_token = session_token
		response.set_cookie(key="session_token", value=session_token)
	else:
		raise HTTPException(status_code=401)



@app.post("/login_token", status_code=201)
def logint(user: str, password: str, response: Response):
	if (login == user and password == passwd):
		token_value = sha256(f"{user}{password}".encode()).hexdigest()
		app.token = token_value
		return {"token": token_value}
	else:
		raise HTTPException(status_code=401)


