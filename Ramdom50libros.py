#!/usr/bin/env python3
import requests
import json
from faker import Faker

# Credenciales y host del simulador de API
APIHOST = "http://library.demo.local"
LOGIN = "cisco"
PASSWORD = "Cisco123!"

def getAuthToken():
    authCreds = (LOGIN, PASSWORD)
    r = requests.post(
        f"{APIHOST}/api/v1/loginViaBasic", 
        auth=authCreds
    )
    if r.status_code == 200:
        return r.json()["token"]
    else:
        raise Exception(f"Status code {r.status_code} and text {r.text}, while trying to Auth.")

def addBook(book, apiKey):
    r = requests.post(
        f"{APIHOST}/api/v1/books", 
        headers={
            "Content-type": "application/json",
            "X-API-Key": apiKey
        },
        data=json.dumps(book)
    )
    if r.status_code == 200:
        print(f"Book {book} added.")
    else:
        raise Exception(f"Error code {r.status_code} and text {r.text}, while trying to add book {book}.")

def getBooks(apiKey):
    r = requests.get(
        f"{APIHOST}/api/v1/books",
        headers={"X-API-Key": apiKey}
    )
    if r.status_code == 200:
        print("\n--- Listado total de libros creados en la biblioteca ---")
        print(json.dumps(r.json(), indent=2))
    else:
        print(f"Error al obtener los libros: {r.status_code} - {r.text}")

if __name__ == "__main__":
    # 1. Obtener el token de autorización
    apiKey = getAuthToken()
    
    # 2. Inicializar Faker para generar datos aleatorios (título, autor, isbn)
    fake = Faker()
    
    print("--- Agregando 50 libros aleatorios ---")
    # 3. Bucle para agregar 50 libros (ejemplo de IDs del 108 al 157)
    for i in range(108, 158):
        fakeTitle = fake.catch_phrase()
        fakeAuthor = fake.name()
        fakeISBN = fake.isbn13()
        
        book = {
            "id": i,
            "title": fakeTitle,
            "author": fakeAuthor,
            "isbn": fakeISBN
        }
        
        addBook(book, apiKey)
        
