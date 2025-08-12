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

class travel(BaseModel):
    destination: str
    month:str
    price_pln:int
class traveldestinationUpdate(BaseModel):
    destination: str


def get_db_connection():
    conn=sqlite3.connect
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/health")
def create_healthl(destination: str, month: str, price_pln: int):
    validate_wpis(wpis)
    new_id = health[-1]["id"] + 1 if health else 1
    new_health = {"id": new_id, "destination": destination, "month": month, "price_pln": price_pln}
    health.append(new_health)
    return new_health
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

class travel(BaseModel):
    destination: str
    month:str
    price_pln:int
class traveldestinationUpdate(BaseModel):
    destination: str


def get_db_connection():
    conn=sqlite3.connect
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/health")
def health():
    return {"status": "ok"}
