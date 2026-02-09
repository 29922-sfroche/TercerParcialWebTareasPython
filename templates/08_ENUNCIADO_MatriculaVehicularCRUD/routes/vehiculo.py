# routes/vehiculo.py
import os
import base64
from datetime import datetime
from flask import request

# =====================================================
# RUTA DE IMÁGENES
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "imagenes")


class vehiculo:

    def __init__(self, cn):
        self.con = cn

    # =====================================================
    # BASE64
    # =====================================================
    def _b64(self, txt):
        return base64.b64encode(txt.encode("utf-8")).decode("utf-8")

    # =====================================================
    # CREATE
    # =====================================================
    def save_vehiculo(self):
        f = request.form
        file = request.files.get("foto")

        if not file or file.filename.strip() == "":
            return self._message_error("cargar la imagen")

        os.makedirs(IMAGES_DIR, exist_ok=True)
        file.save(os.path.join(IMAGES_DIR, file.filename))

        sql = f"""
        INSERT INTO vehiculo VALUES(
            NULL,
            '{f["placa"]}',
            {f["marcaCMB"]},
            '{f["motor"]}',
            '{f["chasis"]}',
            '{f["combustibleRBT"]}',
            '{f["anio"]}',
            {f["colorCMB"]},
            '{file.filename}',
            {f["avaluo"]}
        );
        """

        try:
            cur = self.con.cursor()
            cur.execute(sql)
            self.con.commit()
            return self._message_ok("guardó")
        except Exception as e:
            return self._message_error("guardar")

    # =====================================================
    # UPDATE
    # =====================================================
    def update_vehiculo(self):
        f = request.form

        sql = f"""
        UPDATE vehiculo SET
            placa='{f["placa"]}',
            marca={f["marcaCMB"]},
            motor='{f["motor"]}',
            chasis='{f["chasis"]}',
            combustible='{f["combustibleRBT"]}',
            anio='{f["anio"]}',
            color={f["colorCMB"]}
        WHERE id={f["id"]};
        """

        try:
            cur = self.con.cursor()
            cur.execute(sql)
            self.con.commit()
            return self._message_ok("modificó")
        except Exception:
            return self._message_error("modificar")

    # =====================================================
    # FORM
    # =====================================================
    def get_form(self, id=0):

        if int(id) == 0:
            row = {}
            op = "new"
            flag = ""
        else:
            cur = self.con.cursor(dictionary=True)
            cur.execute(f"SELECT * FROM vehiculo WHERE id={id}")
            row = cur.fetchone()

            if not row:
                return self._message_error("buscar")

            op = "update"
            flag = "disabled"

        combustibles = ["Gasolina", "Diesel", "Eléctrico"]

        return f"""
        <form method="POST" action="/index_python?mod=vehiculo" enctype="multipart/form-data">
            <input type="hidden" name="id" value="{id}">
            <input type="hidden" name="op" value="{op}">

            <div class="container mt-4">
            <div class="table-responsive">
            <table class="table table-bordered table-striped table-hover align-middle w-auto mx-auto text-center">
            <thead class="table-dark">
                <tr><th colspan="2">DATOS VEHÍCULO</th></tr>
            </thead>
            <tbody>

                <tr>
                    <td class="text-start fw-semibold">Placa</td>
                    <td><input class="form-control" name="placa" value="{row.get("placa","")}" required></td>
                </tr>

                <tr>
                    <td class="text-start fw-semibold">Marca</td>
                    <td>{self._combo_db("marca","id","descripcion","marcaCMB",row.get("marca"))}</td>
                </tr>

                <tr>
                    <td class="text-start fw-semibold">Motor</td>
                    <td><input class="form-control" name="motor" value="{row.get("motor","")}" required></td>
                </tr>

                <tr>
                    <td class="text-start fw-semibold">Chasis</td>
                    <td><input class="form-control" name="chasis" value="{row.get("chasis","")}" required></td>
                </tr>

                <tr>
                    <td class="text-start fw-semibold">Combustible</td>
                    <td>{self._radio(combustibles,"combustibleRBT",row.get("combustible"))}</td>
                </tr>

                <tr>
                    <td class="text-start fw-semibold">Año</td>
                    <td>{self._combo_anio("anio",1980,row.get("anio"))}</td>
                </tr>

                <tr>
                    <td class="text-start fw-semibold">Color</td>
                    <td>{self._combo_db("color","id","descripcion","colorCMB",row.get("color"))}</td>
                </tr>

                <tr>
                    <td class="text-start fw-semibold">Foto</td>
                    <td><input class="form-control" type="file" name="foto" {flag}></td>
                </tr>

                <tr>
                    <td class="text-start fw-semibold">Avalúo</td>
                    <td><input class="form-control" name="avaluo" value="{row.get("avaluo","")}" {flag} required></td>
                </tr>

                <tr>
                    <th colspan="2">
                        <button type="submit" name="Guardar" class="btn btn-success px-4">GUARDAR</button>
                    </th>
                </tr>

                <tr>
                    <th colspan="2">
                        <a href="/index_python?mod=vehiculo" class="btn btn-secondary px-4">Regresar</a>
                    </th>
                </tr>

            </tbody>
            </table>
            </div>
            </div>
        </form>
        """

    # =====================================================
    # LIST
    # =====================================================
    def get_list(self):

        html = f"""
        <h1 class="text-center">VEHÍCULOS PARTE III</h1>

        <table class="table table-bordered table-hover align-middle w-auto mx-auto text-center">
            <tr>
                <th colspan="8">
                    <a href="/index_python?mod=vehiculo&d={self._b64("new/0")}" class="btn btn-primary">Nuevo</a>
                </th>
            </tr>
            <tr class="table-dark">
                <th>Placa</th>
                <th>Marca</th>
                <th>Color</th>
                <th>Año</th>
                <th>Avalúo</th>
                <th colspan="3">Acciones</th>
            </tr>
        """

        cur = self.con.cursor(dictionary=True)
        cur.execute("""
        SELECT v.id,v.placa,m.descripcion marca,c.descripcion color,v.anio,v.avaluo
        FROM vehiculo v, marca m, color c
        WHERE v.marca=m.id AND v.color=c.id
        """)

        for r in cur.fetchall():
            html += f"""
            <tr>
                <td>{r["placa"]}</td>
                <td>{r["marca"]}</td>
                <td>{r["color"]}</td>
                <td>{r["anio"]}</td>
                <td>{r["avaluo"]}</td>
                <td><a class="btn btn-danger btn-sm" href="/index_python?mod=vehiculo&d={self._b64('del/'+str(r['id']))}">Borrar</a></td>
                <td><a class="btn btn-warning btn-sm" href="/index_python?mod=vehiculo&d={self._b64('act/'+str(r['id']))}">Actualizar</a></td>
                <td><a class="btn btn-info btn-sm" href="/index_python?mod=vehiculo&d={self._b64('det/'+str(r['id']))}">Detalle</a></td>
            </tr>
            """

        html += "</table>"
        return html

    # =====================================================
    # DETAIL
    # =====================================================
    def get_detail_vehiculo(self, id):

        cur = self.con.cursor(dictionary=True)
        cur.execute(f"""
        SELECT v.*,m.descripcion marca,c.descripcion color
        FROM vehiculo v, marca m, color c
        WHERE v.id={id} AND v.marca=m.id AND v.color=c.id
        """)

        r = cur.fetchone()
        if not r:
            return self._message_error("buscar")

        return f"""
        <div class="container mt-4">
        <table class="table table-bordered table-striped w-auto mx-auto">
            <thead class="table-dark">
                <tr><th colspan="2">DETALLE VEHÍCULO</th></tr>
            </thead>
            <tr><td>Placa</td><td>{r["placa"]}</td></tr>
            <tr><td>Marca</td><td>{r["marca"]}</td></tr>
            <tr><td>Motor</td><td>{r["motor"]}</td></tr>
            <tr><td>Chasis</td><td>{r["chasis"]}</td></tr>
            <tr><td>Combustible</td><td>{r["combustible"]}</td></tr>
            <tr><td>Año</td><td>{r["anio"]}</td></tr>
            <tr><td>Color</td><td>{r["color"]}</td></tr>
            <tr class="table-success"><th>Avalúo</th><th>${r["avaluo"]}</th></tr>
            <tr class="table-info"><th>Matrícula</th><th>${float(r["avaluo"])*0.10:.2f}</th></tr>
            <tr>
                <th colspan="2" class="text-center">
                    <img src="/imagenes/{r["foto"]}" class="img-fluid rounded" style="max-width:300px">
                </th>
            </tr>
            <tr>
                <th colspan="2">
                    <a href="/index_python?mod=vehiculo" class="btn btn-secondary">Regresar</a>
                </th>
            </tr>
        </table>
        </div>
        """

    # =====================================================
    # HELPERS
    # =====================================================
    def _combo_db(self, tabla, valor, etiqueta, nombre, defecto):
        cur = self.con.cursor(dictionary=True)
        cur.execute(f"SELECT {valor},{etiqueta} FROM {tabla}")
        html = f'<select class="form-select" name="{nombre}">'
        for r in cur.fetchall():
            sel = "selected" if defecto == r[valor] else ""
            html += f'<option value="{r[valor]}" {sel}>{r[etiqueta]}</option>'
        return html + "</select>"

    def _combo_anio(self, nombre, inicio, defecto):
        html = f'<select class="form-select" name="{nombre}">'
        for i in range(inicio, datetime.now().year + 1):
            sel = "selected" if str(defecto) == str(i) else ""
            html += f'<option value="{i}" {sel}>{i}</option>'
        return html + "</select>"

    def _radio(self, arr, name, defecto):
        html = ""
        for v in arr:
            chk = "checked" if str(defecto) == str(v) else ""
            html += f"""
            <div class="form-check">
                <input class="form-check-input" type="radio" name="{name}" value="{v}" {chk}>
                <label class="form-check-label">{v}</label>
            </div>
            """
        return html
    
    # =====================================================
    # DELETE
    # =====================================================
    def delete_vehiculo(self, id):

        sql = f"DELETE FROM vehiculo WHERE id={id};"

        try:
            cur = self.con.cursor()
            cur.execute(sql)
            self.con.commit()
            return self._message_ok("eliminó")
        except Exception as e:
            return self._message_error("eliminar")


    # =====================================================
    # MENSAJES
    # =====================================================
    def _message_ok(self, t):
        return f"<div class='alert alert-success text-center'>El registro se {t} correctamente</div>"

    def _message_error(self, t):
        return f"<div class='alert alert-danger text-center'>Error al {t}</div>"
