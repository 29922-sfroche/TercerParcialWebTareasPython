from flask import Flask, render_template, request
import os
import sys

# Asegurar que la carpeta de este app (14_Tarea01) esté en sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Asegurar que la subcarpeta "routes" de este proyecto esté primero en sys.path
ROUTES_DIR = os.path.join(BASE_DIR, "routes")
if ROUTES_DIR not in sys.path:
    sys.path.insert(0, ROUTES_DIR)

from conexion import get_connection
from producto import Producto


app = Flask(
    __name__,
    template_folder="routes",   # Flask buscará index.html en la carpeta routes
    static_folder="routes",     # styles.css, app.js también en la carpeta routes
    static_url_path="/routes",  # se servirán como /routes/styles.css, /routes/app.js
)


@app.route("/", methods=["GET", "POST"])
def index():
    """Página principal: muestra el formulario y guarda en detalle_factura."""
    con = get_connection()
    mensaje_guardado = ""

    if request.method == "POST":
        # Caso 1: petición para eliminar un registro existente en la BD
        eliminar_id = request.form.get("eliminar_id")
        if eliminar_id:
            try:
                eliminar_id_int = int(eliminar_id)
            except ValueError:
                eliminar_id_int = 0

            if eliminar_id_int > 0:
                with con.cursor() as cur:
                    cur.execute(
                        "DELETE FROM detalle_factura WHERE id = %s",
                        (eliminar_id_int,),
                    )
                mensaje_guardado = "Registro eliminado correctamente."
        else:
            # Caso 2: guardar los productos enviados desde el formulario JS
            # En el JS los "name" son nombre[], precio[], cantidad[], total[]
            nombres = request.form.getlist("nombre[]")
            precios = request.form.getlist("precio[]")
            cantidades = request.form.getlist("cantidad[]")
            totales = request.form.getlist("total[]")

            insertados = 0

            with con.cursor() as cur:
                for i, nombre in enumerate(nombres):
                    if not nombre:
                        continue

                    try:
                        precio = float(precios[i]) if i < len(precios) and precios[i] else 0.0
                    except ValueError:
                        precio = 0.0

                    try:
                        cantidad = int(cantidades[i]) if i < len(cantidades) and cantidades[i] else 0
                    except ValueError:
                        cantidad = 0

                    # Si no viene total, lo calculamos
                    try:
                        total = float(totales[i]) if i < len(totales) and totales[i] else precio * cantidad
                    except (ValueError, TypeError):
                        total = precio * cantidad

                    if precio <= 0 or cantidad <= 0:
                        continue

                    cur.execute(
                        """
                        INSERT INTO detalle_factura (nombre, precio, cantidad, total)
                        VALUES (%s, %s, %s, %s)
                        """,
                        (nombre, precio, cantidad, total),
                    )

                    insertados += 1

            if insertados > 0:
                mensaje_guardado = f"Se guardaron {insertados} producto(s) en la base de datos."
            else:
                mensaje_guardado = "No se pudo guardar la información en la base de datos."

    # Llenar combo de productos (equivalente a $objProducto->get_select_options())
    obj_producto = Producto(con)
    opciones_productos = obj_producto.get_select_options()

    # Consultar todos los registros actuales de detalle_factura
    with con.cursor() as cur:
        cur.execute(
            "SELECT id, nombre, precio, cantidad, total FROM detalle_factura ORDER BY id DESC"
        )
        registros_guardados = cur.fetchall()

    con.close()

    return render_template(
        "index.html",
        mensaje_guardado=mensaje_guardado,
        opciones_productos=opciones_productos,
        registros_guardados=registros_guardados,
    )


if __name__ == "__main__":
    # Ejecutar con: python app.py
    # Luego abrir: http://127.0.0.1:5000/
    app.run(debug=True)
