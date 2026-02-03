# routes/matricula.py
import base64
from datetime import datetime
from flask import request


class Matricula:

    def __init__(self, cn):
        self.id = None
        self.fecha = None
        self.vehiculo = None
        self.agencia = None
        self.anio = None
        self.con = cn

    # =======================
    # CREATE
    # =======================
    def save_matricula(self):

        self.fecha = request.form.get("fecha")
        self.vehiculo = request.form.get("vehiculo")
        self.agencia = request.form.get("agencia")
        self.anio = request.form.get("anio")

        sql = f"""
        INSERT INTO matricula VALUES(
            NULL,
            '{self.fecha}',
            {self.vehiculo},
            {self.agencia},
            '{self.anio}'
        );
        """

        try:
            cur = self.con.cursor()
            cur.execute(sql)
            self.con.commit()
            return self._message_ok("guardó")
        except Exception:
            return self._message_error("guardar<br>")

    # =======================
    # UPDATE
    # =======================
    def update_matricula(self):

        self.id = request.form.get("id")
        self.fecha = request.form.get("fecha")
        self.vehiculo = request.form.get("vehiculo")
        self.agencia = request.form.get("agencia")
        self.anio = request.form.get("anio")

        sql = f"""
        UPDATE matricula SET
            fecha='{self.fecha}',
            vehiculo={self.vehiculo},
            agencia={self.agencia},
            anio='{self.anio}'
        WHERE id={self.id};
        """

        try:
            cur = self.con.cursor()
            cur.execute(sql)
            self.con.commit()
            return self._message_ok("modificó")
        except Exception:
            return self._message_error("al modificar<br>")

    # =======================
    # FORM (NEW / ACT)
    # =======================
    def get_form(self, id=None):

        if (id is None) or (int(id) == 0):

            self.fecha = None
            self.vehiculo = None
            self.agencia = None
            self.anio = None

            op = "new"
            bandera = True

        else:

            sql = f"SELECT * FROM matricula WHERE id={id};"
            cur = self.con.cursor(dictionary=True)
            cur.execute(sql)
            row = cur.fetchone()
            bandera = row is not None

            if not bandera:
                mensaje = f"tratar de actualizar la matricula con id= {id}<br>"
                return self._message_error(mensaje)

            else:
                # DEBUG IGUAL QUE PHP
                print("\nREGISTRO A MODIFICAR:")
                print(row)

                self.fecha = row["fecha"]
                self.vehiculo = row["vehiculo"]
                self.agencia = row["agencia"]
                self.anio = row["anio"]

                op = "update"

        if bandera:

            html = f"""
            <form name="Form_matricula" method="POST" action="/?mod=matricula">

                <input type="hidden" name="id" value="{id or 0}">
                <input type="hidden" name="op" value="{op}">

                <table border="2" align="center">
                    <tr>
                        <th colspan="2">DATOS MATRÍCULA</th>
                    </tr>
                    <tr>
                        <td>Fecha:</td>
                        <td><input type="date" name="fecha" value="{self.fecha or ''}" required></td>
                    </tr>
                    <tr>
                        <td>Vehículo:</td>
                        <td>{self._get_combo_db("vehiculo","id","placa","vehiculo",self.vehiculo)}</td>
                    </tr>
                    <tr>
                        <td>Agencia:</td>
                        <td>{self._get_combo_db("agencia","id","descripcion","agencia",self.agencia)}</td>
                    </tr>
                    <tr>
                        <td>Año:</td>
                        <td>{self._get_combo_anio("anio",1950,self.anio)}</td>
                    </tr>
                    <tr>
                        <th colspan="2"><input type="submit" name="Guardar" value="GUARDAR"></th>
                    </tr>
                    <tr>
                        <th colspan="2"><a href="/?mod=matricula">Regresar</a></th>
                    </tr>
                </table>
            </form>
            """
            return html

    # =======================
    # READ (LIST)
    # =======================
    def get_list(self):

        d_new_final = base64.b64encode(b"new/0").decode()

        html = f"""
        <table border="1" align="center">
        <h1>MATRÍCULAS PARTE III</h1>
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
        SELECT m.id, m.fecha, v.placa, a.descripcion as agencia, m.anio
        FROM matricula m, vehiculo v, agencia a
        WHERE m.vehiculo = v.id AND m.agencia = a.id;
        """

        cur = self.con.cursor(dictionary=True)
        cur.execute(sql)
        rows = cur.fetchall()

        if rows:
            for row in rows:
                d_del = base64.b64encode(f"del/{row['id']}".encode()).decode()
                d_act = base64.b64encode(f"act/{row['id']}".encode()).decode()
                d_det = base64.b64encode(f"det/{row['id']}".encode()).decode()

                html += f"""
                <tr>
                    <td>{row['fecha']}</td>
                    <td>{row['placa']}</td>
                    <td>{row['agencia']}</td>
                    <td>{row['anio']}</td>
                    <td><a href="/?mod=matricula&d={d_del}">Borrar</a></td>
                    <td><a href="/?mod=matricula&d={d_act}">Actualizar</a></td>
                    <td><a href="/?mod=matricula&d={d_det}">Detalle</a></td>
                </tr>
                """
        else:
            html += self._message_BD_Vacia("Tabla Matricula<br>")

        html += "</table>"
        return html

    # =======================
    # READ (DETAIL)
    # =======================
    def get_detail_matricula(self, id):

        sql = f"""
        SELECT m.fecha, v.placa, a.descripcion as agencia, m.anio
        FROM matricula m, vehiculo v, agencia a
        WHERE m.id={id} AND m.vehiculo=v.id AND m.agencia=a.id;
        """

        cur = self.con.cursor(dictionary=True)
        cur.execute(sql)
        row = cur.fetchone()

        if row is None:
            mensaje = f"desplegar el detalle de la matricula con id= {id}<br>"
            return self._message_error(mensaje)

        html = f"""
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

    # =======================
    # DELETE
    # =======================
    def delete_matricula(self, id):

        sql = f"DELETE FROM matricula WHERE id={id};"

        try:
            cur = self.con.cursor()
            cur.execute(sql)
            self.con.commit()
            return self._message_ok("eliminó")
        except Exception:
            return self._message_error("eliminar<br>")

    # =======================
    # HELPERS
    # =======================
    def _get_combo_db(self, tabla, valor, etiqueta, nombre, defecto=None):

        html = f'<select name="{nombre}">'
        sql = f"SELECT {valor},{etiqueta} FROM {tabla};"
        cur = self.con.cursor(dictionary=True)
        cur.execute(sql)

        for row in cur.fetchall():
            if defecto == row[valor]:
                html += f'<option value="{row[valor]}" selected>{row[etiqueta]}</option>\n'
            else:
                html += f'<option value="{row[valor]}">{row[etiqueta]}</option>\n'

        html += "</select>"
        return html

    def _get_combo_anio(self, nombre, anio_inicial, defecto=None):

        html = f'<select name="{nombre}">'
        anio_actual = datetime.now().year

        for i in range(anio_inicial, anio_actual + 1):
            if defecto == i:
                html += f'<option value="{i}" selected>{i}</option>\n'
            else:
                html += f'<option value="{i}">{i}</option>\n'

        html += "</select>"
        return html

    # =======================
    # MENSAJES
    # =======================
    def _message_error(self, tipo):

        return f"""
        <table border="0" align="center">
            <tr>
                <th>Error al {tipo}Favor contactar a .................... </th>
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
                <th>NO existen registros en la {tipo}Favor contactar a .................... </th>
            </tr>
        </table>
        """

    def _message_ok(self, tipo):

        return f"""
        <table border="0" align="center">
            <tr>
                <th>El registro se {tipo} correctamente</th>
            </tr>
            <tr>
                <th><a href="/?mod=matricula">Regresar</a></th>
            </tr>
        </table>
        """
