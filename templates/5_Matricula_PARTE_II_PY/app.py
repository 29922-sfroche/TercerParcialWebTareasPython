import base64
import mysql.connector
from flask import Flask, request, send_from_directory
import os

from constantes import SERVER, USER, PASS, BD
from routes.vehiculo import Vehiculo
from routes.matricula import Matricula

app = Flask(__name__)

# ======================================================
# print_r estilo PHP
# ======================================================
def print_r_py(data):
    salida = "Array\n(\n"
    if isinstance(data, dict):
        for k, v in data.items():
            salida += f"    [{k}] => {v}\n"
    elif isinstance(data, (list, tuple)):
        for i, v in enumerate(data):
            salida += f"    [{i}] => {v}\n"
    salida += ")\n"
    return salida

# ======================================================
# IMÁGENES
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "imagenes")

@app.route("/imagenes/<path:filename>")
def imagenes(filename):
    return send_from_directory(IMAGES_DIR, filename)

# ======================================================
# CONEXIÓN
# ======================================================
def conectar():
    html = "<br> CONEXION A LA BASE DE DATOS<br>"
    cn = mysql.connector.connect(
        host=SERVER,
        user=USER,
        password=PASS,
        database=BD,
        charset="utf8"
    )
    html += "La conexión tuvo éxito .......<br><br>"
    return cn, html

# ======================================================
# INDEX (IGUAL A index.php)
# ======================================================
@app.route("/", methods=["GET", "POST"])
def index():

    # -------------------------------
    # MODULO ACTIVO
    # -------------------------------
    mod = request.args.get("mod", "vehiculo")

    cn, debug_db = conectar()
    v = Vehiculo(cn)
    m = Matricula(cn)

    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>Ejercicios</title>

    <!-- BOOTSTRAP -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

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

<!-- NAVBAR -->
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
  <div class="container-fluid">

    <a class="navbar-brand" href="/">Ejercicios</a>

    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav ms-auto">
        <li class="nav-item">
          <a class="nav-link {'active' if mod=='vehiculo' else ''}" href="/?mod=vehiculo">Vehículos</a>
        </li>
        <li class="nav-item">
          <a class="nav-link {'active' if mod=='matricula' else ''}" href="/?mod=matricula">Matrículas</a>
        </li>
      </ul>
    </div>
  </div>
</nav>

<div class="container mt-4">
{debug_db}
"""

    # ======================
    # PETICION GET
    # ======================
    if request.args:
        html += "<br>PETICION GET<br>"
        html += "<pre>" + print_r_py(request.args.to_dict()) + "</pre>"

    # ======================
    # PETICION POST
    # ======================
    if request.form:
        html += "<br>PETICION POST<br>"
        html += "<pre>" + print_r_py(request.form.to_dict()) + "</pre>"

    # ======================
    # GET d=base64(op/id)
    # ======================
    d = request.args.get("d")
    if d:
        dato = base64.b64decode(d).decode()
        tmp = dato.split("/")

        html += "<br>VARIABLE TEMP<br>"
        html += "<pre>" + print_r_py(tmp) + "</pre>"

        op, id = tmp
        id = int(id)

        if mod == "vehiculo":
            if op == "det":
                html += v.get_detail_vehiculo(id)
            elif op == "del":
                html += v.delete_vehiculo(id)
            elif op == "act":
                html += v.get_form(id)
            elif op == "new":
                html += v.get_form()
            else:
                html += v.get_list()
        else:
            if op == "det":
                html += m.get_detail_matricula(id)
            elif op == "del":
                html += m.delete_matricula(id)
            elif op == "act":
                html += m.get_form(id)
            elif op == "new":
                html += m.get_form()
            else:
                html += m.get_list()

    # ======================
    # POST Guardar
    # ======================
    elif "Guardar" in request.form:
        html += "<br><a href='/?mod=" + mod + "' class='btn btn-secondary'>Regresar</a>"

    else:
        html += v.get_list() if mod == "vehiculo" else m.get_list()

    html += """
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

    cn.close()
    return html


if __name__ == "__main__":
    app.run(debug=True)
