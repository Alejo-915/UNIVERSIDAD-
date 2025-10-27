from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select
from models import Estudiante
from database import engine

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.get("/")
def listar_estudiantes(semestre: int = Query(None, description="Filtrar por semestre")):
    with Session(engine) as session:
        query = select(Estudiante)

        if semestre is not None:
            query = query.where(Estudiante.semestre == semestre)

        estudiantes = session.exec(query).all()

        if not estudiantes:
            raise HTTPException(status_code=404, detail="No se encontraron estudiantes con ese filtro")

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


#    actualizar estudiante
@router.put("/{estudiante_id}")
def actualizar_estudiante(estudiante_id: int, datos_actualizados: Estudiante):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, estudiante_id)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")

        # actualizar solo los campos enviados
        if datos_actualizados.nombre:
            estudiante.nombre = datos_actualizados.nombre
        if datos_actualizados.correo:
            estudiante.correo = datos_actualizados.correo
        if datos_actualizados.edad:
            estudiante.edad = datos_actualizados.edad

        session.add(estudiante)
        session.commit()
        session.refresh(estudiante)
        return {"mensaje": "Estudiante actualizado correctamente", "estudiante": estudiante}

