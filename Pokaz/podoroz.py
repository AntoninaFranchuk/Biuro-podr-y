from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import requests

database="travel.db"
app = FastAPI()

conn = sqlite3.connect('travel.db', check_same_thread=False)
conn.row_factory = sqlite3.Row
cur=conn.cursor()

with sqlite3.connect(database) as conn:
    cur.execute("""
    CREATE TABLE IF NOT EXISTS travel( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        destination TEXT NOT NULL,
        
        month TEXT NOT NULL,
        price_pln REAL INTEGER NOT NULL,
        UNIQUE(destination,month)
    )
    """)

class Travel(BaseModel):
    destination: str
    month:str
    price_pln:int
class TraveldestinationUpdate(BaseModel):
    destination: str


def get_db_connection():
    conn=sqlite3.connect
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/health")
def create_health(travel:Travel):
    try:
        with get_db_connection(database) as conn:
            conn.row_factory = sqlite3.Row
            cur=conn.cursor()
            cur.execute(
            "INSERT INTO travel(destination, month, price_pln) VALUES(?,?,?)",
            (travel.destination, travel.month, travel.price_pln)
        )
        new_id = cur.lastrowid
        cur.execute("SELECT id FROM travel WHERE destination=?", (new_id,))
        return dict(cur.fetchone())