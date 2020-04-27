from fastapi import FastAPI, Response, Request, HTTPException, Depends, Cookie
from hashlib import sha256
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.patient_id = 0
app.users = {"trudnY": "PaC13Nt", "admin": "admin"}
app.secret = "secret"
app.tokens = {}
app.patient_list = {}

template = Jinja2Templates(directory="templates")


@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}


def check_stupid_cookie(session_token: str = Cookie(None)):
	print(session_token)
	print(app.tokens)
	if session_token not in app.tokens:
		session_token = None
	return session_token


@app.get("/welcome")
def welcome_to_the_jungle(request: Request, session_token: str = Depends(check_stupid_cookie)):
	if session_token is None:
		raise HTTPException(status_code=401, detail="dostęp wzbroniony")
	user = app.tokens[session_token]
	return template.TemplateResponse("item.html", {"request": request, "user": user})


@app.post("/login")
def login_to_app(response: Response, credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
	if credentials.username in app.users and credentials.password == app.users[credentials.username]:
		session_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret}", encoding='utf8')).hexdigest()
		app.tokens[session_token] = credentials.username
		response.set_cookie(key="session_token", value=session_token)
		print(session_token)
		response.status_code = 307
		response.headers['Location'] = "/welcome"
		return response
	else:
		raise HTTPException(status_code=401, detail="Niepoprawny login lub hasło")


@app.post("/logout")
def bye_bye(response: Response):
	response.delete_cookie(key="session_token",path="/")
	response.status_code = 307
	response.headers['Location'] = "/"
	return response


@app.post("/patient")
def add_patient(response: Response, name: str, surname: str, session_token: str = Depends(check_stupid_cookie)):
	if session_token is None:
		raise HTTPException(status_code=401, detail="dostęp wzbroniony")
	app.patient_id +=1
	app.patient_list[app.patient_id] = {name:surname}
	response.status_code = 307
	response.headers['Location'] = f"/patient/{app.patient_id}"
	return JSONResponse(app.patient_list[app.patient_id])


@app.get("/patient")
def show_patients(response: Response, session_token: str = Depends(check_stupid_cookie)):
	if session_token is None:
		raise HTTPException(status_code=401, detail="dostęp wzbroniony")
	response.status_code = 307
	return JSONResponse(app.patient_list)


@app.get("/patient/{id}")
def show_patients(id: int, session_token: str = Depends(check_stupid_cookie)):
	if session_token is None:
		raise HTTPException(status_code=401, detail="dostęp wzbroniony")
	return JSONResponse(app.patient_list[id])


@app.delete("/patient/{id}")
def show_patients(response: Response, id: int, session_token: str = Depends(check_stupid_cookie)):
	if session_token is None:
		raise HTTPException(status_code=401, detail="dostęp wzbroniony")
	app.patient_list.pop(id)
	response.status_code = 204
	#response.headers['Location'] = f"/patient"
