from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
db = SQLAlchemy(app)

# Create Models
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean, default=False)

@app.route('/')
@app.route('/index.html')
def index():
    todo_list = Todo.query.all()
    total_todo = len(todo_list)
    completed_todo = len([t for t in todo_list if t.complete])
    uncompleted = total_todo - completed_todo
    return render_template('dashboard/index.html', todo_list=todo_list, total_todo=total_todo, completed_todo=completed_todo, uncompleted=uncompleted)

@app.route('/about.html')
def about():
    return render_template('dashboard/about.html')

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('task_title')
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    todo = Todo.query.get(id)
    if todo:
        new_title = request.form.get('new_title')
        new_status = request.form.get('new_status')
        if new_title:
            todo.title = new_title
        if new_status is not None:
            todo.complete = new_status == 'true'
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
