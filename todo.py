from datetime import datetime
from flask import Flask, request, flash, url_for, redirect, \
     render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('todo.cfg')
db = SQLAlchemy(app)


class Keys(db.Model):
    __tablename__ = 'keys'
    id = db.Column('keys_id',db.Integer, primary_key=True)
    api_key= db.Column(db.String(50))
    key= db.Column(db.String(150))

    def __init__(self,id,api_key,key):
        self.id = id
        self.api_key = api_key
        self.key= key



class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column('todo_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.String)
    done = db.Column(db.Boolean)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.done = False
        self.pub_date = datetime.utcnow()


@app.route('/')
def show_all():
    return render_template('show_all.html',
        todos=Todo.query.order_by(Todo.pub_date.desc()).all()
    )


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['title']:
            flash('Title is required', 'error')
        elif not request.form['text']:
            flash('Text is required', 'error')
        else:
            todo = Todo(request.form['title'], request.form['text'])
            db.session.add(todo)
            db.session.commit()
            flash(u'Todo item was successfully created')
            return redirect(url_for('show_all'))
    return render_template('new.html')


@app.route('/update', methods=['POST'])
def update_done():
    for todo in Todo.query.all():
        todo.done = ('done.%d' % todo.id) in request.form
    flash('Updated status')
    db.session.commit()
    return redirect(url_for('show_all'))


@app.route('/keys', methods=['GET','POST'])
def keys():
    if request.method == 'POST':
        if not request.form['api_key']:
            flash('Api_key is required', 'error')
        elif not request.form['key']:
            flash('Key is required', 'error')
        else:
            keys = Keys(request.form['api_key'], request.form['key'])
            db.session.add(keys)
            db.session.commit()
            flash(u'keys items were successfully created')
            return redirect(url_for('show_all'))
    return render_template('key.html')


if __name__ == '__main__':
    app.run()
