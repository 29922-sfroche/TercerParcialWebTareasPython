import base64
import mysql.connector
from flask import Flask, request
from Constantes import SERVER, USER, PASS, BD
from routes.vehiculo import vehiculo

app = Flask(__name__)

def conectar():
    return mysql.connector.connect(
        host=SERVER,
        user=USER,
        password=PASS,
        database=BD,
        charset="utf8"
    )

@app.route("/", methods=["GET","POST"])
def index():

    cn = conectar()
    v = vehiculo(cn)
    html = ""

    if "d" in request.args:
        try:
            dato = base64.b64decode(request.args["d"]).decode()
            op, id = dato.split("/")
        except Exception:
            cn.close()
            return "<html><body>" + v.get_list() + "</body></html>"


        if op == "del":
            html += v.delete_vehiculo(id)
        elif op == "det":
            html += v.get_detail_vehiculo(id)
        elif op == "new":
            html += v.get_form()
        elif op == "act":
            html += v.get_form(id)

    else:
        # Manejo de envío del formulario (crear o actualizar vehículo)
        if "Guardar" in request.form and request.form["op"] == "new":
            # La clase vehiculo usa directamente flask.request, por eso no se pasan parámetros
            html += v.save_vehiculo()
        elif "Guardar" in request.form and request.form["op"] == "update":
            html += v.update_vehiculo()
        else:
            html += v.get_list()

    cn.close()
    return f"<html><body>{html}</body></html>"

if __name__ == "__main__":
    app.run(debug=True)
