from fastapi import FastAPI

from powerplantapp.api.services.strategy import compute_response
from powerplantapp.domain.model import PayLoad


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/productionplan")
async def production_plan(payload: PayLoad):
    return compute_response(payload)
