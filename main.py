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

Zadanie 4
Stwórz ścieżkę `/patient/{pk}`, która przyjmuje request w metodą GET.

pk, powinien być liczbą. Najlepiej intem.

W przypadku znalezienia takiego pacjenta, odpowiedź powinna wyglądać tak:
`{"name": "NAME", "surename": "SURENAME"}`

W przypadku nieznalezienia należy zwrócić odpowiedni kod http:
https://en.wikipedia.org/wiki/List_of_HTTP_status_codes

PS 1 Podobnie jak w poprzednim zadaniu, znajdź miejsce w aplikacji, gdzie można zapisać pacjenta

PS 2 Zmodyfikuj endpoint POST `/patient`, tak aby zachował przesłane dane

PS 3 Pamiętaj, aby liczyć pacjentów od 0!
"""


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()
app.num = 0
app.count = -1
patlist = []


@app.get("/")
def root():
	return {"message": "Hello World during the coronavirus pandemic!"}


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
		return patlist[pk]
	else:
		raise HTTPException(status_code=204, detail="No Content")
