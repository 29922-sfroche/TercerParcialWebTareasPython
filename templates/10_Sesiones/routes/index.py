from flask import Flask
import mysql.connector
from Notebook import Notebook

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():

    html = """
    <html>
    <head>
        <meta charset="utf-8">
        <title>Sesiones en Python</title>
    </head>
    <body>
        <table border="0" style="width:100%">
            <tr>
                <th colspan="3">
                    <a href="../app.py">Página principal</a>
                </th>
            </tr>
        </table>
    """

    # ==========================
    # CONEXIÓN A LA BASE DE DATOS
    # ==========================
    cn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="SesionesBD"
    )

    cursor = cn.cursor(dictionary=True)
    cursor.execute("SELECT Codigo, Marca, Precio FROM notebook")

    notebooks = {}

    for fila in cursor.fetchall():
        obj = Notebook(
            fila["Codigo"],
            fila["Marca"],
            fila["Precio"]
        )
        notebooks[fila["Marca"]] = obj

    cn.close()

    # ==========================
    # TABLA DE NOTEBOOKS
    # ==========================
    html += "<h1>Recorrer un vector con foreach</h1>"
    html += "<table border='1'>"
    html += "<tr><th>Codigo</th><th>Marca</th><th>Precio</th></tr>"

    for obj in notebooks.values():
        html += f"""
        <tr>
            <td>{obj.getCodigo()}</td>
            <td>{obj.getMarca()}</td>
            <td>{obj.getPrecio()}</td>
        </tr>
        """

    html += "</table><br><br>"

    # ==========================
    # FORMULARIO (SIMULA SESIÓN)
    # ==========================
    html += "<form action='verNotebook.py' method='POST'>"

    # Inputs ocultos (equivalente a $_SESSION)
    for obj in notebooks.values():
        html += f"""
            <input type="hidden" name="codigo_{obj.getMarca()}" value="{obj.getCodigo()}">
            <input type="hidden" name="precio_{obj.getMarca()}" value="{obj.getPrecio()}">
        """

    html += "<select name='op'>"

    for obj in notebooks.values():
        html += f"<option value='{obj.getMarca()}'>{obj.getMarca()}</option>"

    html += "</select>"
    html += "<button type='submit'>consultar</button>"
    html += "</form>"

    html += "</body></html>"
    return html
