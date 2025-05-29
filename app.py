from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "datos.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # para acceder por nombre de columna
    return conn

# Crear tabla si no existe
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS datos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            correo TEXT NOT NULL,
            telefono TEXT
        )
    ''')
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def formulario():
    if request.method == "POST":
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        telefono = request.form.get("telefono")

        conn = get_db_connection()
        conn.execute("INSERT INTO datos (nombre, correo, telefono) VALUES (?, ?, ?)",
                     (nombre, correo, telefono))
        conn.commit()
        conn.close()

        return redirect("/datos")

    return render_template("formulario.html")

@app.route("/datos")
def mostrar_datos():
    conn = get_db_connection()
    datos = conn.execute("SELECT * FROM datos").fetchall()
    conn.close()
    return render_template("datos.html", datos=datos)

if __name__ == "__main__":
    init_db()
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
