from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import requests

database = "travel.db"
app = FastAPI(title="Travel API", description="CRUD operations for travels", version="1.0")

with sqlite3.connect(database) as conn:
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS travel( 
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

def get_db_connection():
    conn = sqlite3.connect(database, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/travels")
def create_travel(travel: Travel):
    with get_db_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO travel(destination, month, price_pln) VALUES (?, ?, ?)",
                (travel.destination, travel.month, travel.price_pln)
            )
            conn.commit()
            return {"id": cur.lastrowid}
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="This travel already exists")
