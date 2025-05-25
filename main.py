import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dispatcher import dispatch_request

app = FastAPI()

class DispatchRequest(BaseModel):
    function_name: str
    payload: dict | None = None

@app.post("/dispatch")
async def dispatch_endpoint(request: DispatchRequest):
    """
    Endpoint principal pour dispatcher les appels vers les fonctions logiques.
    """
    try:
        response = dispatch_request(request.function_name, request.payload)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))