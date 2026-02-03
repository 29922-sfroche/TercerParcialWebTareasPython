# app.py
import base64
import mysql.connector
from flask import Flask, request

from constantes import SERVER, USER, PASS, BD
from routes.vehiculo import vehiculo
from routes.matricula import Matricula
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    static_url_path="/imagenes",
    static_folder=os.path.join(BASE_DIR, "imagenes")
)

app = Flask(__name__)

# ===============================
# CONEXIÓN
# ===============================
def conectar():
    cn = mysql.connector.connect(
        host=SERVER,
        user=USER,
        password=PASS,
        database=BD,
        charset="utf8"
    )
    return cn


@app.route("/", methods=["GET", "POST"])
def index():

    cn = conectar()
    v = vehiculo(cn)
    m = Matricula(cn)

    html = ""

    # ===============================
    # MÓDULO ACTIVO
    # ===============================
    mod = request.args.get("mod", "vehiculo")

    # ===============================
    # NAVBAR (igual que PHP)
    # ===============================
    html += f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <title>Vehículos y Matrículas</title>

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

        <style>
            table {{
                border-collapse: collapse !important;
                border: 1px solid black !important;
            }}
            th, td {{
                border: 1px solid black !important;
                padding: 6px;
            }}
            th {{
                font-weight: bold !important;
            }}
        </style>
    </head>
    <body>

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container-fluid">

        <a class="navbar-brand" href="/">Ejercicios</a>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto"></ul>
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link {"active" if mod=="vehiculo" else ""}" href="/?mod=vehiculo">
                Vehículos
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link {"active" if mod=="matricula" else ""}" href="/?mod=matricula">
                Matrículas
              </a>
            </li>
          </ul>
        </div>

      </div>
    </nav>

    <div class="container mt-4">
    """

    # =========================================================
    # VEHÍCULOS
    # =========================================================
    if mod == "vehiculo":

        if "d" in request.args:
            try:
                dato = base64.b64decode(request.args["d"]).decode()
                op, id = dato.split("/")
            except:
                html += v.get_list()
            else:
                if op == "del":
                    html += v.delete_vehiculo(id)
                elif op == "det":
                    html += v.get_detail_vehiculo(id)
                elif op == "new":
                    html += v.get_form()
                elif op == "act":
                    html += v.get_form(id)

        else:
            if "Guardar" in request.form and request.form["op"] == "new":
                html += v.save_vehiculo()
            elif "Guardar" in request.form and request.form["op"] == "update":
                html += v.update_vehiculo()
            else:
                html += v.get_list()

    # =========================================================
    # MATRÍCULAS
    # =========================================================
    if mod == "matricula":

        if "d" in request.args:
            try:
                dato = base64.b64decode(request.args["d"]).decode()
                op, id = dato.split("/")
            except:
                html += m.get_list()
            else:
                if op == "del":
                    html += m.delete_matricula(id)
                elif op == "det":
                    html += m.get_detail_matricula(id)
                elif op == "new":
                    html += m.get_form()
                elif op == "act":
                    html += m.get_form(id)

        else:
            if "Guardar" in request.form and request.form["op"] == "new":
                html += m.save_matricula()
            elif "Guardar" in request.form and request.form["op"] == "update":
                html += m.update_matricula()
            else:
                html += m.get_list()

    html += """
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """

    cn.close()
    return html


if __name__ == "__main__":
    app.run(debug=True)
