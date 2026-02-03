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


class Vehiculo:

    # ======================================================
    # CONSTRUCTOR
    # ======================================================
    def __init__(self, cn):
        self.con = cn

        self.id = None
        self.placa = None
        self.marca = None
        self.motor = None
        self.chasis = None
        self.combustible = None
        self.anio = None
        self.color = None
        self.foto = None
        self.avaluo = None

        # MISMA SALIDA QUE PHP
        self.debug = "EJECUTANDOSE EL CONSTRUCTOR VEHICULO<br><br>"

    # ======================================================
    # FORMULARIO (NEW / UPDATE)
    # ======================================================
    def get_form(self, id=None):

        html = self.debug

        # ------------------------------------------
        # NUEVO
        # ------------------------------------------
        if id is None or id == 0:
            self.placa = None
            self.marca = None
            self.motor = None
            self.chasis = None
            self.combustible = None
            self.anio = None
            self.color = None
            self.foto = None
            self.avaluo = None

            flag = ""
            op = "new"
            bandera = 1

        # ------------------------------------------
        # ACTUALIZAR
        # ------------------------------------------
        else:
            sql = f"SELECT * FROM vehiculo WHERE id={id};"
            cur = self.con.cursor(dictionary=True)
            cur.execute(sql)
            row = cur.fetchone()
            num = cur.rowcount

            bandera = 0 if num == 0 else 1

            if not bandera:
                mensaje = f"tratar de actualizar el vehiculo con id= {id}<br>"
                html += self._message_error(mensaje)
                return html

            html += "<br>REGISTRO A MODIFICAR:<br>"
            html += "<pre>" + print_r_py(row) + "</pre>"

            self.placa = row["placa"]
            self.marca = row["marca"]
            self.motor = row["motor"]
            self.chasis = row["chasis"]
            self.combustible = row["combustible"]
            self.anio = row["anio"]
            self.color = row["color"]
            self.foto = row["foto"]
            self.avaluo = row["avaluo"]

            flag = "enabled"
            op = "update"

        # ------------------------------------------
        # FORMULARIO
        # ------------------------------------------
        if bandera:
            combustibles = ["Gasolina", "Diesel", "Eléctrico"]

            html += f"""
            <form name="Form_vehiculo" method="POST" enctype="multipart/form-data">
                <input type="hidden" name="id" value="{id or 0}">
                <input type="hidden" name="op" value="{op}">

                <table border="2" align="center">
                    <tr>
                        <th colspan="2">DATOS VEHÍCULO</th>
                    </tr>

                    <tr>
                        <td>Placa:</td>
                        <td><input type="text" size="6" name="placa" value="{self.placa or ''}"></td>
                    </tr>

                    <tr>
                        <td>Marca:</td>
                        <td>{self._get_combo_db("marca","id","descripcion","marca",self.marca)}</td>
                    </tr>

                    <tr>
                        <td>Motor:</td>
                        <td><input type="text" size="15" name="motor" value="{self.motor or ''}"></td>
                    </tr>

                    <tr>
                        <td>Chasis:</td>
                        <td><input type="text" size="15" name="chasis" value="{self.chasis or ''}"></td>
                    </tr>

                    <tr>
                        <td>Combustible:</td>
                        <td>{self._get_radio(combustibles,"combustible",self.combustible)}</td>
                    </tr>

                    <tr>
                        <td>Año:</td>
                        <td>{self._get_combo_anio("anio",1950,self.anio)}</td>
                    </tr>

                    <tr>
                        <td>Color:</td>
                        <td>{self._get_combo_db("color","id","descripcion","color",self.color)}</td>
                    </tr>

                    <tr>
                        <td>Foto:</td>
                        <td><input type="file" name="foto" {flag}></td>
                    </tr>

                    <tr>
                        <td>Avalúo:</td>
                        <td><input type="text" size="8" name="avaluo" value="{self.avaluo or ''}" {flag}></td>
                    </tr>

                    <tr>
                        <th colspan="2">
                            <input type="submit" name="Guardar" value="GUARDAR">
                        </th>
                    </tr>

                    <tr>
                        <th colspan="2"><a href="/?mod=vehiculo">Regresar</a></th>
                    </tr>
                </table>
            </form>
            """

        return html

    # ======================================================
    # LISTADO
    # ======================================================
    def get_list(self):

        d_new = base64.b64encode("new/0".encode()).decode()

        html = f"""
        <h1>VEHÍCULOS PARTE II</h1>

        <table border="1" align="center">
            <tr>
                <th colspan="8">Lista de Vehículos</th>
            </tr>

            <tr>
                <th colspan="8">
                    <a href="?mod=vehiculo&d={d_new}">Nuevo</a>
                </th>
            </tr>

            <tr>
                <th>Placa</th>
                <th>Marca</th>
                <th>Color</th>
                <th>Año</th>
                <th>Avalúo</th>
                <th colspan="3">Acciones</th>
            </tr>
        """

        sql = """
        SELECT v.id, v.placa, m.descripcion AS marca,
               c.descripcion AS color, v.anio, v.avaluo
        FROM vehiculo v, color c, marca m
        WHERE v.marca=m.id AND v.color=c.id;
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
                    <td>{row['placa']}</td>
                    <td>{row['marca']}</td>
                    <td>{row['color']}</td>
                    <td>{row['anio']}</td>
                    <td>{row['avaluo']}</td>
                    <td><a href="?mod=vehiculo&d={d_del}">Borrar</a></td>
                    <td><a href="?mod=vehiculo&d={d_act}">Actualizar</a></td>
                    <td><a href="?mod=vehiculo&d={d_det}">Detalle</a></td>
                </tr>
                """
        else:
            html += self._message_BD_Vacia("Tabla Vehiculo<br>")

        html += "</table>"
        return html

    # ======================================================
    # DETALLE
    # ======================================================
    def get_detail_vehiculo(self, id):

        sql = f"""
        SELECT v.placa, m.descripcion AS marca, v.motor,
               v.chasis, v.combustible, v.anio,
               c.descripcion AS color, v.foto, v.avaluo
        FROM vehiculo v, color c, marca m
        WHERE v.id={id} AND v.marca=m.id AND v.color=c.id;
        """

        cur = self.con.cursor(dictionary=True)
        cur.execute(sql)
        row = cur.fetchone()

        if not row:
            mensaje = f"desplegar el detalle del vehiculo con id= {id}<br>"
            return self._message_error(mensaje)

        html = "<br>TUPLA<br>"
        html += "<pre>" + print_r_py(row) + "</pre>"

        html += f"""
        <table border="1" align="center">
            <tr>
                <th colspan="2">DATOS DEL VEHÍCULO</th>
            </tr>
            <tr><td>Placa:</td><td>{row['placa']}</td></tr>
            <tr><td>Marca:</td><td>{row['marca']}</td></tr>
            <tr><td>Motor:</td><td>{row['motor']}</td></tr>
            <tr><td>Chasis:</td><td>{row['chasis']}</td></tr>
            <tr><td>Combustible:</td><td>{row['combustible']}</td></tr>
            <tr><td>Año:</td><td>{row['anio']}</td></tr>
            <tr><td>Color:</td><td>{row['color']}</td></tr>
            <tr><td>Avalúo:</td><th>${row['avaluo']} USD</th></tr>
            <tr>
                <td>Valor Matrícula:</td>
                <th>${self._calculo_matricula(row['avaluo'])} USD</th>
            </tr>
            <tr>
                <th colspan="2">
                    <img src="/imagenes/{row['foto']}" width="300px">
                </th>
            </tr>
            <tr>
                <th colspan="2"><a href="/?mod=vehiculo">Regresar</a></th>
            </tr>
        </table>
        """

        return html

    # ======================================================
    # DELETE
    # ======================================================
    def delete_vehiculo(self, id):

        sql = f"DELETE FROM vehiculo WHERE id={id};"
        cur = self.con.cursor()

        try:
            cur.execute(sql)
            self.con.commit()
            return self._message_ok("eliminó")
        except:
            return self._message_error("eliminar<br>")

    # ======================================================
    # HELPERS
    # ======================================================
    def _calculo_matricula(self, avaluo):
        return f"{float(avaluo) * 0.10:.2f}"

    def _get_combo_db(self, tabla, valor, etiqueta, nombre, defecto=None):
        html = f'<select name="{nombre}">'
        cur = self.con.cursor(dictionary=True)
        cur.execute(f"SELECT {valor}, {etiqueta} FROM {tabla};")

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

    def _get_radio(self, arreglo, nombre, defecto=None):
        html = '<table border="0" align="left">'
        for etiqueta in arreglo:
            checked = "checked" if defecto == etiqueta else ""
            html += f"""
            <tr>
                <td>{etiqueta}</td>
                <td><input type="radio" value="{etiqueta}" name="{nombre}" {checked}></td>
            </tr>
            """
        html += "</table>"
        return html

    # ======================================================
    # MENSAJES
    # ======================================================
    def _message_error(self, tipo):
        return f"""
        <table border="0" align="center">
            <tr>
                <th>Error al {tipo} Favor contactar a ....................</th>
            </tr>
            <tr>
                <th><a href="/?mod=vehiculo">Regresar</a></th>
            </tr>
        </table>
        """

    def _message_BD_Vacia(self, tipo):
        return f"""
        <table border="0" align="center">
            <tr>
                <th>NO existen registros en la {tipo}</th>
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
                <th><a href="/?mod=vehiculo">Regresar</a></th>
            </tr>
        </table>
        """
