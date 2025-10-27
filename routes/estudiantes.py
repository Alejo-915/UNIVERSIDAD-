from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from models import Estudiante
from database import engine

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

@router.get("/")
def listar_estudiantes():
    with Session(engine) as session:
        estudiantes = session.exec(select(Estudiante)).all()
        return estudiantes

@router.post("/")
def crear_estudiante(estudiante: Estudiante):
    with Session(engine) as session:
        session.add(estudiante)
        session.commit()
        session.refresh(estudiante)
        raise HTTPException(status_code=201, detail="Estudiante creado correctamnete")
        return estudiante

@router.get("/{estudiante_id}")
def obtener_estudiante(estudiante_id: int):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, estudiante_id)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        return estudiante

@router.delete("/{estudiante_id}")
def eliminar_estudiante(estudiante_id: int):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, estudiante_id)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        session.delete(estudiante)
        session.commit()
        return {"mensaje": "Estudiante eliminado correctamente"}
