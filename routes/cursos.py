from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select
from models import Curso
from database import engine


router = APIRouter(prefix="/cursos", tags=["Cursos"])

@router.get("/")
def listar_cursos(creditos: int | None = Query(default=None, description="Filtrar cursos por número de créditos")):
    with Session(engine) as session:
        query = select(Curso)
        if creditos is not None:
            query = query.where(Curso.creditos == creditos)
        cursos = session.exec(query).all()
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

# actualizar cuerso
@router.put("/{curso_id}")
def actualizar_curso(curso_id: int, datos_actualizados: Curso):
    with Session(engine) as session:
        curso = session.get(Curso, curso_id)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")

        # actualizar solo los campos enviados
        if datos_actualizados.nombre:
            curso.nombre = datos_actualizados.nombre
        if datos_actualizados.descripcion:
            curso.descripcion = datos_actualizados.descripcion

        session.add(curso)
        session.commit()
        session.refresh(curso)
        return {"mensaje": "Curso actualizado correctamente", "curso": curso}
