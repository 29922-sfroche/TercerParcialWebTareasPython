from flask import Flask
import mysql.connector

from routes.vehiculo import Vehiculo
from routes.matricula import Matricula

app = Flask(__name__)

def conectar():
    cn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="matriculacionfinal",
        port=3306,
    )

    # ✅ Compatible con distintas versiones
    try:
        cn.set_charset_collation(charset="utf8")
    except Exception:
        try:
            cur = cn.cursor()
            cur.execute("SET NAMES utf8")
            cur.close()
        except Exception:
            pass

    return cn

@app.route("/")
def index():
    try:
        cn = conectar()

        objVehiculo = Vehiculo(cn)
        objMatricula = Matricula(cn)

        html = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="utf-8">
            <title>Matriculas Vehículos</title>
        </head>
        <body>
        """

        html += objVehiculo.get_list()
        html += "<br><hr><br>"
        html += objMatricula.get_list()

        html += """
        </body>
        </html>
        """

        cn.close()
        return html

    except Exception as e:
        return f"""
        <h1>Error en app.py</h1>
        <pre>{str(e)}</pre>
        """, 500

