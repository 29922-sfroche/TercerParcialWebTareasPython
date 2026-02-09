# routes/vehiculo.py
import os
import random
import base64
from datetime import datetime
from flask import request

# ===============================
# RUTA DE IMÁGENES (igual a ../imagenes/autos/)
# ===============================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "imagenes")


class vehiculo:

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

    # =======================
    # UPDATE
    # =======================
    def update_vehiculo(self):

        self.id = request.form.get("id")
        self.placa = request.form.get("placa")
        self.motor = request.form.get("motor")
        self.chasis = request.form.get("chasis")

        self.marca = request.form.get("marcaCMB")
        self.anio = request.form.get("anio")
        self.color = request.form.get("colorCMB")
        self.combustible = request.form.get("combustibleRBT")

        sql = f"""
        UPDATE vehiculo SET
            placa='{self.placa}',
            marca={self.marca},
            motor='{self.motor}',
            chasis='{self.chasis}',
            combustible='{self.combustible}',
            anio='{self.anio}',
            color={self.color}
        WHERE id={self.id};
        """

        try:
            cur = self.con.cursor()
            cur.execute(sql)
            self.con.commit()
            return self._message_ok("modificó")
        except Exception:
            return self._message_error("al modificar")

    # =======================
    # CREATE
    # =======================
    def save_vehiculo(self):

        self.placa = request.form.get("placa")
        self.motor = request.form.get("motor")
        self.chasis = request.form.get("chasis")
        self.avaluo = request.form.get("avaluo")

        self.marca = request.form.get("marcaCMB")
        self.anio = request.form.get("anio")
        self.color = request.form.get("colorCMB")
        self.combustible = request.form.get("combustibleRBT")

        file_obj = request.files.get("foto")
        if file_obj is None:
            return self._message_error("Cargar la imagen")

        self.foto = file_obj.filename
        os.makedirs(IMAGES_DIR, exist_ok=True)
        path = os.path.join(IMAGES_DIR, self.foto)

        try:
            file_obj.save(path)
        except Exception:
            return self._message_error("Cargar la imagen")

        sql = f"""
        INSERT INTO vehiculo VALUES(
            NULL,
            '{self.placa}',
            {self.marca},
            '{self.motor}',
            '{self.chasis}',
            '{self.combustible}',
            '{self.anio}',
            {self.color},
            '{self.foto}',
            {self.avaluo}
        );
        """

        try:
            cur = self.con.cursor()
            cur.execute(sql)
            self.con.commit()
            return self._message_ok("guardó")
        except Exception:
            return self._message_error("guardar")

    # =======================
    # FORM
    # =======================
    def get_form(self, id=None):

        if id is None:
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

        else:
            sql = f"SELECT * FROM vehiculo WHERE id={id};"
            cur = self.con.cursor(dictionary=True)
            cur.execute(sql)
            row = cur.fetchone()

            if row is None:
                return self._message_error(f"tratar de actualizar el vehiculo con id= {id}")

            self.placa = row["placa"]
            self.marca = row["marca"]
            self.motor = row["motor"]
            self.chasis = row["chasis"]
            self.combustible = row["combustible"]
            self.anio = row["anio"]
            self.color = row["color"]
            self.foto = row["foto"]
            self.avaluo = row["avaluo"]

            flag = "disabled"
            op = "update"

        combustibles = ["Gasolina", "Diesel", "Eléctrico"]

        return f"""
        <form name="vehiculo" method="POST" action="/" enctype="multipart/form-data">

            <input type="hidden" name="id" value="{id or 0}">
            <input type="hidden" name="op" value="{op}">

            <table border="1" align="center">
                <tr><th colspan="2">DATOS VEHÍCULO</th></tr>
                <tr><td>Placa:</td><td><input type="text" name="placa" value="{self.placa or ''}" required></td></tr>
                <tr><td>Marca:</td><td>{self._get_combo_db("marca","id","descripcion","marcaCMB",self.marca)}</td></tr>
                <tr><td>Motor:</td><td><input type="text" name="motor" value="{self.motor or ''}" required></td></tr>
                <tr><td>Chasis:</td><td><input type="text" name="chasis" value="{self.chasis or ''}" required></td></tr>
                <tr><td>Combustible:</td><td>{self._get_radio(combustibles,"combustibleRBT",self.combustible)}</td></tr>
                <tr><td>Año:</td><td>{self._get_combo_anio("anio",1980,self.anio)}</td></tr>
                <tr><td>Color:</td><td>{self._get_combo_db("color","id","descripcion","colorCMB",self.color)}</td></tr>
                <tr><td>Foto:</td><td><input type="file" name="foto" {flag}></td></tr>
                <tr><td>Avalúo:</td><td><input type="text" name="avaluo" value="{self.avaluo or ''}" {flag} required></td></tr>
                <tr><th colspan="2"><input type="submit" name="Guardar" value="GUARDAR"></th></tr>
                <tr><th colspan="2"><a href="/">Regresar</a></th></tr>
            </table>
        </form>
        """

    # =======================
    # LIST
    # =======================
    def get_list(self):

        d_new = base64.b64encode(b"new/0").decode()

        html = f"""
        <table border="1" align="center">
        <h1>VEHÍCULOS PARTE III</h1>
            <tr><th colspan="8">Lista de Vehículos</th></tr>
            <tr><th colspan="8"><a href="/?d={d_new}">Nuevo</a></th></tr>
            <tr>
                <th>Placa</th><th>Marca</th><th>Color</th><th>Año</th><th>Avalúo</th>
                <th colspan="3">Acciones</th>
            </tr>
        """

        sql = """
        SELECT v.id, v.placa, m.descripcion as marca,
               c.descripcion as color, v.anio, v.avaluo
        FROM vehiculo v, color c, marca m
        WHERE v.marca=m.id AND v.color=c.id;
        """

        cur = self.con.cursor(dictionary=True)
        cur.execute(sql)

        for row in cur.fetchall():
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
                <td><a href="/?d={d_del}">Borrar</a></td>
                <td><a href="/?d={d_act}">Actualizar</a></td>
                <td><a href="/?d={d_det}">Detalle</a></td>
            </tr>
            """

        html += "</table>"
        return html

    # =======================
    # DETAIL
    # =======================
    def get_detail_vehiculo(self, id):

        sql = f"""
        SELECT v.placa, m.descripcion as marca, v.motor, v.chasis,
               v.combustible, v.anio, c.descripcion as color,
               v.foto, v.avaluo
        FROM vehiculo v, color c, marca m
        WHERE v.id={id} AND v.marca=m.id AND v.color=c.id;
        """

        cur = self.con.cursor(dictionary=True)
        cur.execute(sql)
        row = cur.fetchone()

        if row is None:
            return self._message_error(f"tratar de editar el vehiculo con id= {id}")

        return f"""
        <table border="1" align="center">
            <tr><th colspan="2">DATOS DEL VEHÍCULO</th></tr>
            <tr><td>Placa:</td><td>{row['placa']}</td></tr>
            <tr><td>Marca:</td><td>{row['marca']}</td></tr>
            <tr><td>Motor:</td><td>{row['motor']}</td></tr>
            <tr><td>Chasis:</td><td>{row['chasis']}</td></tr>
            <tr><td>Combustible:</td><td>{row['combustible']}</td></tr>
            <tr><td>Año:</td><td>{row['anio']}</td></tr>
            <tr><td>Color:</td><td>{row['color']}</td></tr>
            <tr><td>Avalúo:</td><th>${row['avaluo']} USD</th></tr>
            <tr><td>Valor Matrícula:</td><th>${self._calculo_matricula(row['avaluo'])} USD</th></tr>
            <tr><th colspan="2"><img src="/imagenes/{row['foto']}" width="300px"/></th></tr>
            <tr><th colspan="2"><a href="/">Regresar</a></th></tr>
        </table>
        """

    # =======================
    # DELETE
    # =======================
    def delete_vehiculo(self, id):

        sql = f"DELETE FROM vehiculo WHERE id={id};"

        try:
            cur = self.con.cursor()
            cur.execute(sql)
            self.con.commit()
            return self._message_ok("ELIMINÓ")
        except Exception:
            return self._message_error("eliminar")

    # =======================
    # HELPERS
    # =======================
    def _get_combo_db(self, tabla, valor, etiqueta, nombre, defecto):
        html = f'<select name="{nombre}">'
        sql = f"SELECT {valor},{etiqueta} FROM {tabla};"
        cur = self.con.cursor(dictionary=True)
        cur.execute(sql)

        for row in cur.fetchall():
            sel = "selected" if defecto == row[valor] else ""
            html += f'<option value="{row[valor]}" {sel}>{row[etiqueta]}</option>\n'

        html += "</select>"
        return html

    def _get_combo_anio(self, nombre, anio_inicial, defecto):
        html = f'<select name="{nombre}">'
        anio_actual = datetime.now().year
        for i in range(anio_inicial, anio_actual + 1):
            sel = "selected" if defecto == i else ""
            html += f'<option value="{i}" {sel}>{i}</option>\n'
        html += "</select>"
        return html

    def _get_radio(self, arreglo, nombre, defecto):
        html = '<table border=0 align="left">'
        for etiqueta in arreglo:
            checked = "checked" if defecto in (None, etiqueta) else ""
            html += f"""
            <tr>
                <td>{etiqueta}</td>
                <td><input type="radio" name="{nombre}" value="{etiqueta}" {checked}></td>
            </tr>
            """
        html += "</table>"
        return html

    def _calculo_matricula(self, avaluo):
        return format(float(avaluo) * 0.10, ".2f")

    def _message_error(self, tipo):
        return f"""
        <table border="0" align="center">
            <tr><th>Error al {tipo}. Favor contactar a .................... </th></tr>
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
