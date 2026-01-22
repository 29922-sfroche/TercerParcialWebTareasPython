from flask import Flask, request
import mysql.connector
import base64
import traceback

from routes.matricula import Matricula

app = Flask(__name__)

def conectar():
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
    op = tmp[0].strip()
    id_ = int(tmp[1]) if len(tmp) > 1 and tmp[1].isdigit() else 0
    return raw, tmp, op, id_

@app.route("/", methods=["GET", "POST"])
def index():
    dbg = ""

    try:
        cn = conectar()
        dbg += "<br>CONEXION A LA BASE DE DATOS<br>"
        dbg += "La conexión tuvo éxito .......<br><br>"

        m = Matricula(cn)
        dbg += "EJECUTANDOSE EL CONSTRUCTOR MATRICULA<br><br>"

        # ---------------- GET (Parte II) ----------------
        if "d" in request.args:
            dbg += "<br>PETICION GET<br><pre>{}</pre>".format(dict(request.args))

            raw, tmp, op, id_ = decode_d(request.args["d"])
            dbg += "<br>VARIABLE TEMP<br><pre>{}</pre>".format(tmp)

            if op == "det":
                return dbg + m.get_detail_matricula(id_)
            elif op == "del":
                return dbg + m.delete_matricula(id_)
            elif op == "act":
                return dbg + m.get_form(id_)
            elif op == "new":
                return dbg + m.get_form(0)  # NEW: formulario vacío
            else:
                return dbg + m.get_list()

        # ---------------- POST (solo muestra lo enviado) ----------------
        if request.method == "POST" and "Guardar" in request.form:
            dbg += "<br>PETICION POST ......<br>"
            dbg += "<pre>{}</pre>".format(dict(request.form))
            dbg += '<br><a href="/">Regresar</a>'
            return dbg

        # ---------------- LISTA ----------------
        return dbg + m.get_list()

    except Exception:
        # si algo falla, lo ves en la página (tipo depuración)
        return dbg + "<br><b>ERROR:</b><pre>{}</pre>".format(traceback.format_exc())

if __name__ == "__main__":
    app.run(debug=True)
