from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="STD24174", description="This is a specification of STD24174")

class Characteristic(BaseModel):
    ram_memory: int
    rom_memory: int

class Phone(BaseModel):
    identifier: str
    brand: str
    model: str
    characteristics: Characteristic

class PhoneUpdate(BaseModel):
    characteristics: Characteristic


phones_db = []


@app.get("/health")
async def health_check():
    return "Ok"

@app.post("/phones", status_code=status.HTTP_201_CREATED)
async def create_phones(phones: List[Phone]):
    phones_db.extend(phones)
    return phones

@app.get("/phones")
async def get_all_phones():
    return phones_db

@app.get("/phones/{id}")
async def get_phone_by_id(id: str):
    for phone in phones_db:
        if phone.identifier == id:
            return phone
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Le phone comportant l'id {id} n'existe pas ou n'a pas été trouvé"
    )

@app.put("/phones/{id}/characteristics")
async def update_phone_characteristics(id: str, characteristics: Characteristic):
    for phone in phones_db:
        if phone.identifier == id:
            phone.characteristics = characteristics
            return phone
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Le phone comportant l'id {id} n'existe pas ou n'a pas été trouvé"
    )