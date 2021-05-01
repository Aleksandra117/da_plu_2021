from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


import datetime

app=FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/hello", response_class=HTMLResponse)
def read_item(request: Request):

	t_date = datetime.date.today()
	today_date = t_date.strftime("%Y-%m-%d")
	return templates.TemplateResponse("index_task1.html.j2", {
		"request": request, "today_date": today_date})
