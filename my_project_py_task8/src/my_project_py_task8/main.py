import re
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def add_nums(a, b):
    return a + b