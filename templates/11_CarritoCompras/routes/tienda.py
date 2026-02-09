from datetime import datetime
from decimal import Decimal
from flask import session
import pymysql
import json
import base64

from routes.constantes import SERVER, USER, PASS, BD, PORT


def conectar():
    conn = pymysql.connect(
        host=SERVER,
        user=USER,
        password=PASS,
        database=BD,
        port=PORT,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )
    return conn


class Tienda:
    def __init__(self, conn, form=None):
        self.con = conn

        # Reconstruir carrito desde el formulario si viene serializado
        if form is not None:
            raw_cart = form.get("cart_data", "").strip()
            if raw_cart:
                try:
                    data_json = base64.b64decode(raw_cart.encode("utf-8")).decode(
                        "utf-8"
                    )
                    cart = json.loads(data_json)
                    if isinstance(cart, dict):
                        session["cart"] = cart
                except Exception:
                    # Si algo falla al parsear, simplemente ignoramos y seguimos
                    pass

            # Intentar reconstruir también los datos del cliente a partir de rif_cliente
            # para que al pulsar "Editar" no se pierda el cliente seleccionado
            try:
                rif = form.get("rif_cliente", "").strip()
                if rif and int(session.get("cliente_id", 0)) <= 0:
                    with self.con.cursor() as cur:
                        cur.execute(
                            "SELECT ClienteID, RazonSocial, Rif FROM Clientes WHERE Rif=%s LIMIT 1;",
                            (rif,),
                        )
                        row_cli = cur.fetchone()
                    if row_cli:
                        session["cliente_id"] = int(row_cli["ClienteID"])
                        session["cliente_rif"] = row_cli["Rif"]
                        session["cliente_nombre"] = row_cli["RazonSocial"] or ""
            except Exception:
                # Si algo falla, simplemente no rellenamos datos de cliente
                pass

        if "cart" not in session:
            session["cart"] = {}

        session.setdefault("cliente_id", 0)
        session.setdefault("cliente_rif", "")
        session.setdefault("cliente_nombre", "")

        session.setdefault("ui_show_client_modal", 0)
        session.setdefault("ui_new_rif", "")

        if "hist" not in session:
            session["hist"] = {
                "rif": "",
                "cliente_id": 0,
                "razon": "",
                "pedidos": [],
                "pedido_sel": 0,
                "items": [],
            }

    # *************************************** HELPERS ************************************************************

    def _message_error_inline(self, tipo: str) -> str:
        return f'<div class="alert alert-danger" role="alert">Error: {tipo}</div>'

    def _message_ok_inline(self, tipo: str) -> str:
        return f'<div class="alert alert-success" role="alert">{tipo}</div>'

    def _cart_total(self) -> Decimal:
        total = Decimal("0")
        for pid, it in session["cart"].items():
            precio = Decimal(str(it.get("precio", 0)))
            cantidad = int(it.get("cantidad", 0))
            total += precio * cantidad
        return total

    def _cliente_locked(self) -> bool:
        return len(session["cart"]) > 0

    def _get_combo_productos(self, nombre, defecto, disabled=None):
        disabled_attr = disabled or ""
        html = f'<select class="form-select" name="{nombre}" {disabled_attr}>'
        with self.con.cursor() as cur:
            cur.execute("SELECT ProductoID, Descripcion FROM Productos;")
            for row in cur.fetchall():
                val = int(row["ProductoID"])
                lab = row["Descripcion"]
                if defecto == val:
                    html += f'<option value="{val}" selected>{lab}</option>\n'
                else:
                    html += f'<option value="{val}">{lab}</option>\n'
        html += "</select>"
        return html

    # *************************************** CLIENTE *************************************************************

    def client_search(self, form):
        rif = form.get("rif_cliente", "").strip()
        if rif == "":
            return self._message_error_inline("Ingrese la cédula del cliente.")

        if self._cliente_locked():
            return ""

        with self.con.cursor() as cur:
            cur.execute(
                "SELECT ClienteID, RazonSocial, Rif FROM Clientes WHERE Rif=%s LIMIT 1;",
                (rif,),
            )
            row = cur.fetchone()

        if not row:
            session["cliente_id"] = 0
            session["cliente_rif"] = rif
            session["cliente_nombre"] = ""

            session["ui_new_rif"] = rif
            session["ui_show_client_modal"] = 1
            return ""

        session["cliente_id"] = int(row["ClienteID"])
        session["cliente_rif"] = row["Rif"]
        session["cliente_nombre"] = row["RazonSocial"] or ""
        session["ui_show_client_modal"] = 0
        session["ui_new_rif"] = ""
        return ""

    def client_create(self, form):
        if self._cliente_locked():
            return ""

        rif = form.get("Rif", "").strip()
        raz = form.get("RazonSocial", "").strip()
        dir_ = form.get("Direccion", "").strip()
        ciu = form.get("Ciudad", "").strip()
        est = form.get("Estado", "").strip()
        cp = form.get("CodigoPostal", "").strip()
        pai = form.get("Pais", "").strip()
        tel = form.get("Telefono", "").strip()

        if rif == "":
            session["ui_new_rif"] = rif
            session["ui_show_client_modal"] = 1
            return self._message_error_inline("Cédula inválida.")

        if raz == "":
            session["ui_new_rif"] = rif
            session["ui_show_client_modal"] = 1
            return self._message_error_inline(
                "Debe ingresar el Nombre / Razón Social."
            )

        with self.con.cursor() as cur:
            cur.execute(
                "SELECT ClienteID, RazonSocial FROM Clientes WHERE Rif=%s LIMIT 1;",
                (rif,),
            )
            row0 = cur.fetchone()
            if row0:
                session["cliente_id"] = int(row0["ClienteID"])
                session["cliente_rif"] = rif
                session["cliente_nombre"] = row0["RazonSocial"] or raz
                session["ui_show_client_modal"] = 0
                session["ui_new_rif"] = ""
                return ""

            cur.execute(
                """
                INSERT INTO Clientes
                (RazonSocial, Direccion, Ciudad, Estado, CodigoPostal, Rif, Pais, Telefonos)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
                """,
                (raz, dir_, ciu, est, cp, rif, pai, tel),
            )
            self.con.commit()
            new_id = cur.lastrowid

        session["cliente_id"] = int(new_id)
        session["cliente_rif"] = rif
        session["cliente_nombre"] = raz
        session["ui_show_client_modal"] = 0
        session["ui_new_rif"] = ""
        return ""

    # *************************************** PAGE ***************************************************************

    def get_page(self, msg="", edit_id=None):
        from markupsafe import escape

        op = "add"
        btn_name = "Agregar"
        qty_def = 1
        prod_def = None
        disabled_prod = None

        cart = session.get("cart", {})

        # Serializar carrito actual para enviarlo en formularios (base64 + JSON)
        try:
            cart_json = json.dumps(cart)
            cart_encoded = base64.b64encode(cart_json.encode("utf-8")).decode("utf-8")
        except Exception:
            cart_encoded = ""

        if edit_id is not None:
            eid = int(edit_id)
            if str(eid) in cart:
                op = "update"
                btn_name = "Actualizar"
                qty_def = int(cart[str(eid)]["cantidad"])
                prod_def = eid
                disabled_prod = "disabled"
            else:
                edit_id = None

        cliente_locked = self._cliente_locked()
        cliente_id = int(session.get("cliente_id", 0))
        cliente_rif = session.get("cliente_rif", "")
        cliente_nombre = session.get("cliente_nombre", "")

        hist = session.get("hist", {})
        rif_hist = hist.get("rif", "")
        razon_hist = hist.get("razon", "")
        items = hist.get("items", [])

        html = ""
        html += "<div class=\"card shadow-sm border-0\">"
        html += "<div class=\"card-body\">"
        html += (
            "<div class=\"d-flex flex-column flex-md-row align-items-md-center "
            "justify-content-between mb-4\">"
            "<h2 class=\"h3 mb-2 mb-md-0 text-primary fw-bold\">Carrito de compras</h2>"
            "<p class=\"text-muted mb-0 small\">Administra el pedido actual y revisa el historial de compras.</p>"
            "</div>"
        )

        if msg:
            html += msg

        html += "<div class=\"row g-4\">"
        # IZQUIERDA
        html += "<div class=\"col-12 col-lg-7\">"

        disable_cliente = "disabled" if cliente_locked else ""

        html += f"""
        <div class="card mb-3">
            <div class="card-body">
                <h5 class="mb-3">Cliente</h5>
                <form class="row g-2" method="POST" action="/">
                    <input type="hidden" name="op" value="client_search">

                    <div class="col-12 col-md-7">
                        <label class="form-label">Cédula (Rif)</label>
                        <input class="form-control" type="text" name="rif_cliente" value="{escape(cliente_rif)}" {disable_cliente} required>
                    </div>

                    <div class="col-12 col-md-5 d-flex align-items-end">
                        <button type="submit" class="btn btn-primary w-100" name="BuscarCliente" value="BuscarCliente" {disable_cliente}>Buscar</button>
                    </div>

                    <div class="col-12">
                        <label class="form-label">Nombre</label>
                        <input class="form-control" type="text" value="{escape(cliente_nombre)}" readonly>
                    </div>
                </form>
            </div>
        </div>
        """

        if int(session.get("ui_show_client_modal", 0)) == 1 and session.get(
            "ui_new_rif", ""
        ):
            newrif = escape(session["ui_new_rif"])
            html += f"""
        <div class="alert alert-warning mb-2">Cliente no encontrado. Registrar nuevo cliente.</div>
        <div class="card mb-3">
          <div class="card-body">
            <h5 class="mb-3">Registrar nuevo cliente</h5>
            <form method="POST" action="/" class="row g-3">
              <input type="hidden" name="op" value="client_create">

              <div class="col-12 col-md-4">
                <label class="form-label">Cédula (Rif)</label>
                <input class="form-control" type="text" name="Rif" value="{newrif}" readonly>
              </div>

              <div class="col-12 col-md-8">
                <label class="form-label">Nombre</label>
                <input class="form-control" type="text" name="RazonSocial" required>
              </div>

              <div class="col-12">
                <label class="form-label">Dirección</label>
                <input class="form-control" type="text" name="Direccion">
              </div>

              <div class="col-12 col-md-6">
                <label class="form-label">Ciudad</label>
                <input class="form-control" type="text" name="Ciudad">
              </div>

              <div class="col-12 col-md-6">
                <label class="form-label">Provincia</label>
                <input class="form-control" type="text" name="Estado">
              </div>

              <div class="col-12 col-md-4">
                <label class="form-label">Código Postal</label>
                <input class="form-control" type="text" name="CodigoPostal">
              </div>

              <div class="col-12 col-md-4">
                <label class="form-label">País</label>
                <input class="form-control" type="text" name="Pais" value="Ecuador">
              </div>

              <div class="col-12 col-md-4">
                <label class="form-label">Teléfonos</label>
                <input class="form-control" type="text" name="Telefono">
              </div>

              <div class="col-12 d-flex gap-2">
                <button type="submit" class="btn btn-success" name="GuardarCliente" value="GuardarCliente">Guardar Cliente</button>
              </div>
            </form>
          </div>
        </div>
        """

        disable_add = "disabled" if cliente_id <= 0 else ""
        edit_hidden = "" if edit_id is None else int(edit_id)
        prod_select = self._get_combo_productos(
            "productoCMB", prod_def, (disabled_prod or "") + " " + disable_add
        )

        html += f"""
        <form class="row g-3 mb-3" method="POST" action="/">
            <input type="hidden" name="op" value="{op}">
            <input type="hidden" name="edit_id" value="{edit_hidden}">
            <input type="hidden" name="rif_cliente" value="{escape(cliente_rif)}">
            <input type="hidden" name="cart_data" value="{cart_encoded}">

            <div class="col-12 col-md-8">
                <label class="form-label">Producto</label>
                {prod_select}
            </div>

            <div class="col-12 col-md-4">
                <label class="form-label">Cantidad</label>
                <input class="form-control" type="number" min="1" name="cantidad" value="{qty_def}" required {disable_add}>
            </div>

            <div class="col-12 d-flex gap-2">
                <button type="submit" class="btn btn-success" name="{btn_name}" value="{btn_name}" {disable_add}>{btn_name}</button>
        """

        if op == "update":
            html += '<a class="btn btn-secondary" href="/">Cancelar</a>'

        html += "</div></form>"

        # Tabla carrito
        html += """
        <div class="table-responsive">
        <table class="table table-bordered table-striped align-middle">
            <thead class="table-dark">
                <tr>
                    <th>Producto</th>
                    <th class="text-end">Precio</th>
                    <th class="text-center">Cantidad</th>
                    <th class="text-end">Subtotal</th>
                    <th class="text-center" style="width:200px;">Acciones</th>
                </tr>
            </thead>
            <tbody>
        """

        if len(cart) == 0:
            html += (
                '<tr><td colspan="5" class="text-center">No has agregado ' "productos todavía.</td></tr>"
            )
        else:
            for pid, it in cart.items():
                pid_i = int(pid)
                desc = it["descripcion"]
                precio = Decimal(str(it["precio"]))
                cant = int(it["cantidad"])
                sub = precio * cant

                html += f"""
                <tr>
                    <td>{desc}</td>
                    <td class="text-end">${precio:.2f}</td>
                    <td class="text-center">{cant}</td>
                    <td class="text-end">${sub:.2f}</td>
                    <td class="text-center">
                        <form method="POST" action="/" style="display:inline-block; margin-right:4px;">
                            <input type="hidden" name="op" value="cart_edit">
                            <input type="hidden" name="item_id" value="{pid_i}">
                            <input type="hidden" name="rif_cliente" value="{escape(cliente_rif)}">
                            <input type="hidden" name="cart_data" value="{cart_encoded}">
                            <button type="submit" class="btn btn-sm btn-primary">Editar</button>
                        </form>
                        <form method="POST" action="/" style="display:inline-block;">
                            <input type="hidden" name="op" value="cart_del">
                            <input type="hidden" name="item_id" value="{pid_i}">
                            <input type="hidden" name="rif_cliente" value="{escape(cliente_rif)}">
                            <input type="hidden" name="cart_data" value="{cart_encoded}">
                            <button type="submit" class="btn btn-sm btn-danger">Borrar</button>
                        </form>
                    </td>
                </tr>
                """

        total = self._cart_total()
        html += f"""
            </tbody>
            <tfoot>
                <tr>
                    <th class="text-end" colspan="3">TOTAL</th>
                    <th class="text-end">${total:.2f}</th>
                    <th></th>
                </tr>
            </tfoot>
        </table>
        </div>
        """

        disable_cart_btns = "disabled" if len(cart) == 0 else ""
        html += f"""
        <div class="d-flex gap-2 mt-2">
            <form method="POST" action="/">
                <input type="hidden" name="op" value="save">
                <input type="hidden" name="rif_cliente" value="{escape(cliente_rif)}">
                <input type="hidden" name="cart_data" value="{cart_encoded}">
                <button type="submit" class="btn btn-dark" name="GuardarPedido" value="GuardarPedido" {disable_cart_btns}>Guardar Pedido</button>
            </form>

            <form method="POST" action="/">
                <input type="hidden" name="op" value="clear_cart">
                <input type="hidden" name="cart_data" value="{cart_encoded}">
                <button type="submit" class="btn btn-outline-danger" name="LimpiarOrden" value="LimpiarOrden" {disable_cart_btns}>Limpiar orden</button>
            </form>
        </div>
        """

        html += "</div>"  # izquierda

        # DERECHA HISTORIAL
        html += "<div class=\"col-12 col-lg-5\">"
        html += f"""
        <div class="card border-0 shadow-sm bg-white">
            <div class="card-body">
                <h5 class="mb-3">Historial de compras</h5>

                <form class="row g-2 mb-2" method="POST" action="/">
                    <input type="hidden" name="op" value="hist_search">
                    <div class="col-12">
                        <label class="form-label">Buscar por Cédula (Rif)</label>
                        <input class="form-control" type="text" name="rif" value="{escape(rif_hist)}" required>
                    </div>
                    <div class="col-12">
                        <button type="submit" class="btn btn-primary w-100" name="BuscarCompras" value="BuscarCompras">Buscar</button>
                    </div>
                </form>

                <form class="row g-2 mb-3" method="POST" action="/">
                    <input type="hidden" name="op" value="hist_clear">
                    <div class="col-12">
                        <button type="submit" class="btn btn-outline-secondary w-100" name="LimpiarHistorial" value="LimpiarHistorial">Limpiar</button>
                    </div>
                </form>
        """

        if razon_hist:
            html += f"<div class=\"mb-2\"><strong>Cliente:</strong> {escape(razon_hist)}</div>"

        if items:
            from decimal import Decimal as D

            tot_hist = D("0")
            html += """
                <div class="table-responsive">
                <table class="table table-sm table-bordered align-middle">
                    <thead class="table-dark">
                        <tr>
                            <th>Fecha</th>
                            <th>Producto</th>
                            <th class="text-end">Precio</th>
                            <th class="text-center">Cant.</th>
                            <th class="text-end">Subt.</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            for it in items:
                desc = it["Descripcion"]
                precio = D(str(it["Precio"]))
                cant = int(it["Cantidad"])
                fecha = it["FechaPedido"]
                sub = precio * cant
                tot_hist += sub

                html += f"""
                        <tr>
                            <td>{fecha}</td>
                            <td>{desc}</td>
                            <td class="text-end">${precio:.2f}</td>
                            <td class="text-center">{cant}</td>
                            <td class="text-end">${sub:.2f}</td>
                        </tr>
                """
            html += f"""
                    </tbody>
                    <tfoot>
                        <tr>
                            <th class="text-end" colspan="4">TOTAL</th>
                            <th class="text-end">${tot_hist:.2f}</th>
                        </tr>
                    </tfoot>
                </table>
                </div>
            """

        html += "</div></div>"  # card-body, card
        html += "</div>"  # derecha
        html += "</div>"  # row
        html += "</div>"  # card-body
        html += "</div>"  # card
        return html

    # *************************************** COMPRA ACTUAL ********************************************************

    def _ensure_cliente_from_form(self, form):
        """Obtiene/valida el cliente usando la sesión o el rif del formulario.

        Esto permite que el flujo funcione aunque la sesión de Flask se pierda
        entre peticiones (por ejemplo, si se usa un cargador/proxy externo).
        """
        cliente_id = int(session.get("cliente_id", 0))
        if cliente_id > 0:
            return cliente_id, None

        rif = form.get("rif_cliente", "").strip()
        if rif == "":
            return 0, self._message_error_inline("Primero busque un cliente por cédula.")

        with self.con.cursor() as cur:
            cur.execute(
                "SELECT ClienteID, RazonSocial, Rif FROM Clientes WHERE Rif=%s LIMIT 1;",
                (rif,),
            )
            row = cur.fetchone()

        if not row:
            return 0, self._message_error_inline("No existe cliente con esa cédula (Rif).")

        cliente_id = int(row["ClienteID"])
        session["cliente_id"] = cliente_id
        session["cliente_rif"] = row["Rif"]
        session["cliente_nombre"] = row["RazonSocial"] or ""
        return cliente_id, None

    def add_item(self, form):
        cliente_id, err = self._ensure_cliente_from_form(form)
        if err is not None:
            return err

        pid = int(form.get("productoCMB", 0))
        cant = int(form.get("cantidad", 0))

        if pid <= 0 or cant <= 0:
            return self._message_error_inline(
                "Debe seleccionar un producto y una cantidad válida."
            )

        with self.con.cursor() as cur:
            cur.execute(
                "SELECT ProductoID, Descripcion, Precio, Imagen, Detalles FROM Productos WHERE ProductoID=%s;",
                (pid,),
            )
            row = cur.fetchone()

        if not row:
            return self._message_error_inline("Producto no encontrado.")

        cart = session.get("cart", {})
        key = str(pid)
        if key in cart:
            cart[key]["cantidad"] += cant
        else:
            cart[key] = {
                "producto_id": int(row["ProductoID"]),
                "descripcion": row["Descripcion"],
                "precio": float(row["Precio"]),
                "imagen": row.get("Imagen"),
                "detalles": row.get("Detalles"),
                "cantidad": cant,
            }
        session["cart"] = cart
        return self._message_ok_inline("Producto agregado correctamente.")

    def update_item(self, form):
        cliente_id, err = self._ensure_cliente_from_form(form)
        if err is not None:
            return err

        edit_id = int(form.get("edit_id", 0))
        cant = int(form.get("cantidad", 0))

        cart = session.get("cart", {})
        key = str(edit_id)
        if edit_id <= 0 or key not in cart:
            return ""
        if cant <= 0:
            return self._message_error_inline("Cantidad inválida.")

        cart[key]["cantidad"] = cant
        session["cart"] = cart
        return self._message_ok_inline("Cantidad actualizada correctamente.")

    def delete_item(self, id_):
        pid = int(id_)
        cart = session.get("cart", {})
        key = str(pid)
        if key in cart:
            del cart[key]
            session["cart"] = cart
        return ""

    def clear_cart(self):
        session["cart"] = {}
        session["cliente_id"] = 0
        session["cliente_rif"] = ""
        session["cliente_nombre"] = ""
        return ""

    def save_pedido(self, form=None):
        # form puede ser None si se llama desde código antiguo;
        # en ese caso seguimos usando solo la sesión.
        if form is not None:
            cliente_id, err = self._ensure_cliente_from_form(form)
            if err is not None:
                return err
        else:
            cliente_id = int(session.get("cliente_id", 0))

        cart = session.get("cart", {})

        if cliente_id <= 0:
            return self._message_error_inline("Primero busque un cliente por cédula.")
        if not cart:
            return self._message_error_inline("No hay productos para guardar.")

        try:
            with self.con.cursor() as cur:
                cur.execute(
                    "INSERT INTO Pedidos (ClienteID, FechaPedido) VALUES (%s, NOW());",
                    (cliente_id,),
                )
                pedido_id = cur.lastrowid

                for pid, it in cart.items():
                    pid_i = int(pid)
                    cant = int(it["cantidad"])
                    cur.execute(
                        "INSERT INTO PedidosItems (PedidoID, ProductoID, Cantidad) VALUES (%s,%s,%s);",
                        (pedido_id, pid_i, cant),
                    )
            self.con.commit()
        except Exception:
            self.con.rollback()
            return self._message_error_inline("No se pudo guardar el pedido.")

        session["cart"] = {}
        return self._message_ok_inline(f"Pedido guardado correctamente.")

    # *************************************** HISTORIAL ***********************************************************

    def hist_search(self, form):
        rif = form.get("rif", "").strip()
        if rif == "":
            return self._message_error_inline("Ingrese la cédula (Rif).")

        with self.con.cursor() as cur:
            cur.execute(
                "SELECT ClienteID, RazonSocial, Rif FROM Clientes WHERE Rif=%s LIMIT 1;",
                (rif,),
            )
            row = cur.fetchone()

        hist = {
            "rif": rif,
            "cliente_id": 0,
            "razon": "",
            "pedidos": [],
            "pedido_sel": 0,
            "items": [],
        }

        if not row:
            session["hist"] = hist
            return self._message_error_inline("No existe cliente con esa cédula (Rif).")

        cid = int(row["ClienteID"])
        raz = row["RazonSocial"]

        with self.con.cursor() as cur:
            # Importante: duplicar los % en DATE_FORMAT para que PyMySQL
            # no intente formatear %Y, %m, etc. como placeholders de Python.
            cur.execute(
                """
                SELECT DATE_FORMAT(pe.FechaPedido,'%%Y-%%m-%%d %%H:%%i:%%s') AS FechaPedido,
                       pr.Descripcion,
                       pr.Precio,
                       pi.Cantidad
                FROM Pedidos pe
                INNER JOIN PedidosItems pi ON pi.PedidoID = pe.PedidoID
                INNER JOIN Productos pr ON pr.ProductoID = pi.ProductoID
                WHERE pe.ClienteID = %s
                ORDER BY pe.FechaPedido DESC, pe.PedidoID DESC;
                """,
                (cid,),
            )
            items = cur.fetchall()

        hist["cliente_id"] = cid
        hist["razon"] = (
            f"Cliente (Rif: {rif})" if not raz else raz
        )
        hist["items"] = items
        session["hist"] = hist

        if not items:
            return self._message_ok_inline(
                "Cliente encontrado, pero no tiene compras registradas."
            )
        return self._message_ok_inline("Compras encontradas.")

    def hist_view(self, form):
        pid = int(form.get("pedidoID", 0))
        if pid <= 0:
            return self._message_error_inline("Seleccione una fecha de compra.")

        with self.con.cursor() as cur:
            cur.execute(
                """
                SELECT p.Descripcion, p.Precio, pi.Cantidad
                FROM PedidosItems pi
                INNER JOIN Productos p ON p.ProductoID = pi.ProductoID
                WHERE pi.PedidoID = %s;
                """,
                (pid,),
            )
            items = cur.fetchall()

        hist = session.get("hist", {})
        hist["pedido_sel"] = pid
        hist["items"] = items
        session["hist"] = hist

        if not items:
            return self._message_error_inline("No hay detalle para ese pedido.")
        return self._message_ok_inline("Detalle cargado.")

    def hist_clear(self):
        session["hist"] = {
            "rif": "",
            "cliente_id": 0,
            "razon": "",
            "pedidos": [],
            "pedido_sel": 0,
            "items": [],
        }
        return self._message_ok_inline("Historial limpiado.")
