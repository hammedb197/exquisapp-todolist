from flask import Flask, request
from flask import render_template
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)

    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return 'Content {}'.format(self.content)
db.drop_all()
db.create_all()


@app.route('/')
def tasks_list():
    tasks = Todo.query.all()
    return render_template('todo_list.html', tasks=tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    content = request.form['content']
    if not content:
        return 'No content added, reload the page'

    todos = Todo(content)
    db.session.add(todos)
    db.session.commit()
    return redirect('/')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    todos = Todo.query.get(task_id)
    if not todos:
        return redirect('/')

    db.session.delete(todos)
    db.session.commit()
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)