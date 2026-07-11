from flask import Flask
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

conexion = sqlite3.connect("usuarios.db", check_same_thread=False)
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

usuarios = [
    ("Catalina Castillo", "cata123"),
    ("Issac Herrera", "isa123"),
    ("Cristobal Sepulveda", "cris123")
]

for nombre, clave in usuarios:

    cursor.execute("SELECT * FROM usuarios WHERE nombre=?", (nombre,))

    if cursor.fetchone() is None:

        hash_password = generate_password_hash(clave)

        cursor.execute(
            "INSERT INTO usuarios(nombre,password) VALUES(?,?)",
            (nombre, hash_password)
        )

conexion.commit()


@app.route("/")
def inicio():
    return "<h2>Servidor funcionando correctamente.</h2>"


@app.route("/validar/<usuario>/<clave>")
def validar(usuario, clave):

    cursor.execute(
        "SELECT password FROM usuarios WHERE nombre=?",
        (usuario,)
    )

    dato = cursor.fetchone()

    if dato:

        if check_password_hash(dato[0], clave):
            return "Usuario y contraseña correctos"

    return "Usuario o contraseña incorrectos"


app.run(host="0.0.0.0", port=5800)