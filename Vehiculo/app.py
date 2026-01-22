from flask import Flask, request
import base64
import mysql.connector
from routes.vehiculo import Vehiculo

app = Flask(__name__, static_url_path="", static_folder=".")


def conectar():
    # NO imprime en terminal, solo retorna conexión
    cn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="matriculacionfinal"
    )
    return cn

def decode_d(value: str):
    raw = base64.b64decode(value).decode("utf-8")
    tmp = raw.split("/")
    op = tmp[0]
    id_ = int(tmp[1]) if len(tmp) > 1 and tmp[1].isdigit() else 0
    return raw, tmp, op, id_

@app.route("/", methods=["GET", "POST"])
def index():
    cn = conectar()

    # debug en página (como tus echo en PHP)
    dbg = ""
    dbg += "<br>CONEXION A LA BASE DE DATOS<br>"
    dbg += "La conexión tuvo éxito .......<br><br>"

    v = Vehiculo(cn)
    dbg += "EJECUTANDOSE EL CONSTRUCTOR VEHICULO<br><br>"

    # ---------------- GET ----------------
    if "d" in request.args:
        dbg += "<br>PETICION GET<br><pre>{}</pre>".format(dict(request.args))

        try:
            raw, tmp, op, id_ = decode_d(request.args.get("d", ""))
            dbg += "<br>VARIABLE TEMP<br><pre>{}</pre>".format(tmp)
        except Exception as e:
            return dbg + "<b>Error decodificando d:</b> {}<br><a href='/'>Regresar</a>".format(e)

        if op == "det":
            return dbg + v.get_detail_vehiculo(id_)
        elif op == "del":
            return dbg + v.delete_vehiculo(id_)
        elif op == "act":
            return dbg + v.get_form(id_)
        elif op == "new":
            return dbg + v.get_form(0)
        else:
            return dbg + v.get_list()

    # ---------------- POST ----------------
    if request.method == "POST":
        if "Guardar" in request.form:
            dbg += "<br>PETICION POST ......<br><pre>{}</pre>".format(dict(request.form))
            dbg += "<a href='/'>Regresar</a>"
            return dbg

    # ---------------- LIST ----------------
    return dbg + v.get_list()


if __name__ == "__main__":
    app.run(debug=True)
