from fastapi import FastAPI, Cookie, Response, Depends
from hashlib import sha256
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials


app = FastAPI()
app.num = 0
app.count = -1
app.users = {"trudnY": "PaC13Nt", "admin": "admin"}
app.secret = "secret"
app.tokens = []
patlist = []

security = HTTPBasic()


@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}


#@app.post("/welcome")
@app.get("/welcome")
def welcome_to_the_jungle():
	return {"message": "welcome to the jungle! We have funny games!"}


@app.post("/login")
def login_to_app(user: str, passw: str, response: Response):
	if user in app.users and passw == app.users[user]:
		s_token = sha256(bytes(f"{user}{passw}{app.secret}", encoding='utf8')).hexdigest()
		app.tokens += s_token
		response.set_cookie(key="session_token",value=s_token)
		response = RedirectResponse(url='/welcome')
		print('logged in')
		return response
	else:
		return "username or password is incorrect"


@app.get("/users/me")
def read_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    return {"username": credentials.username, "password": credentials.password}

@app.get("/num")
def num():
	app.num += 1
	return app.num


@app.get("/patient")
def l_patients():
	return {"lista": patlist}


class Request(BaseModel):
	name: str
	surename: str


class Respond(BaseModel):
	id: int = None
	patient: dict


@app.post("/patient", response_model=Respond)
def new_patient(data: Request):
	if data:
		patlist.append(data.dict())
		app.count +=1
	return Respond(id = app.count, patient = data.dict())


@app.get("/patient/{pk}")
def get_patient(pk: int):
	if pk in range(len(patlist)):
		return Request(name = patlist[pk]["name"], surename = patlist[pk]["surename"])
	else:
		return JSONResponse(status_code=204, content={})
