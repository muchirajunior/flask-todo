# type: ignore
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mydb.db'

db=SQLAlchemy(app)

class Todo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    todo=db.Column(db.String)
    complete=db.Column(db.Boolean, default=False)

    def __init__(self, todo):
        self.todo=todo



@app.route('/')
def index():
    todos=Todo.query.all()
    print(todos)
    return render_template('index.html', page="TODO APP", todos=todos)

@app.route('/add', methods=['POST','GET'])
def addtodo():
    if request.method=='POST':
        todo=request.form['todo']
        newTodo=Todo(todo)
        db.session.add(newTodo)
        db.session.commit()

        return redirect('/')

    return render_template('add.html', page="add todo")

@app.route('/update/<id>')
def update(id):
    todo=Todo.query.filter_by(id=id).first()
    todo.complete=True
    db.session.commit()
    return redirect('/')

@app.route('/delete/<id>')
def delete(id):
    todo=Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 