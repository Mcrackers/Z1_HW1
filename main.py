from fastapi import FastAPI, Response, HTTPException, Depends
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


@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}

@app.get("/welcome")
def welcome_to_the_jungle():
	return {"message": "Welcome to the jungle! We have funny games!"}


@app.post("/login")
def login_to_app(response: Response, credentials: HTTPBasicCredentials=Depends(HTTPBasic())):
	if credentials.username in app.users and credentials.password == app.users[credentials.username]:
		s_token = sha256(bytes(f"{credentials.username}{credentials.password}{app.secret}", encoding='utf8')).hexdigest()
		app.tokens += s_token
		response.set_cookie(key="session_token",value=s_token)
		response.status_code = 307
		RedirectResponse(url='/welcome')
	else:
		raise HTTPException(status_code=401, detail="Niepoprawny login lub haslo")


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
