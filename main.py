import os
from fastapi import FastAPI
import psycopg2

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

def create_tables():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pacientes (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(255),
        modulo VARCHAR(50),
        fecha_inicio DATE,
        fecha_fin DATE
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS visitas (
        id SERIAL PRIMARY KEY,
        paciente_id INTEGER REFERENCES pacientes(id),
        tipo VARCHAR(50),
        fecha DATE
    );
    """)

    conn.commit()
    cur.close()
    conn.close()

@app.on_event("startup")
def startup():
    create_tables()

@app.get("/")
def read_root():
    return {"message": "AuditControl conectado a base correctamente 🚀"}
