from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def ver_notebook():

    marca = request.form.get("op")
    codigo = request.form.get(f"codigo_{marca}")
    precio = request.form.get(f"precio_{marca}")

    html = "<pre>VARIABLE POST:\n"
    html += str(request.form) + "</pre>"

    html += f"<h1>{marca}</h1>"
    html += f"Codigo: {codigo}<br>"
    html += f"Precio: ${precio}<br><br>"
    html += "<a href='index.py'>Volver</a>"

    return html
