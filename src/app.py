from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# configurando el orm 
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id','title','description')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

# para agregar tareas 
@app.route('/tasks', methods=['POST'])
def create_task():
    titulo = request.json['title']
    descripcion = request.json['description']
    # creando la tarea 
    newTask = Task(titulo, descripcion)
    # guardando en la base de datos 
    db.session.add(newTask)
    db.session.commit()
    return task_schema.jsonify(newTask)

# para ver las tareas existentes 
@app.route('/tasks', methods=['GET'])
def get_task():
    allTask = Task.query.all()
    resultados = tasks_schema.dump(allTask)
    return jsonify(resultados)

#  para ver tareas por id 
@app.route('/tasks/<idTask>', methods=['GET'])
def getTask(idTask):
    task = Task.query.get(idTask)
    return task_schema.jsonify(task)

#  para actualizar por id 
@app.route('/tasks/<idTask>', methods=['PUT'])
def updateTask(idTask):
    task = Task.query.get(idTask)
    titulo = request.json['title']
    descripcion = request.json['description']
    task.title = titulo
    task.description = descripcion
    db.session.commit()
    return task_schema.jsonify(task)

# para eliminar por id 
@app.route('/tasks/<idTask>', methods=['DELETE'])
def deleteTask(idTask):
    task = Task.query.get(idTask)
    db.session.delete(task)
    db.session.commit()
    return task_schema.jsonify(task)

# ruta inicial 
@app.route('/', methods=['GET'])
def index():
    return jsonify({'mesanje':'Bienvenido!'})

if __name__ == '__main__':
    app.run(debug=True)