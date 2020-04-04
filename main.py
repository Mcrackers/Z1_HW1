"""
Zadanie 2

Stwórz ścieżkę '/method' która zwróci nazwę metody z jaką wykonano request.
PS Wystarczy jeśli endpoint będzie obsługiwał requesty `GET`, `POST`, `PUT`, `DELETE`
PS2 W kodzie nie wolno użyć żadnego `ifa`

format odpowiedzi(JSON):
`{"method": "METHOD"}`

Zadanie 3

Stwórz ścieżkę `/patient`, która przyjmie request z metodą `POST` i danymi w formacie json w postaci:

`{"name": "IMIE", "surename": "NAZWISKO"}`

i zwróci JSON w postaci:

`{"id": N, "patient": {"name": "IMIE", "surename": "NAZWISKO"}}`

Gdzie `N` jest kolejnym numerem zgłoszonej osoby

Naturalnie ścieżka ma działać dla dowolnych stringów (w kodowaniu utf-8) podanych w polach `name` i `surename`.

PS 1 W tym zadaniu ważne jest aby znaleźć miejsce w którym będzie można zapisać ilość odwiedzin od ostatniego uruchomienia aplikacji na serwerze oraz 
umieć posługiwać JSONami.
Na tym etapie kursu nie bawimy się w bazy danych. Być może spostrzeżesz bardzo ciekawe zachowanie ;-)

PS 2 Przed uruchomieniem testów, należy zrestartować swoją aplikację, żeby licznik na początku miał wartość 0!
"""
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
app.num = -1
l1 = []


@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}


@app.get("/method")
def return_get():
	return {"method": "GET"}


@app.post("/method")
def return_post():
	return {"method": "POST"}


@app.put("/method")
def return_put():
	return {"method": "PUT"}


@app.delete("/method")
def return_delete():
	return {"method": "DELETE"}


@app.get("/num")
def num():
	app.num += 1
	return app.num


@app.get("/patient")
def l_patients():
	return {"lista": l1}


class Request(BaseModel):
	name: str
	surename: str


class Respond(BaseModel):
	id: int
	patient: dict


@app.post("/patient", response_model=Respond)
def new_patient(data: Request):
	if data:
		l1.append(data.dict())
		app.num +=1
	return Respond(id = app.num, patient = data.dict())