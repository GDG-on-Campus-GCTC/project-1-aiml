from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from teachers.crew import Teachers
import os 

load_dotenv("teachers\.env")
app=FastAPI()

class Query(BaseModel):
    input: str
    c:int= 2026

@app.post("/query")
def query(query: Query):
    inputs={
        'topic': query.input,
        'current_year': str(query.c)
    }
    r=Teachers().crewcall()
    result=r.kickoff(inputs=inputs)
    return {"response": result.raw}

@app.get("/")
def home():
    return "welcome to the study portal"
