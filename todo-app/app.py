from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://nebo@localhost:5432/todo-app'
db = SQLAlchemy(app,
# session_options={"expire_on_commit": False} # provides a means that after a commit data in the session is invalid.
)

migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean(), nullable=False, default=False)
    def __repr__(self):
        return f'<Todo {self.id} {self.decription}>'

# migration will take care of the creation of the database.
# db.create_all()

def create_todo_entry(description):
    try:
        todo = Todo(description=description)
        db.session.add(todo)
        db.session.commit()
        error=False
    except:
        db.session.rollback()
        error=True
        print(sys.exc_info())
    finally:
        db.session.close()
        return error

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())

@app.route('/todos/create', methods=['POST'])
def create_todo():
    # form submission
    # description = request.form.get('description', '')
    # AJAX Asynch submission
    description = request.get_json()["description"]
    error = create_todo_entry(description)
    if (error):
        abort(500)
    else:
        return jsonify({
            'description': description
        })
    # must be the name of the route handler
    # return redirect(url_for('index'))