from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class DatePayload(BaseModel):
    date: str

@app.post("/")
async def receive_date(payload: DatePayload):
    print("date :",  payload.date)
    return {"date": payload.date}