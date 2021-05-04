from fastapi import FastAPI, Request, Response, Cookie, HTTPException, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from hashlib import sha256

import datetime
import secrets


app=FastAPI()
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()


login = "4dm1n"
passwd = "NotSoSecurePa$$"
app.session_token = []
app.token = []



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
		session_token = secrets.token_urlsafe(32)
		if len(app.session_token) == 3:
			app.session_token.pop(0)
		app.session_token.append(session_token)
		response.set_cookie(key="session_token", value=session_token)
	else:
		raise HTTPException(status_code=401)



@app.post("/login_token", status_code=201)
def logint(credentials: HTTPBasicCredentials = Depends(security)):
	correct_username = secrets.compare_digest(credentials.username, login)
	correct_password = secrets.compare_digest(credentials.password, passwd)
	if (correct_username and correct_password):
		token_value = secrets.token_urlsafe(32)
		if len(app.token) == 3:
			app.token.pop(0)
		app.token.append(token_value)
		return {"token": token_value}

	else:
		raise HTTPException(status_code=401)


@app.get("/welcome_session", status_code = 200)
def secured_data(response: Response, format: str = "", session_token: str = Cookie(None)):
	if (session_token not in app.session_token):
			raise HTTPException(status_code=401)
	else:
		if format == "json":
			data = {"message": "Welcome!"}
			return data
		elif format == "html":
			data = """
			<html>
				<head>
					<title>Some HTML in here</title>
				</head>
				<body>
					<h1>Welcome!</h1>
				</body>
			</html>
			"""
			return Response(content = data, media_type="text/html")
		else:
			data = "Welcome!"
			return Response(content = data, media_type="text/plain")
	
		

@app.get("/welcome_token", status_code=200)
def secured_data_token(response: Response, format: str = "", token: str = ""):
	if (token not in app.token):
			raise HTTPException(status_code=401)
	else:
		if format == "json":
			data = {"message": "Welcome!"}
			return data
		elif format == "html":
			data = """
			<html>
				<head>
					<title>Some HTML in here</title>
				</head>
				<body>
					<h1>Welcome!</h1>
				</body>
			</html>
			"""
			return Response(content = data, media_type="text/html")
		else:
			data = "Welcome!"
			return Response(content = data, media_type="text/plain")
	



@app.delete("/logout_session")
def logouts(format: str = "", session_token: str = Cookie(None)):
	if (session_token not in app.session_token):
			raise HTTPException(status_code=401)
	else:
		index_session = app.session_token.index(session_token)
		app.session_token.pop(index_session)

		return RedirectResponse("/logged_out?format="+format, status_code = 303)





@app.delete("/logout_token")
def logoutt(format: str = "", token: str = ""):
	if (token not in app.token):
			raise HTTPException(status_code=401)
	else:
		index_token = app.token.index(token)
		app.token.pop(index_token)

		return RedirectResponse("/logged_out?format="+format, status_code = 303)




@app.get("/logged_out", status_code = 200)
def logged_out_view(response: Response, format :str = ""):
	if format == "json":
		return {"message": "Logged out!"}
	elif format == "html":
		data = """
		<html>
			<head>
				<title>Some HTML in here</title>
			</head>
			<body>
				<h1>Logged out!</h1>
			</body>
		</html>
		"""
		return Response(content = data, media_type="text/html")
	else:
		data = "Logged out!"
		return Response(content = data, media_type="text/plain")