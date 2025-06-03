from flask import Flask, request, jsonify
from flasgger import Swagger
from models import db, Student, Subject
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)
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


@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Actualizar un estudiante
    ---
    parameters:
      - in: path
        name: student_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          required:
            - name
            - email
          properties:
            name:
              type: string
            email:
              type: string
    responses:
      200:
        description: Estudiante actualizado
    """
    data = request.get_json()
    student = Student.query.get_or_404(student_id)
    student.name = data["name"]
    student.email = data["email"]
    db.session.commit()
    return jsonify({"id": student.id, "name": student.name})


@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Eliminar un estudiante
    ---
    parameters:
      - in: path
        name: student_id
        type: integer
        required: true
    responses:
      204:
        description: Estudiante eliminado
    """
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return '', 204

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


@app.route("/subjects/<int:subject_id>", methods=["PUT"])
def update_subject(subject_id):
    """
    Actualizar una asignatura
    ---
    parameters:
      - in: path
        name: subject_id
        type: integer
        required: true
      - in: body
        name: body
        schema:
          required:
            - name
            - student_id
          properties:
            name:
              type: string
            student_id:
              type: integer
    responses:
      200:
        description: Asignatura actualizada
    """
    data = request.get_json()
    subject = Subject.query.get_or_404(subject_id)
    subject.name = data["name"]
    subject.student_id = data["student_id"]
    db.session.commit()
    return jsonify({"id": subject.id, "name": subject.name})


@app.route("/subjects/<int:subject_id>", methods=["DELETE"])
def delete_subject(subject_id):
    """
    Eliminar una asignatura
    ---
    parameters:
      - in: path
        name: subject_id
        type: integer
        required: true
    responses:
      204:
        description: Asignatura eliminada
    """
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    return '', 204


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
