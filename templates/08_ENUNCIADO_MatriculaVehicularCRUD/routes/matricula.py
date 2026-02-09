# routes/matricula.py
import base64
from datetime import datetime
from flask import request


class Matricula:
    def __init__(self, cn):
        self.con = cn

    # =====================================================
    # BASE64
    # =====================================================
    def _b64(self, txt):
        return base64.b64encode(txt.encode()).decode()

    # =====================================================
    # CREATE
    # =====================================================
    def save_matricula(self):
        f = request.form
        sql = f"""
        INSERT INTO matricula VALUES (
            NULL,
            '{f["fecha"]}',
            {f["vehiculo"]},
            {f["agencia"]},
            '{f["anio"]}'
        );
        """
        try:
            cur = self.con.cursor()
            cur.execute(sql)
            self.con.commit()
            return self._message_ok("guardó")
        except:
            return self._message_error("guardar")

    # =====================================================
    # UPDATE
    # =====================================================
    def update_matricula(self):
        f = request.form
        sql = f"""
        UPDATE matricula SET
            fecha='{f["fecha"]}',
            vehiculo={f["vehiculo"]},
            agencia={f["agencia"]},
            anio='{f["anio"]}'
        WHERE id={f["id"]};
        """
        try:
            cur = self.con.cursor()
            cur.execute(sql)
            self.con.commit()
            return self._message_ok("modificó")
        except:
            return self._message_error("modificar")

    # =====================================================
    # FORM
    # =====================================================
    def get_form(self, id=0):
        if int(id) == 0:
            row = {"fecha":"", "vehiculo":"", "agencia":"", "anio":""}
            op = "new"
        else:
            cur = self.con.cursor(dictionary=True)
            cur.execute(f"SELECT * FROM matricula WHERE id={id}")
            row = cur.fetchone()
            if not row:
                return self._message_error("buscar")
            op = "update"

        return f"""
        <form method="POST" action="/index?mod=matricula">
            <input type="hidden" name="id" value="{id}">
            <input type="hidden" name="op" value="{op}">

            <div class="container mt-4">
            <div class="table-responsive">
            <table class="table table-bordered table-striped table-hover align-middle w-auto mx-auto text-center">
                <thead class="table-dark">
                    <tr><th colspan="2">DATOS MATRÍCULA</th></tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="fw-semibold text-start">Fecha</td>
                        <td class="text-start">
                            <input type="date" name="fecha" value="{row['fecha']}" required>
                        </td>
                    </tr>
                    <tr>
                        <td class="fw-semibold text-start">Vehículo</td>
                        <td class="text-start">{self._combo_db('vehiculo','id','placa','vehiculo',row['vehiculo'])}</td>
                    </tr>
                    <tr>
                        <td class="fw-semibold text-start">Agencia</td>
                        <td class="text-start">{self._combo_db('agencia','id','descripcion','agencia',row['agencia'])}</td>
                    </tr>
                    <tr>
                        <td class="fw-semibold text-start">Año</td>
                        <td class="text-start">{self._combo_anio('anio',1950,row['anio'])}</td>
                    </tr>
                    <tr>
                        <th colspan="2">
                            <button name="Guardar" class="btn btn-success px-4">GUARDAR</button>
                        </th>
                    </tr>
                    <tr>
                        <th colspan="2">
                            <a href="/index?mod=matricula" class="btn btn-secondary px-4">Regresar</a>
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
        html = """
        <h1 class="text-center">MATRÍCULAS PARTE III</h1>
        <table class="table table-bordered text-center w-auto mx-auto">
        <tr><th colspan="7">Lista de Matrículas</th></tr>
        <tr>
            <th colspan="7">
                <a href="/index?mod=matricula&d={}" class="btn btn-primary">Nuevo</a>
            </th>
        </tr>
        <tr>
            <th>Fecha</th><th>Vehículo</th><th>Agencia</th><th>Año</th>
            <th colspan="3">Acciones</th>
        </tr>
        """.format(self._b64("new/0"))

        cur = self.con.cursor(dictionary=True)
        cur.execute("""
        SELECT m.id,m.fecha,v.placa,a.descripcion,m.anio
        FROM matricula m, vehiculo v, agencia a
        WHERE m.vehiculo=v.id AND m.agencia=a.id
        """)

        for r in cur.fetchall():
            html += f"""
            <tr>
                <td>{r['fecha']}</td>
                <td>{r['placa']}</td>
                <td>{r['descripcion']}</td>
                <td>{r['anio']}</td>
                <td><a class="btn btn-danger btn-sm" href="/index?mod=matricula&d={self._b64('del/'+str(r['id']))}">Borrar</a></td>
                <td><a class="btn btn-warning btn-sm" href="/index?mod=matricula&d={self._b64('act/'+str(r['id']))}">Actualizar</a></td>
                <td><a class="btn btn-info btn-sm" href="/index?mod=matricula&d={self._b64('det/'+str(r['id']))}">Detalle</a></td>
            </tr>
            """

        html += "</table>"
        return html

    # =====================================================
    # DELETE
    # =====================================================
    def delete_matricula(self, id):
        """Elimina una matrícula por id y devuelve un mensaje HTML."""

        sql = f"DELETE FROM matricula WHERE id={id};"

        try:
            cur = self.con.cursor()
            cur.execute(sql)
            self.con.commit()
            return self._message_ok("ELIMINÓ")
        except Exception:
            return self._message_error("eliminar")

    # =====================================================
    # DETAIL
    # =====================================================
    def get_detail_matricula(self, id):
        """Muestra el detalle de una matrícula, incluyendo datos de vehículo y agencia."""

        cur = self.con.cursor(dictionary=True)
        cur.execute(f"""
        SELECT m.fecha,
               m.anio,
               v.placa,
               a.descripcion AS agencia
        FROM matricula m, vehiculo v, agencia a
        WHERE m.id={id}
          AND m.vehiculo=v.id
          AND m.agencia=a.id
        """)

        row = cur.fetchone()

        if not row:
            return self._message_error("buscar")

        return f"""
        <div class="container mt-4">
        <table class="table table-bordered table-striped w-auto mx-auto text-center">
            <thead class="table-dark">
                <tr><th colspan="2">DETALLE MATRÍCULA</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td class="fw-semibold text-start">Fecha</td>
                    <td class="text-start">{row['fecha']}</td>
                </tr>
                <tr>
                    <td class="fw-semibold text-start">Vehículo</td>
                    <td class="text-start">{row['placa']}</td>
                </tr>
                <tr>
                    <td class="fw-semibold text-start">Agencia</td>
                    <td class="text-start">{row['agencia']}</td>
                </tr>
                <tr>
                    <td class="fw-semibold text-start">Año</td>
                    <td class="text-start">{row['anio']}</td>
                </tr>
                <tr>
                    <th colspan="2">
                        <a href="/index?mod=matricula" class="btn btn-secondary px-4">Regresar</a>
                    </th>
                </tr>
            </tbody>
        </table>
        </div>
        """

    # =====================================================
    # HELPERS
    # =====================================================
    def _combo_db(self, tabla, valor, etiqueta, nombre, defecto):
        cur = self.con.cursor(dictionary=True)
        cur.execute(f"SELECT {valor},{etiqueta} FROM {tabla}")
        html = f'<select name="{nombre}">'
        for r in cur.fetchall():
            sel = "selected" if str(defecto)==str(r[valor]) else ""
            html += f'<option value="{r[valor]}" {sel}>{r[etiqueta]}</option>'
        return html + "</select>"

    def _combo_anio(self, nombre, inicio, defecto):
        actual = datetime.now().year
        html = f'<select name="{nombre}">'
        for i in range(inicio, actual+1):
            sel = "selected" if str(defecto)==str(i) else ""
            html += f'<option {sel}>{i}</option>'
        return html + "</select>"

    # =====================================================
    # MENSAJES
    # =====================================================
    def _message_ok(self, t):
        return f"""
        <div class="text-center mt-4">
            <div class="alert alert-success">El registro se {t} correctamente</div>
            <a href="/index?mod=matricula" class="btn btn-secondary">Regresar</a>
        </div>
        """

    def _message_error(self, t):
        return f"""
        <div class="text-center mt-4">
            <div class="alert alert-danger">Error al {t}</div>
            <a href="/index?mod=matricula" class="btn btn-secondary">Regresar</a>
        </div>
        """
