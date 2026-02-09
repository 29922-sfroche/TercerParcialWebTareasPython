from flask import Flask, request, session, redirect, url_for
from flask import render_template_string
import base64

from routes.tienda import Tienda, conectar

app = Flask(__name__)
app.secret_key = "cambia-esta-clave-super-secreta"  # Cambia esto en producción


PAGE_TEMPLATE = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
    <title>Carrito de compras</title>
    <meta http-equiv="content-type" content="text/html;charset=utf-8" />
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" />
</head>
<body class="bg-light">
    <div class="container py-5">
        {{ content|safe }}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""


@app.route("/", methods=["GET", "POST"])
def index():
    conn = conectar()
    # Para POST pasamos el formulario, de modo que Tienda
    # pueda reconstruir el carrito desde los campos ocultos.
    tienda = Tienda(conn, request.form if request.method == "POST" else None)

    msg = ""
    edit_id = None

    if request.method == "GET" and "d" in request.args:
        # Ruta antigua basada en GET; con el nuevo manejo sin estado
        # del carrito ya no se utiliza, pero se deja por compatibilidad.
        dato = base64.b64decode(request.args.get("d")).decode()
        tmp = dato.split("/")
        op = tmp[0]
        id_ = tmp[1]
        if op == "del":
            msg = tienda.delete_item(id_)
        elif op == "act":
            edit_id = id_
    elif request.method == "POST":
        op = request.form.get("op", "")
        if "BuscarCliente" in request.form and op == "client_search":
            msg = tienda.client_search(request.form)
        elif "GuardarCliente" in request.form and op == "client_create":
            msg = tienda.client_create(request.form)
        elif "Agregar" in request.form and op == "add":
            msg = tienda.add_item(request.form)
        elif "Actualizar" in request.form and op == "update":
            msg = tienda.update_item(request.form)
        elif op == "cart_del" and "item_id" in request.form:
            msg = tienda.delete_item(request.form.get("item_id"))
        elif op == "cart_edit" and "item_id" in request.form:
            edit_id = request.form.get("item_id")
        elif "GuardarPedido" in request.form and op == "save":
            # Pasamos el formulario para que save_pedido pueda recuperar el cliente
            # a partir del rif enviado, incluso si la sesión se perdió.
            msg = tienda.save_pedido(request.form)
        elif "LimpiarOrden" in request.form and op == "clear_cart":
            msg = tienda.clear_cart()
        elif "BuscarCompras" in request.form and op == "hist_search":
            msg = tienda.hist_search(request.form)
        elif "VerCompra" in request.form and op == "hist_view":
            msg = tienda.hist_view(request.form)
        elif "LimpiarHistorial" in request.form and op == "hist_clear":
            msg = tienda.hist_clear()

    content = tienda.get_page(msg, edit_id)
    conn.close()
    return render_template_string(PAGE_TEMPLATE, content=content)


if __name__ == "__main__":
    app.run(debug=True)
