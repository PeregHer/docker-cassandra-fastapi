from fastapi import FastAPI
from starlette.responses import RedirectResponse
from data import Connexion

app = FastAPI()

@app.get("/", include_in_schema=False)
def redirect():
    return RedirectResponse('/docs')

@app.get("/restaurant/{id}", tags=['Resto'])
def get_restaurant(id):
    data = Connexion.get_restaurant(id)
    return {'data': data} 

@app.get("/restaurant/{id}/inspections", tags=['Resto'])
def get_resto_inspec(id):
    data = Connexion.get_resto_inspec(id)
    return {'data': data} 

@app.get("/resto_by_type/{type}", tags=['Resto'])
def get_resto_names(type):
    data = Connexion.get_resto_names(type)
    return {'data': data}

@app.get("/top10/{grade}", tags=['Resto'])
def get_top10(grade):
    data = Connexion.get_top10(grade)
    return {'data': data}