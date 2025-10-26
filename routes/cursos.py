from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from models import Curso
from database import engine


router = APIRouter(prefix="/cursos", tags=["Cursos"])

@router.get("/")
def listar_cursos():
    with Session(engine) as session:
        cursos = session.exec(select(Curso)).all()
        return cursos

@router.post("/")
def crear_curso(curso: Curso):
    with Session(engine) as session:
        session.add(curso)
        session.commit()
        session.refresh(curso)
        return curso

@router.get("/{curso_id}")
def obtener_curso(curso_id: int):
    with Session(engine) as session:
        curso = session.get(Curso, curso_id)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        return curso

@router.delete("/{curso_id}")
def eliminar_curso(curso_id: int):
    with Session(engine) as session:
        curso = session.get(Curso, curso_id)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
        session.delete(curso)
        session.commit()
        return {"mensaje": "Curso eliminado correctamente"}
