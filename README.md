# Universidad API

##  Descripción
Proyecto desarrollado en **FastAPI** y **SQLModel** que gestiona la información de una universidad.  
Permite registrar **estudiantes**, **cursos** y **matrículas**, incluyendo relaciones entre las tablas y un **filtro por créditos** en los cursos.  
Es ideal para practicar conceptos de bases de datos relacionales, ORM y desarrollo de APIs RESTful.

---

##  Requisitos
Antes de ejecutar el proyecto, asegúrate de tener instalado:

- **Python 3.10 o superior**
- **FastAPI**
- **SQLModel**
- **Uvicorn**
- **SQLite** (base de datos por defecto)

# Pasos para ejecutar el proyecto

1. Clonar el repositorio
git clone <url>

2. Crear el entorno virtual
python -m venv venv

3. Activar el entorno virtual
venv\Scripts\activate

4. Instalar las dependencias
pip install -r requirements.txt

5. Ejecutar el proyecto (ejemplo con FastAPI)
uvicorn main:app --reload

USO
Una vez el servidor esté corriendo, abre tu navegador en:


http://127.0.0.1:8000/docs
Allí podrás interactuar con la documentación automática generada por Swagger UI y probar los endpoints.

🔗 Rutas principales (Endpoints)
🧑‍🎓 Estudiantes
POST /estudiantes/ → Crear un nuevo estudiante

GET /estudiantes/ → Listar todos los estudiantes

📘 Cursos
POST /cursos/ → Crear un nuevo curso

GET /cursos/ → Listar todos los cursos

GET /cursos/filtro?min_creditos=3 → Filtrar cursos por cantidad mínima de créditos

🧾 Matrículas
POST /matriculas/ → Crear una matrícula

GET /matriculas/ → Listar todas las matrículas

Autor
Edwin Alejandro López Montero
Estudiante de Ingeniería en Sistemas y Computación

