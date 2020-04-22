from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
app = FastAPI()
app.num = 0
app.count = -1
patlist = []


@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/welcome")
def welcome_to_the_jungle():
	return {"message": "welcome to the jungle! We have funny games!"}


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
