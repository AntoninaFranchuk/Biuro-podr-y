from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Optinal
from pydantic import validator
import sqlite3
import requests

database = "travel.db"
app = FastAPI(title="Travel API", description="CRUD operations for travels", version="1.0")

with sqlite3.connect(database) as conn:
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS trips( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        destination TEXT NOT NULL,
        month TEXT NOT NULL,
        price_pln REAL NOT NULL,
        UNIQUE(destination, month)
    )
    """)

class Travel(BaseModel):
    destination: str
    month: str
    price_pln: float

def get_currency_rate(currency_code: str) -> float:
    if currency_code.upper() == "PLN":
        return 1.0  # курс PLN к PLN всегда 1
    url = f"https://api.nbp.pl/api/exchangerates/rates/A/{currency_code.upper()}?format=json"
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Currency {currency_code} not supported")
        data = resp.json()
        return data["rates"][0]["mid"]
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=400, detail="NBP API request failed")

def get_db_connection():
    conn = sqlite3.connect(database, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
    
@validator("destination","month")
def not_empty(cls,v):
    if not v.strip():
        raise ValueError("Error")
    return v

@validator("price_pln")
def not_negative(cls,v):
    if v<0:
        raise ValueError("Error, price_pln must be >=0")
    return v

@app.post("/trips",status_code=201)
def create_trip(trip: Travel):
    with get_db_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO travel(destination, month, price_pln) VALUES (?, ?, ?)",
                (trip.destination.strip(), trip.month.strip(), trip.price_pln)
            )
            conn.commit()
            return {**trip.dict(),"id":cur.lastrowid}
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="This travel already exists")
@app.get("/trips")
def get_all_trips():
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM trips ORDER BY destination, month")
        return [dict(row) for row in cur.fetchall()]

@app.get("/trips/{destination}")
def get_trips_by_destination(destination: str):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM trips WHERE LOWER(destination) = LOWER(?) ORDER BY month",
            (destination,)
        )
        return [dict(row) for row in cur.fetchall()]

@app.get("/trips")
def get_all_trips(currency: Optional[str] = "PLN"):
    rate = get_currency_rate(currency)
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM trips ORDER BY destination, month")
        trips = [dict(row) for row in cur.fetchall()]
        if currency.upper() != "PLN":
            for trip in trips:
                trip["price"] = round(trip["price_pln"] / rate, 2)
                trip["currency"] = currency.upper()
                del trip["price_pln"]
        return trips

@app.get("/trips/{destination}")
def get_trips_by_destination(destination: str, currency: Optional[str] = "PLN"):
    rate = get_currency_rate(currency)
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM trips WHERE LOWER(destination) = LOWER(?) ORDER BY month",
            (destination,)
        )
        trips = [dict(row) for row in cur.fetchall()]
        if currency.upper() != "PLN":
            for trip in trips:
                trip["price"] = round(trip["price_pln"] / rate, 2)
                trip["currency"] = currency.upper()
                del trip["price_pln"]
        return trips
