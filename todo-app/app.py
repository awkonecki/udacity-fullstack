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

# many to many example
# order_items = db.Table('order_items',
#     db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
#     db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
# )

# class Order(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   status = db.Column(db.String(), nullable=False)
#   products = db.relationship('Product', secondary=order_items,
#       backref=db.backref('orders', lazy=True))

# class Product(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String(), nullable=False)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean(), nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=True)
    def __repr__(self):
        return f'<Todo {self.id} {self.decription}>'

class TodoList(db.Model):
    __tablename__= 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship("Todo", backref='list', lazy=True)

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

def update_todo_entry(todo_id, entry_status):
    try:
        todo_item = Todo.query.get(todo_id)
        todo_item.completed = entry_status
        # db.session.update(todo_item)
        db.session.commit()
        error = False
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
        return error

def delete_todo_entry(todo_id):
    try:
        # todo_item = Todo.query.get(todo_id)
        # db.session.delete(todo_item)
        # db.session.commit()
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
        error = False
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info())
    finally:
        db.session.close()
        return error

@app.route('/lists/<int:list_id>')
def get_list_todos(list_id):
    return render_template('index.html',
        lists=TodoList.query.all(),
        active_list=TodoList.query.get(list_id),
        todos=Todo.query.filter_by(list_id=list_id).order_by('id').all())

@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))

@app.route('/todos/<int:todo_id>/delete', methods=['DELETE'])
def deleteTodo(todo_id):
    error = delete_todo_entry(todo_id)
    return jsonify({ "success": True })

@app.route('/todos/<int:todo_id>/checked', methods=['POST'])
def checkCompleted(todo_id):
    completed = request.get_json()["completed"]
    error = update_todo_entry(todo_id, completed)
    if (error):
        abort(500)
    else:
        return redirect(url_for('index'))

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