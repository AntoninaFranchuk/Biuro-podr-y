from fastapi import FastAPI
import sqlite3
import requests

app = FastAPI()
conn = sqlite3.connect

def get_db_connection():
    conn=sqlite3.connect
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/health")
def health():
    return {"status": "ok"}
