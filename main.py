from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine
from routes import estudiantes, cursos, matricula

from database import engine


app = FastAPI(title="Universidad API")

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

app.include_router(estudiantes.router)
app.include_router(cursos.router)
app.include_router(matricula.router)
