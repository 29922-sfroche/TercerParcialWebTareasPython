import base64
import mysql.connector
from flask import Flask, request

from constantes import SERVER, USER, PASS, BD
from routes.vehiculo import Vehiculo
from flask import send_from_directory
import os

app = Flask(__name__)

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


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "imagenes")


@app.route("/imagenes/<path:filename>")
def servir_imagenes(filename):
    return send_from_directory(IMAGES_DIR, filename)

def conectar():
    html = "<br>CONEXION A LA BASE DE DATOS<br>"
    cn = mysql.connector.connect(
        host=SERVER,
        user=USER,
        password=PASS,
        database=BD,
        charset="utf8"
    )
    html += "La conexión tuvo éxito ......<br><br>"
    return cn, html


@app.route("/", methods=["GET", "POST"])
def index():
    cn, debug_db = conectar()
    v = Vehiculo(cn)

    html = ""
    html += debug_db
    html += v.debug

    # ======================
    # POST GUARDAR (PRIMERO)
    # ======================
    if "Guardar" in request.form and request.form.get("placa"):
        html += "<br>PETICION POST<br>"
        html += "<pre>" + print_r_py(request.form.to_dict()) + "</pre>"
        html += "<br>GRABAR VEHICULO - PARTE III<br><br>"
        html += "<a href='/'>Regresar</a>"

        cn.close()
        return f"<html><body>{html}</body></html>" 


    # ======================
    # GET ?d=
    # ======================
    d = request.args.get("d")
    if d:
        html += "<br>PETICION GET<br>"
        html += "<pre>" + print_r_py(request.args.to_dict()) + "</pre>"

        dato = base64.b64decode(d).decode()
        tmp = dato.split("/")

        html += "<br>VARIABLE TEMP<br>"
        html += "<pre>" + print_r_py(tmp) + "</pre>"

        op, id = tmp
        id = int(id)

        if op == "act":
            html += v.get_form(id)
        elif op == "det":
            html += v.get_detail_vehiculo(id)
        elif op == "new":
            html += v.get_form()
        elif op == "del":
            html += v.delete_vehiculo(id)
        else:
            html += v.get_list()

    else:
        html += v.get_list()

    cn.close()
    return f"<html><body>{html}</body></html>"


