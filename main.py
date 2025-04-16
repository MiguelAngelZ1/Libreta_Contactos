from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)


def init_db():
    with sqlite3.connect('libreta.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS contactos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                grado TEXT NOT NULL,
                nombre TEXT NOT NULL,
                dni TEXT NOT NULL
            )
        ''')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        grado = request.form['grado']
        nombre = request.form['nombre']
        dni = request.form['dni']
        try:
            with sqlite3.connect('libreta.db') as conn:
                c = conn.cursor()
                c.execute(
                    'INSERT INTO contactos (grado, nombre, dni) VALUES (?, ?, ?)',
                    (grado, nombre, dni))
        except Exception as e:
            print("❌ ERROR AL INSERTAR:", e)
        return redirect('/')

    with sqlite3.connect('libreta.db') as conn:
        c = conn.cursor()
        c.execute('SELECT grado, nombre, dni FROM contactos')
        contactos = c.fetchall()
    return render_template('index.html', contactos=contactos)


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=3000, debug=True)
