import base64
import datetime

class Vehiculo:

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

    def _b64(self, txt: str) -> str:
        return base64.b64encode(txt.encode("utf-8")).decode("utf-8")

    # =========================
    # LISTA
    # =========================
    def get_list(self):
        d_new = self._b64("new/0")

        html = f"""
        <table border="1" align="center">
            <tr><th colspan="8">Lista de Vehículos</th></tr>
            <tr><th colspan="8"><a href="/?d={d_new}">Nuevo</a></th></tr>
            <tr>
                <th>Placa</th><th>Marca</th><th>Color</th>
                <th>Año</th><th>Avalúo</th><th colspan="3">Acciones</th>
            </tr>
        """

        cur = self.con.cursor(dictionary=True)
        sql = """
            SELECT v.id, v.placa,
                   m.descripcion AS marca,
                   c.descripcion AS color,
                   v.anio, v.avaluo
            FROM vehiculo v, marca m, color c
            WHERE v.marca=m.id AND v.color=c.id;
        """
        cur.execute(sql)
        rows = cur.fetchall()

        for r in rows:
            d_del = self._b64(f"del/{r['id']}")
            d_act = self._b64(f"act/{r['id']}")
            d_det = self._b64(f"det/{r['id']}")

            html += f"""
            <tr>
                <td>{r['placa']}</td>
                <td>{r['marca']}</td>
                <td>{r['color']}</td>
                <td>{r['anio']}</td>
                <td>{r['avaluo']}</td>
                <td><a href="/?d={d_del}">Borrar</a></td>
                <td><a href="/?d={d_act}">Actualizar</a></td>
                <td><a href="/?d={d_det}">Detalle</a></td>
            </tr>
            """

        html += "</table>"
        return html

    # =========================
    # FORMULARIO (NEW / ACT)
    # =========================
    def get_form(self, id_=0):

        debug = ""

        if id_ == 0:
            # NEW
            self.placa = ""
            self.marca = None
            self.motor = ""
            self.chasis = ""
            self.combustible = None
            self.anio = None
            self.color = None
            self.foto = None
            self.avaluo = ""
            op = "new"
            flag_file = ""   # enabled
            flag_avaluo = "" # enabled

        else:
            # ACT (precarga)
            cur = self.con.cursor(dictionary=True)
            cur.execute("SELECT * FROM vehiculo WHERE id=%s;", (id_,))
            row = cur.fetchone()

            if not row:
                return self._message_error(f"tratar de actualizar el vehiculo con id= {id_}<br>")

            debug = f"<br>REGISTRO A MODIFICAR:<br><pre>{row}</pre>"

            self.placa = row.get("placa", "")
            self.marca = row.get("marca", None)
            self.motor = row.get("motor", "")
            self.chasis = row.get("chasis", "")
            self.combustible = row.get("combustible", None)
            self.anio = row.get("anio", None)
            self.color = row.get("color", None)
            self.foto = row.get("foto", None)
            self.avaluo = row.get("avaluo", "")

            # En tu PHP en act ponías enabled; si quisieras bloquear, aquí usarías "disabled"
            flag_file = ""    # o "disabled"
            flag_avaluo = ""  # o "disabled"
            op = "update"

        combustibles = ["Gasolina", "Diesel", "Eléctrico"]

        html = f"""
        {debug}
        <form name="Form_vehiculo" method="POST" action="/" enctype="multipart/form-data">
            <input type="hidden" name="id" value="{id_}">
            <input type="hidden" name="op" value="{op}">

            <table border="2" align="center">
                <tr>
                    <th colspan="2">DATOS VEHÍCULO</th>
                </tr>

                <tr>
                    <td>Placa:</td>
                    <td><input type="text" size="6" name="placa" value="{self.placa}"></td>
                </tr>

                <tr>
                    <td>Marca:</td>
                    <td>{self._get_combo_db("marca", "id", "descripcion", "marcaCMB", self.marca)}</td>
                </tr>

                <tr>
                    <td>Motor:</td>
                    <td><input type="text" size="15" name="motor" value="{self.motor}"></td>
                </tr>

                <tr>
                    <td>Chasis:</td>
                    <td><input type="text" size="15" name="chasis" value="{self.chasis}"></td>
                </tr>

                <tr>
                    <td>Combustible:</td>
                    <td>{self._get_radio(combustibles, "combustibleRBT", self.combustible)}</td>
                </tr>

                <tr>
                    <td>Año:</td>
                    <td>{self._get_combo_anio("anio", 1950, self.anio)}</td>
                </tr>

                <tr>
                    <td>Color:</td>
                    <td>{self._get_combo_db("color", "id", "descripcion", "colorCMB", self.color)}</td>
                </tr>

                <tr>
                    <td>Foto:</td>
                    <td><input type="file" name="foto" {flag_file}></td>
                </tr>

                <tr>
                    <td>Avalúo:</td>
                    <td><input type="text" size="8" name="avaluo" value="{self.avaluo}" {flag_avaluo}></td>
                </tr>

                <tr>
                    <th colspan="2">
                        <input type="submit" name="Guardar" value="GUARDAR">
                    </th>
                </tr>

                <tr>
                    <th colspan="2"><a href="/">Regresar</a></th>
                </tr>
            </table>
        </form>
        """
        return html

    # =========================
    # DETALLE COMPLETO
    # =========================
    def get_detail_vehiculo(self, id_):
        cur = self.con.cursor(dictionary=True)
        sql = """
            SELECT v.placa,
                   m.descripcion AS marca,
                   v.motor, v.chasis, v.combustible,
                   v.anio,
                   c.descripcion AS color,
                   v.foto, v.avaluo
            FROM vehiculo v, marca m, color c
            WHERE v.id=%s AND v.marca=m.id AND v.color=c.id;
        """
        cur.execute(sql, (id_,))
        row = cur.fetchone()

        if not row:
            return self._message_error(f"desplegar el detalle del vehiculo con id= {id_}<br>")

        avaluo = float(row["avaluo"])
        valor_matricula = avaluo * 0.10

        avaluo_fmt = f"{avaluo:,.2f}"
        matricula_fmt = f"{valor_matricula:,.2f}"

        # Si tu carpeta "imagenes" está en el proyecto, lo correcto en web es /imagenes/...
        img_src = f"/imagenes/autos/{row['foto']}"

        html = f"""
        <table border="1" align="center">
            <tr><th colspan="2">DATOS DEL VEHÍCULO</th></tr>

            <tr><td>Placa: </td><td>{row['placa']}</td></tr>
            <tr><td>Marca: </td><td>{row['marca']}</td></tr>
            <tr><td>Motor: </td><td>{row['motor']}</td></tr>
            <tr><td>Chasis: </td><td>{row['chasis']}</td></tr>
            <tr><td>Combustible: </td><td>{row['combustible']}</td></tr>
            <tr><td>Año: </td><td>{row['anio']}</td></tr>
            <tr><td>Color: </td><td>{row['color']}</td></tr>

            <tr><td>Avalúo: </td><th>${avaluo_fmt} USD</th></tr>
            <tr><td>Valor Matrícula: </td><th>${matricula_fmt} USD</th></tr>

            <tr>
                <th colspan="2"><img src="{img_src}" width="300px"></th>
            </tr>

            <tr><th colspan="2"><a href="/">Regresar</a></th></tr>
        </table>
        """
        return html

    # =========================
    # ELIMINAR
    # =========================
    def delete_vehiculo(self, id_):
        cur = self.con.cursor()
        cur.execute("DELETE FROM vehiculo WHERE id=%s;", (id_,))
        self.con.commit()
        return self._message_ok("eliminó")

    # =========================
    # COMBO DB (marca/color)
    # =========================
    def _get_combo_db(self, tabla, valor, etiqueta, nombre, defecto=None):
        cur = self.con.cursor(dictionary=True)
        cur.execute(f"SELECT {valor}, {etiqueta} FROM {tabla};")
        rows = cur.fetchall()

        html = f'<select name="{nombre}">'
        for r in rows:
            selected = ' selected' if defecto == r[valor] else ''
            html += f'<option value="{r[valor]}"{selected}>{r[etiqueta]}</option>'
        html += '</select>'
        return html

    # =========================
    # COMBO AÑO
    # =========================
    def _get_combo_anio(self, nombre, anio_inicial, defecto=None):
        anio_actual = datetime.datetime.now().year
        html = f'<select name="{nombre}">'
        for i in range(anio_inicial, anio_actual + 1):
            selected = ' selected' if defecto == i else ''
            html += f'<option value="{i}"{selected}>{i}</option>'
        html += '</select>'
        return html

    # =========================
    # RADIOS COMBUSTIBLE
    # =========================
    def _get_radio(self, arreglo, nombre, defecto=None):
        html = '<table border="0" align="left">'
        for etiqueta in arreglo:
            checked = ' checked' if defecto == etiqueta else ''
            html += f"""
            <tr>
                <td>{etiqueta}</td>
                <td><input type="radio" value="{etiqueta}" name="{nombre}"{checked}></td>
            </tr>
            """
        html += "</table>"
        return html

    # =========================
    # MENSAJES
    # =========================
    def _message_error(self, tipo):
        return f"""
        <table border="0" align="center">
            <tr><th>Error al {tipo}. Favor contactar a ..............</th></tr>
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
