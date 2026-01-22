import base64
import datetime

class Matricula:
    def __init__(self, cn):
        self.con = cn

        # ATRIBUTOS igual a PHP
        self.id = None
        self.fecha = None
        self.vehiculo = None
        self.agencia = None
        self.anio = None

    def _b64(self, txt: str) -> str:
        return base64.b64encode(txt.encode("utf-8")).decode("utf-8")

    # =========================
    # LISTA 
    # =========================
    def get_list(self):
        d_new = self._b64("new/0")

        html = f"""
        <table border="1" align="center">
            <tr>
                <th colspan="7">Lista de Matrículas</th>
            </tr>
            <tr>
                <th colspan="7"><a href="/?d={d_new}">Nuevo</a></th>
            </tr>
            <tr>
                <th>Fecha</th>
                <th>Vehiculo</th>
                <th>Agencia</th>
                <th>Año</th>
                <th colspan="3">Acciones</th>
            </tr>
        """

        cur = self.con.cursor(dictionary=True)
        sql = """
            SELECT m.id, m.fecha, v.placa, a.descripcion AS agencia, m.anio
            FROM matricula m, vehiculo v, agencia a
            WHERE m.vehiculo = v.id AND m.agencia = a.id;
        """
        cur.execute(sql)
        rows = cur.fetchall()

        for r in rows:
            d_del = self._b64(f"del/{r['id']}")
            d_act = self._b64(f"act/{r['id']}")
            d_det = self._b64(f"det/{r['id']}")

            html += f"""
            <tr>
                <td>{r['fecha']}</td>
                <td>{r['placa']}</td>
                <td>{r['agencia']}</td>
                <td>{r['anio']}</td>
                <td><a href="/?d={d_del}">Borrar</a></td>
                <td><a href="/?d={d_act}">Actualizar</a></td>
                <td><a href="/?d={d_det}">Detalle</a></td>
            </tr>
            """

        html += "</table>"
        return html

    # =========================
    # FORM (NEW / ACT) 
    # =========================
    def get_form(self, id_=0):
        debug = ""

        if id_ == 0:
            # NEW: valores por defecto
            self.fecha = datetime.date.today().isoformat()
            self.vehiculo = None
            self.agencia = None
            self.anio = datetime.date.today().year

            debug += "<br>FORMULARIO NUEVO (NO GUARDA EN BD)<br>"

        else:
            # ACT: carga de BD
            cur = self.con.cursor(dictionary=True)
            cur.execute("SELECT * FROM matricula WHERE id=%s;", (id_,))
            row = cur.fetchone()

            if not row:
                return self._message_error(f"tratar de actualizar la matricula con id= {id_}<br>")

            debug += "<br>REGISTRO A MODIFICAR:<br><pre>{}</pre>".format(row)

            self.fecha = row.get("fecha")
            self.vehiculo = row.get("vehiculo")
            self.agencia = row.get("agencia")
            self.anio = row.get("anio")

        html = f"""
        {debug}
        <form method="POST" action="/">
            <input type="hidden" name="id" value="{id_}">
            <table border="2" align="center">
                <tr>
                    <th colspan="2">DATOS MATRÍCULA</th>
                </tr>

                <tr>
                    <td>Fecha:</td>
                    <td><input type="date" name="fecha" value="{self.fecha}"></td>
                </tr>

                <tr>
                    <td>Vehículo:</td>
                    <td>{self._get_combo_db("vehiculo", "id", "placa", "vehiculoCMB", self.vehiculo)}</td>
                </tr>

                <tr>
                    <td>Agencia:</td>
                    <td>{self._get_combo_db("agencia", "id", "descripcion", "agenciaCMB", self.agencia)}</td>
                </tr>

                <tr>
                    <td>Año:</td>
                    <td>{self._get_combo_anio("anio", 1950, self.anio)}</td>
                </tr>

                <tr>
                    <th colspan="2"><input type="submit" name="Guardar" value="GUARDAR"></th>
                </tr>
                <tr>
                    <th colspan="2"><a href="/">Regresar</a></th>
                </tr>
            </table>
        </form>
        """
        return html

    # =========================
    # DETALLE
    # =========================
    def get_detail_matricula(self, id_):
        cur = self.con.cursor(dictionary=True)
        sql = """
            SELECT m.id, m.fecha, v.placa, a.descripcion AS agencia, m.anio
            FROM matricula m, vehiculo v, agencia a
            WHERE m.id=%s AND m.vehiculo=v.id AND m.agencia=a.id;
        """
        cur.execute(sql, (id_,))
        row = cur.fetchone()

        if not row:
            return self._message_error(f"desplegar el detalle de la matricula con id= {id_}<br>")

        html = f"""
        <table border="1" align="center">
            <tr><th colspan="2">DATOS DE MATRÍCULA</th></tr>
            <tr><td>Fecha:</td><td>{row['fecha']}</td></tr>
            <tr><td>Vehiculo:</td><td>{row['placa']}</td></tr>
            <tr><td>Agencia:</td><td>{row['agencia']}</td></tr>
            <tr><td>Año:</td><td>{row['anio']}</td></tr>
            <tr><th colspan="2"><a href="/">Regresar</a></th></tr>
        </table>
        """
        return html

    # =========================
    # ELIMINAR 
    # =========================
    def delete_matricula(self, id_):
        cur = self.con.cursor()
        cur.execute("DELETE FROM matricula WHERE id=%s;", (id_,))
        self.con.commit()
        return self._message_ok("eliminó")

    # =========================
    # COMBO DESDE BD
    # =========================
    def _get_combo_db(self, tabla, valor, etiqueta, nombre, defecto=None):
        cur = self.con.cursor(dictionary=True)
        cur.execute(f"SELECT {valor}, {etiqueta} FROM {tabla};")
        rows = cur.fetchall()

        html = f'<select name="{nombre}">'
        for r in rows:
            selected = " selected" if defecto == r[valor] else ""
            html += f'<option value="{r[valor]}"{selected}>{r[etiqueta]}</option>'
        html += "</select>"
        return html

    # =========================
    # COMBO AÑO
    # =========================
    def _get_combo_anio(self, nombre, anio_inicial, defecto=None):
        anio_actual = datetime.datetime.now().year
        html = f'<select name="{nombre}">'
        for i in range(anio_inicial, anio_actual + 1):
            selected = " selected" if int(defecto) == i else ""
            html += f'<option value="{i}"{selected}>{i}</option>'
        html += "</select>"
        return html

    # =========================
    # MENSAJES
    # =========================
    def _message_error(self, tipo):
        return f"""
        <table border="0" align="center">
            <tr><th>Error al {tipo} Favor contactar a ..............</th></tr>
            <tr><th><a href="/">Regresar</a></th></tr>
        </table>
        """

    def _message_ok(self, tipo):
        return f"""
        <table border="0" align="center">
            <tr><th>El registro se {tipo} correctamente</th></tr>
            <tr><th><a href="/">Regresar</a></th></tr>
        </table>
        """
