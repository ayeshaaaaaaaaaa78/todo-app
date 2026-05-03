from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB = 'todos.db'

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )''')

@app.route('/')
def index():
    with get_db() as conn:
        todos = conn.execute('SELECT * FROM todos').fetchall()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title', '').strip()
    if title:
        with get_db() as conn:
            conn.execute('INSERT INTO todos (title) VALUES (?)', (title,))
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>')
def complete(todo_id):
    with get_db() as conn:
        conn.execute('UPDATE todos SET done=1 WHERE id=?', (todo_id,))
    return redirect(url_for('index'))

@app.route('/undo/<int:todo_id>')
def undo(todo_id):
    with get_db() as conn:
        conn.execute('UPDATE todos SET done=0 WHERE id=?', (todo_id,))
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):
    with get_db() as conn:
        conn.execute('DELETE FROM todos WHERE id=?', (todo_id,))
    return redirect(url_for('index'))

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit(todo_id):
    with get_db() as conn:
        todo = conn.execute('SELECT * FROM todos WHERE id=?', (todo_id,)).fetchone()
    if request.method == 'POST':
        new_title = request.form.get('title', '').strip()
        if new_title:
            with get_db() as conn:
                conn.execute('UPDATE todos SET title=? WHERE id=?', (new_title, todo_id))
        return redirect(url_for('index'))
    return render_template('edit.html', todo=todo)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)