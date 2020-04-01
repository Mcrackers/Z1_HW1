"""
Zadanie 2

Stwórz ścieżkę '/method' która zwróci nazwę metody z jaką wykonano request.
PS Wystarczy jeśli endpoint będzie obsługiwał requesty `GET`, `POST`, `PUT`, `DELETE`
PS2 W kodzie nie wolno użyć żadnego `ifa`

format odpowiedzi(JSON):
`{"method": "METHOD"}`
"""
from fastapi import FastAPI

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

