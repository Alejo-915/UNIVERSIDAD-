from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional


class Estudiante(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nombre: str
    correo: str
    edad: int
    semestre: int = Field(default=1)

    matriculas: List["Matricula"] = Relationship(back_populates="estudiante")

class Curso(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nombre: str
    descripcion: str
    creditos: int

    matriculas: List["Matricula"] = Relationship(back_populates="curso")

class Matricula(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    estudiante_id: int = Field(foreign_key="estudiante.id")
    curso_id: int = Field(foreign_key="curso.id")
    fecha: str

    estudiante: Optional[Estudiante] = Relationship(back_populates="matriculas")
    curso: Optional[Curso] = Relationship(back_populates="matriculas")
