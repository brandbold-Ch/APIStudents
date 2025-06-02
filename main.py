from flask import Flask, request, jsonify
from flasgger import Swagger
from models import db, Student, Subject

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

swagger = Swagger(app)
db.init_app(app)


@app.before_request
def create_tables():
    db.create_all()

# ---------- CRUD Estudiantes ----------


@app.route("/students", methods=["POST"])
def create_student():
    """
    Crear un estudiante
    ---
    parameters:
      - in: body
        name: body
        schema:
          id: Student
          required:
            - name
            - email
          properties:
            name:
              type: string
            email:
              type: string
    responses:
      201:
        description: Estudiante creado
    """
    data = request.get_json()
    student = Student(name=data["name"], email=data["email"])
    db.session.add(student)
    db.session.commit()
    return jsonify({"id": student.id, "name": student.name}), 201


@app.route("/students", methods=["GET"])
def get_students():
    """
    Listar todos los estudiantes
    ---
    responses:
      200:
        description: Lista de estudiantes
    """
    students = Student.query.all()
    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "email": s.email,
            "subjects": [sub.name for sub in s.subjects]
        } for s in students
    ])

# CRUD PUT y DELETE omitidos por brevedad, pero también se pueden documentar igual

# ---------- CRUD Asignaturas ----------

@app.route("/subjects", methods=["POST"])
def create_subject():
    """
    Crear una asignatura
    ---
    parameters:
      - in: body
        name: body
        schema:
          id: Subject
          required:
            - name
            - student_id
          properties:
            name:
              type: string
            student_id:
              type: integer
    responses:
      201:
        description: Asignatura creada
    """
    data = request.get_json()
    subject = Subject(name=data["name"], student_id=data["student_id"])
    db.session.add(subject)
    db.session.commit()
    return jsonify({"id": subject.id, "name": subject.name}), 201


@app.route("/subjects", methods=["GET"])
def get_subjects():
    """
    Listar todas las asignaturas
    ---
    responses:
      200:
        description: Lista de asignaturas
    """
    subjects = Subject.query.all()
    return jsonify([
        {
            "id": s.id,
            "name": s.name,
            "student": s.student.name
        } for s in subjects
    ])
