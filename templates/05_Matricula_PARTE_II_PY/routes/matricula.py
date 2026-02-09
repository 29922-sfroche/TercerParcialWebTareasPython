# routes/matricula.py
import base64
from datetime import datetime

# ==========================================================
# print_r tipo PHP (PRUEBAS DE ESCRITORIO)
# ==========================================================
def print_r_py(data):
    salida = "Array\n(\n"
    if isinstance(data, dict):
        for k, v in data.items():
            salida += f"    [{k}] => {v}\n"
    elif isinstance(data, (list, tuple)):
        for i, v in enumerate(data):
            salida += f"    [{i}] => {v}\n"
    salida += ")\n"
    return salida


class Matricula:
    def __init__(self, cn):
        self.con = cn
        self.id = None
        self.fecha = None
        self.vehiculo = None
        self.agencia = None
        self.anio = None

        # MISMA SALIDA QUE PHP
        self.debug = "EJECUTANDOSE EL CONSTRUCTOR MATRICULA<br><br>"

    # ======================================================
    # FORM (NEW / ACT) - SOLO MUESTRA (igual PHP)
    # ======================================================
    def get_form(self, id=None):

        html = self.debug

        # ------------------------------------------
        # NUEVO
        # ------------------------------------------
        if id is None or id == 0:
            self.fecha = None
            self.vehiculo = None
            self.agencia = None
            self.anio = None

            op = "new"
            bandera = 1

        # ------------------------------------------
        # ACTUALIZAR
        # ------------------------------------------
        else:
            sql = f"SELECT * FROM matricula WHERE id={id};"
            cur = self.con.cursor(dictionary=True)
            cur.execute(sql)
            row = cur.fetchone()
            num = cur.rowcount

            bandera = 0 if num == 0 else 1

            if not bandera:
                mensaje = f"tratar de actualizar la matricula con id= {id} <br>"
                html += self._message_error(mensaje)
                return html

            # MISMO ESTILO QUE VEHICULO: imprime registro a modificar
            html += "<br>REGISTRO A MODIFICAR: <br>"
            html += "<pre>" + print_r_py(row) + "</pre>"

            self.fecha = row["fecha"]
            self.vehiculo = row["vehiculo"]
            self.agencia = row["agencia"]
            self.anio = row["anio"]

            op = "update"

        # ------------------------------------------
        # CONSTRUCCION FORM
        # ------------------------------------------
        if bandera:
            html += f"""
            <form name="Form_matricula" method="POST">
                <input type="hidden" name="id" value="{id or 0}">
                <input type="hidden" name="op" value="{op}">

                <table border="2" align="center">
                    <tr>
                        <th colspan="2">DATOS MATRÍCULA</th>
                    </tr>

                    <tr>
                        <td>Fecha:</td>
                        <td><input type="date" name="fecha" value="{self.fecha or ''}"></td>
                    </tr>

                    <tr>
                        <td>Vehículo:</td>
                        <td>{self._get_combo_db("vehiculo","id","placa","vehiculo", self.vehiculo)}</td>
                    </tr>

                    <tr>
                        <td>Agencia:</td>
                        <td>{self._get_combo_db("agencia","id","descripcion","agencia", self.agencia)}</td>
                    </tr>

                    <tr>
                        <td>Año:</td>
                        <td>{self._get_combo_anio("anio",1950, self.anio)}</td>
                    </tr>

                    <tr>
                        <th colspan="2">
                            <input type="submit" name="Guardar" value="GUARDAR">
                        </th>
                    </tr>

                    <tr>
                        <th colspan="2"><a href="/?mod=matricula">Regresar</a></th>
                    </tr>
                </table>
            </form>
            """
        return html

    # ======================================================
    # LIST (con Nuevo / Actualizar / Detalle / Borrar)
    # ======================================================
    def get_list(self):

        d_new_final = base64.b64encode("new/0".encode()).decode()

        html = f"""
        <table border="1" align="center">
            <h1>MATRÍCULAS PARTE II</h1>

            <tr>
                <th colspan="7">Lista de Matrículas</th>
            </tr>

            <tr>
                <th colspan="7">
                    <a href="/?mod=matricula&d={d_new_final}">Nuevo</a>
                </th>
            </tr>

            <tr>
                <th>Fecha</th>
                <th>Vehiculo</th>
                <th>Agencia</th>
                <th>Año</th>
                <th colspan="3">Acciones</th>
            </tr>
        """

        sql = """
        SELECT m.id, m.fecha, v.placa, a.descripcion AS agencia, m.anio
        FROM matricula m, vehiculo v, agencia a
        WHERE m.vehiculo = v.id AND m.agencia = a.id;
        """

        cur = self.con.cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()

        if rows:
            for row in rows:
                d_del_final = base64.b64encode(f"del/{row['id']}".encode()).decode()
                d_act_final = base64.b64encode(f"act/{row['id']}".encode()).decode()
                d_det_final = base64.b64encode(f"det/{row['id']}".encode()).decode()

                html += f"""
                <tr>
                    <td>{row['fecha']}</td>
                    <td>{row['placa']}</td>
                    <td>{row['agencia']}</td>
                    <td>{row['anio']}</td>
                    <td><a href="/?mod=matricula&d={d_del_final}">Borrar</a></td>
                    <td><a href="/?mod=matricula&d={d_act_final}">Actualizar</a></td>
                    <td><a href="/?mod=matricula&d={d_det_final}">Detalle</a></td>
                </tr>
                """
        else:
            mensaje = "Tabla Matricula<br>"
            html += self._message_BD_Vacia(mensaje)
            html += "<br><br><br>"

        html += "</table>"
        return html

    # ======================================================
    # DETAIL
    # ======================================================
    def get_detail_matricula(self, id):

        sql = f"""
        SELECT m.fecha, v.placa, a.descripcion AS agencia, m.anio
        FROM matricula m, vehiculo v, agencia a
        WHERE m.id={id} AND m.vehiculo=v.id AND m.agencia=a.id;
        """

        cur = self.con.cursor(dictionary=True)
        cur.execute(sql)
        row = cur.fetchone()
        num = cur.rowcount

        if num == 0 or not row:
            mensaje = f"desplegar el detalle de la matricula con id= {id} <br>"
            return self._message_error(mensaje)

        html = "<br>TUPLA<br>"
        html += "<pre>" + print_r_py(row) + "</pre>"

        html += f"""
        <table border="1" align="center">
            <tr>
                <th colspan="2">DETALLE MATRÍCULA</th>
            </tr>
            <tr>
                <td>Fecha:</td>
                <td>{row['fecha']}</td>
            </tr>
            <tr>
                <td>Vehículo (placa):</td>
                <td>{row['placa']}</td>
            </tr>
            <tr>
                <td>Agencia:</td>
                <td>{row['agencia']}</td>
            </tr>
            <tr>
                <td>Año:</td>
                <td>{row['anio']}</td>
            </tr>
            <tr>
                <th colspan="2"><a href="/?mod=matricula">Regresar</a></th>
            </tr>
        </table>
        """
        return html

    # ======================================================
    # DELETE
    # ======================================================
    def delete_matricula(self, id):

        sql = f"DELETE FROM matricula WHERE id={id};"
        cur = self.con.cursor()

        try:
            cur.execute(sql)
            self.con.commit()
            # en PHP hace echo, aquí devolvemos HTML
            return self._message_ok("eliminó")
        except:
            return self._message_error("eliminar<br>")

    # ======================================================
    # HELPERS
    # ======================================================
    def _get_combo_db(self, tabla, valor, etiqueta, nombre, defecto=None):
        html = f'<select name="{nombre}">'
        sql = f"SELECT {valor}, {etiqueta} FROM {tabla};"

        cur = self.con.cursor(dictionary=True)
        cur.execute(sql)

        for row in cur.fetchall():
            selected = "selected" if defecto == row[valor] else ""
            html += f'<option value="{row[valor]}" {selected}>{row[etiqueta]}</option>\n'

        html += "</select>"
        return html

    def _get_combo_anio(self, nombre, anio_inicial, defecto=None):
        html = f'<select name="{nombre}">'
        anio_actual = datetime.now().year

        for i in range(anio_inicial, anio_actual + 1):
            selected = "selected" if defecto == i else ""
            html += f'<option value="{i}" {selected}>{i}</option>\n'

        html += "</select>"
        return html

    # ======================================================
    # MENSAJES (idénticos al estilo PHP)
    # ======================================================
    def _message_error(self, tipo):
        return f"""
        <table border="0" align="center">
            <tr>
                <th>Error al {tipo} Favor contactar a .................... </th>
            </tr>
            <tr>
                <th><a href="/?mod=matricula">Regresar</a></th>
            </tr>
        </table>
        """

    def _message_BD_Vacia(self, tipo):
        return f"""
        <table border="0" align="center">
            <tr>
                <th> NO existen registros en la {tipo} Favor contactar a .................... </th>
            </tr>
        </table>
        """

    def _message_ok(self, tipo):
        return f"""
        <table border="0" align="center">
            <tr>
                <th>El registro se  {tipo} correctamente</th>
            </tr>
            <tr>
                <th><a href="/?mod=matricula">Regresar</a></th>
            </tr>
        </table>
        """
