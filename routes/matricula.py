from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from models import Matricula, Estudiante, Curso
from database import engine

router = APIRouter(prefix="/matriculas", tags=["Matrículas"])

@router.get("/")
def listar_matriculas():
    with Session(engine) as session:
        matriculas = session.exec(select(Matricula)).all()
        return matriculas

@router.post("/")
def crear_matricula(matricula: Matricula):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, matricula.estudiante_id)
        curso = session.get(Curso, matricula.curso_id)

        if not estudiante or not curso:
            raise HTTPException(status_code=404, detail="Estudiante o curso no existe")

        session.add(matricula)
        session.commit()
        session.refresh(matricula)
        return matricula

@router.get("/{matricula_id}")
def obtener_matricula(matricula_id: int):
    with Session(engine) as session:
        matricula = session.get(Matricula, matricula_id)
        if not matricula:
            raise HTTPException(status_code=404, detail="Matrícula no encontrada")
        return matricula

@router.delete("/{matricula_id}")
def eliminar_matricula(matricula_id: int):
    with Session(engine) as session:
        matricula = session.get(Matricula, matricula_id)
        if not matricula:
            raise HTTPException(status_code=404, detail="Matrícula no encontrada")
        session.delete(matricula)
        session.commit()
        return {"mensaje": "Matrícula eliminada correctamente"}
