from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from models import Matricula, Estudiante, Curso
from database import engine

router = APIRouter(prefix="/matriculas", tags=["Matriculas"])


#  Crear una matrícula (registrar estudiante en curso)
@router.post("/")
def crear_matricula(matricula: Matricula):
    with Session(engine) as session:
        # Verificamos si el estudiante existe
        estudiante = session.get(Estudiante, matricula.estudiante_id)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")

        # Verificamos si el curso existe
        curso = session.get(Curso, matricula.curso_id)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")

        # Verificamos si ya está matriculado en ese curso
        existe = session.exec(
            select(Matricula)
            .where(Matricula.estudiante_id == matricula.estudiante_id)
            .where(Matricula.curso_id == matricula.curso_id)
        ).first()

        if existe:
            raise HTTPException(status_code=400, detail="El estudiante ya está matriculado en este curso")

        # Guardamos la matrícula
        session.add(matricula)
        session.commit()
        session.refresh(matricula)
        return matricula


#  Listar todas las matrículas
@router.get("/")
def listar_matriculas():
    with Session(engine) as session:
        matriculas = session.exec(select(Matricula)).all()
        return matriculas

#  Ver una matrícula por ID
@router.get("/{matricula_id}")
def obtener_matricula(matricula_id: int):
    with Session(engine) as session:
        matricula = session.get(Matricula, matricula_id)
        if not matricula:
            raise HTTPException(status_code=404, detail="Matrícula no encontrada")
        return matricula


#  Listar todos los cursos en los que está inscrito un estudiante
@router.get("/estudiante/{estudiante_id}")
def cursos_por_estudiante(estudiante_id: int):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, estudiante_id)
        if not estudiante:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")

        matriculas = session.exec(
            select(Matricula).where(Matricula.estudiante_id == estudiante_id)
        ).all()

        cursos = []
        for m in matriculas:
            curso = session.get(Curso, m.curso_id)
            cursos.append({
                "curso_id": curso.id,
                "nombre": curso.nombre,
                "descripcion": curso.descripcion,
                "fecha_matricula": m.fecha
            })

        return {"estudiante": estudiante.nombre, "cursos": cursos}


#  Listar todos los estudiantes matriculados en un curso
@router.get("/curso/{curso_id}")
def estudiantes_por_curso(curso_id: int):
    with Session(engine) as session:
        curso = session.get(Curso, curso_id)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")

        matriculas = session.exec(
            select(Matricula).where(Matricula.curso_id == curso_id)
        ).all()

        estudiantes = []
        for m in matriculas:
            estudiante = session.get(Estudiante, m.estudiante_id)
            estudiantes.append({
                "estudiante_id": estudiante.id,
                "nombre": estudiante.nombre,
                "correo": estudiante.correo,
                "fecha_matricula": m.fecha
            })

        return {"curso": curso.nombre, "estudiantes": estudiantes}


# Eliminar una matrícula (desmatricular estudiante de un curso)
@router.delete("/{matricula_id}")
def eliminar_matricula(matricula_id: int):
    with Session(engine) as session:
        matricula = session.get(Matricula, matricula_id)
        if not matricula:
            raise HTTPException(status_code=404, detail="Matrícula no encontrada")

        session.delete(matricula)
        session.commit()
        return {"mensaje": f"El estudiante con ID {matricula.estudiante_id} fue desmatriculado del curso {matricula.curso_id}"}


@router.delete("/")
def eliminar_por_estudiante_y_curso(estudiante_id: int, curso_id: int):
    with Session(engine) as session:
        matricula = session.exec(
            select(Matricula)
            .where(Matricula.estudiante_id == estudiante_id)
            .where(Matricula.curso_id == curso_id)
        ).first()

        if not matricula:
            raise HTTPException(status_code=404, detail="Matrícula no encontrada")

        session.delete(matricula)
        session.commit()
        return {"mensaje": f"El estudiante {estudiante_id} fue desmatriculado del curso {curso_id}"}


