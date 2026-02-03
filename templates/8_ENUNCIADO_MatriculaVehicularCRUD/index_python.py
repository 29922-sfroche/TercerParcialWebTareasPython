# index.py
import base64
import mysql.connector
from constantes import SERVER, USER, PASS, BD
from routes.vehiculo import vehiculo
from routes.matricula import Matricula


# ===============================
# CONEXIÓN
# ===============================
def conectar():
    return mysql.connector.connect(
        host=SERVER,
        user=USER,
        password=PASS,
        database=BD,
        charset="utf8"
    )


# ===============================
# LÓGICA PRINCIPAL
# ===============================
def ejecutar_index(request):

    cn = conectar()
    v = vehiculo(cn)
    m = Matricula(cn)

    html = ""

    mod = request.args.get("mod", "vehiculo")

    # ===============================
    # VEHÍCULOS
    # ===============================
    if mod == "vehiculo":

        if "d" in request.args:
            dato = base64.b64decode(request.args["d"]).decode()
            op, id = dato.split("/")

            if op == "del":
                html += v.delete_vehiculo(id)
            elif op == "det":
                html += v.get_detail_vehiculo(id)
            elif op == "new":
                html += v.get_form(0)
            elif op == "act":
                html += v.get_form(id)

        else:
            if "Guardar" in request.form and request.form.get("op") == "new":
                html += v.save_vehiculo()
            elif "Guardar" in request.form and request.form.get("op") == "update":
                html += v.update_vehiculo()
            else:
                html += v.get_list()

    # ===============================
    # MATRÍCULAS
    # ===============================
    if mod == "matricula":

        if "d" in request.args:
            dato = base64.b64decode(request.args["d"]).decode()
            op, id = dato.split("/")

            if op == "del":
                html += m.delete_matricula(id)
            elif op == "det":
                html += m.get_detail_matricula(id)
            elif op == "new":
                html += m.get_form()
            elif op == "act":
                html += m.get_form(id)

        else:
            if "Guardar" in request.form and request.form.get("op") == "new":
                html += m.save_matricula()
            elif "Guardar" in request.form and request.form.get("op") == "update":
                html += m.update_matricula()
            else:
                html += m.get_list()

    cn.close()

    return f"""
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
    <ul class="navbar-nav ms-auto">
      <li class="nav-item">
        <a class="nav-link {'active' if mod=='vehiculo' else ''}"
           href="/index?mod=vehiculo">Vehículos</a>
      </li>
      <li class="nav-item">
        <a class="nav-link {'active' if mod=='matricula' else ''}"
           href="/index?mod=matricula">Matrículas</a>
      </li>
    </ul>
  </div>
</nav>

<div class="container mt-4">
  {html}
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""
