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


app.num = 0


def num():
	app.num += 1
	return app.num


@app.get("/number")
def number():
	return str(app.num)


class Request(BaseModel):
	name: str
	surename: str


class Respond(BaseModel):
	id = num()
	patient: dict


@app.post("/patient", response_model=Respond)
def new_patient(data: Request):
	return Respond(patient=data.dict())



