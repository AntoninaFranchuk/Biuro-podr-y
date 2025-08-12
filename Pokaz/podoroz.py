from fastapi import FastAPI
import sqlite3
import requests
app = FastAPI()
conn = sqlite3.connect

@app.get("/health")
def health():
    return {"status": "ok"}