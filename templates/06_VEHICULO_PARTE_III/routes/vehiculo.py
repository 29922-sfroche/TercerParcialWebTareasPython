import os
import random
import base64
from datetime import datetime
from flask import request

# =====================================================
# RUTA REAL DEL PROYECTO (equivalente a ../imagenes/autos/)
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "imagenes", "autos")


class vehiculo:

    def __init__(self, cn):
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
        self.con = cn

    # *********************** 3.1 METODO update_vehiculo() ***********************
    def update_vehiculo(self):

        # $this->id = $_POST['id'];
        self.id = request.form.get("id")
        self.placa = request.form.get("placa")
        self.motor = request.form.get("motor")
        self.chasis = request.form.get("chasis")

        self.marca = request.form.get("marcaCMB")
        self.anio = request.form.get("anio")
        self.color = request.form.get("colorCMB")
        self.combustible = request.form.get("combustibleRBT")

        sql = (
            "UPDATE vehiculo SET placa='{placa}',\n"
            "marca={marca},\n"
            "motor='{motor}',\n"
            "chasis='{chasis}',\n"
            "combustible='{combustible}',\n"
            "anio='{anio}',\n"
            "color={color}\n"
            "WHERE id={id};"
        ).format(
            placa=self.placa,
            marca=self.marca,
            motor=self.motor,
            chasis=self.chasis,
            combustible=self.combustible,
            anio=self.anio,
            color=self.color,
            id=self.id
        )

        # echo $sql;
        # exit;
        # print(sql)

        try:
            cur = self.con.cursor()
            cur.execute(sql)
            self.con.commit()
            return self._message_ok("modificó")
        except Exception:
            return self._message_error("al modificar")

    # *********************** 3.2 METODO save_vehiculo() ***********************
    def save_vehiculo(self):

        self.placa = request.form.get("placa")
        self.motor = request.form.get("motor")
        self.chasis = request.form.get("chasis")
        self.avaluo = request.form.get("avaluo")

        self.marca = request.form.get("marcaCMB")
        self.anio = request.form.get("anio")
        self.color = request.form.get("colorCMB")
        self.combustible = request.form.get("combustibleRBT")

        # echo "<br> FILES <br>";
        # echo "<pre>";
        # print_r($_FILES);
        # echo "</pre>";
        print("<br> FILES <br>")
        print("<pre>")
        print(request.files)
        print("</pre>")

        file_obj = request.files.get("foto")
        if file_obj is None:
            return self._message_error("Cargar la imagen")

        self.foto = self._get_name_file(file_obj.filename, 12)

        os.makedirs(IMAGES_DIR, exist_ok=True)
        path = os.path.join(IMAGES_DIR, self.foto)

        try:
            file_obj.save(path)
        except Exception:
            return self._message_error("Cargar la imagen")

        sql = (
            "INSERT INTO vehiculo VALUES(NULL,\n"
            "'{placa}',\n"
            "{marca},\n"
            "'{motor}',\n"
            "'{chasis}',\n"
            "'{combustible}',\n"
            "'{anio}',\n"
            "{color},\n"
            "'{foto}',\n"
            "{avaluo});"
        ).format(
            placa=self.placa,
            marca=self.marca,
            motor=self.motor,
            chasis=self.chasis,
            combustible=self.combustible,
            anio=self.anio,
            color=self.color,
            foto=self.foto,
            avaluo=self.avaluo
        )

        try:
            cur = self.con.cursor()
            cur.execute(sql)
            self.con.commit()
            return self._message_ok("guardó")
        except Exception:
            return self._message_error("guardar")


    # *********************** 3.3 METODO _get_name_file() **************************************************
    #
    # private function _get_name_file($nombre_original, $tamanio){
    #     $tmp = explode(".",$nombre_original); //Divido el nombre por el punto y guardo en un arreglo
    #     $numElm = count($tmp); //cuento el número de elemetos del arreglo
    #     $ext = $tmp[$numElm-1]; //Extraer la última posición del arreglo.
    #     $cadena = "";
    #     for($i=1;$i<=$tamanio;$i++){
    #         $c = rand(65,122);
    #         if(($c >= 91) && ($c <=96)){
    #             $c = NULL;
    #              $i--;
    #          }else{
    #             $cadena .= chr($c);
    #         }
    #     }
    #     return $cadena . "." . $ext;
    # }
    #
    def _get_name_file(self, nombre_original, tamanio):

        # $tmp = explode(".",$nombre_original);
        tmp = nombre_original.split(".")

        # $numElm = count($tmp);
        numElm = len(tmp)

        # $ext = $tmp[$numElm-1];
        ext = tmp[numElm - 1]

        # $cadena = "";
        cadena = ""

        # for($i=1;$i<=$tamanio;$i++){
        i = 1
        while i <= tamanio:

            # $c = rand(65,122);
            c = random.randint(65, 122)

            # if(($c >= 91) && ($c <=96)){
            if 91 <= c <= 96:
                # $c = NULL;
                # $i--;
                continue
            else:
                # $cadena .= chr($c);
                cadena += chr(c)
                i += 1

        # return $cadena . "." . $ext;
        return cadena + "." + ext

    # *************************************** PARTE I ************************************************************
    #
    # /*Aquí se agregó el parámetro:  $defecto*/
    #
    def _get_combo_db(self, tabla, valor, etiqueta, nombre, defecto):

        # $html = '<select name="' . $nombre . '">';
        html = '<select name="' + nombre + '">'

        # $sql = "SELECT $valor,$etiqueta FROM $tabla;";
        sql = "SELECT {v},{e} FROM {t};".format(
            v=valor,
            e=etiqueta,
            t=tabla
        )

        # $res = $this->con->query($sql);
        cur = self.con.cursor(dictionary=True)
        cur.execute(sql)

        # while($row = $res->fetch_assoc()){
        for row in cur.fetchall():

            # ImpResultQuery($row);
            # $html .= ($defecto == $row[$valor])? ...
            if defecto == row[valor]:
                html += (
                    '<option value="' + str(row[valor]) +
                    '" selected>' + str(row[etiqueta]) +
                    '</option>' + "\n"
                )
            else:
                html += (
                    '<option value="' + str(row[valor]) +
                    '">' + str(row[etiqueta]) +
                    '</option>' + "\n"
                )

        # $html .= '</select>';
        html += '</select>'

        # return $html;
        return html

    # /*Aquí se agregó el parámetro:  $defecto*/
    def _get_combo_anio(self, nombre, anio_inicial, defecto):

        # $html = '<select name="' . $nombre . '">';
        html = '<select name="' + nombre + '">'

        # $anio_actual = date('Y');
        anio_actual = datetime.now().year

        # for($i=$anio_inicial;$i<=$anio_actual;$i++){
        i = anio_inicial
        while i <= anio_actual:

            # $html .= ($i == $defecto)? ...
            if i == defecto:
                html += (
                    '<option value="' + str(i) +
                    '" selected>' + str(i) +
                    '</option>' + "\n"
                )
            else:
                html += (
                    '<option value="' + str(i) +
                    '">' + str(i) +
                    '</option>' + "\n"
                )

            i += 1

        # $html .= '</select>';
        html += '</select>'

        # return $html;
        return html

    # /*Aquí se agregó el parámetro:  $defecto*/
    def _get_radio(self, arreglo, nombre, defecto):

        # $html = '
        # <table border=0 align="left">';
        html = """
        <table border=0 align="left">
        """

        # //CODIGO NECESARIO EN CASO QUE EL USUARIO NO SE ESCOJA UNA OPCION
        #
        # foreach($arreglo as $etiqueta){
        for etiqueta in arreglo:

            html += """
            <tr>
                <td>""" + etiqueta + """</td>
                <td>
            """

            # if($defecto == NULL){
            if defecto is None:
                # OPCION PARA GRABAR UN NUEVO VEHICULO (id=0)
                html += (
                    '<input type="radio" value="' + etiqueta +
                    '" name="' + nombre + '" checked/></td>'
                )
            else:
                # OPCION PARA MODIFICAR UN VEHICULO EXISTENTE
                if defecto == etiqueta:
                    html += (
                        '<input type="radio" value="' + etiqueta +
                        '" name="' + nombre + '" checked/></td>'
                    )
                else:
                    html += (
                        '<input type="radio" value="' + etiqueta +
                        '" name="' + nombre + '"/></td>'
                    )

            html += """
            </tr>
            """

        # $html .= '
        # </table>';
        html += """
        </table>
        """

        # return $html;
        return html


    # ************************************* PARTE II ****************************************************
    def get_form(self, id=None):

        if id is None:
            # $this->placa = NULL;
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
            sql = "SELECT * FROM vehiculo WHERE id={};".format(id)
            cur = self.con.cursor(dictionary=True)
            cur.execute(sql)
            row = cur.fetchone()

            num = cur.rowcount

            if num == 0:
                mensaje = "tratar de actualizar el vehiculo con id= " + str(id)
                return self._message_error(mensaje)
            else:
                # ***** TUPLA ENCONTRADA *****
                print("<br>TUPLA <br>")
                print("<pre>")
                print(row)
                print("</pre>")

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

        combustibles = [
            "Gasolina",
            "Diesel",
            "Eléctrico"
        ]

        html = """
        <form name="vehiculo" method="POST" action="/" enctype="multipart/form-data">

        <input type="hidden" name="id" value="{id}">
        <input type="hidden" name="op" value="{op}">

        <table border="1" align="center">
            <tr>
                <th colspan="2">DATOS VEHÍCULO</th>
            </tr>
            <tr>
                <td>Placa:</td>
                <td><input type="text" size="6" name="placa" value="{placa}" required></td>
            </tr>
            <tr>
                <td>Marca:</td>
                <td>{marca}</td>
            </tr>
            <tr>
                <td>Motor:</td>
                <td><input type="text" size="15" name="motor" value="{motor}" required></td>
            </tr>
            <tr>
                <td>Chasis:</td>
                <td><input type="text" size="15" name="chasis" value="{chasis}" required></td>
            </tr>
            <tr>
                <td>Combustible:</td>
                <td>{combustible}</td>
            </tr>
            <tr>
                <td>Año:</td>
                <td>{anio}</td>
            </tr>
            <tr>
                <td>Color:</td>
                <td>{color}</td>
            </tr>
            <tr>
                <td>Foto:</td>
                <td><input type="file" name="foto" {flag}></td>
            </tr>
            <tr>
                <td>Avalúo:</td>
                <td><input type="text" size="8" name="avaluo" value="{avaluo}" {flag} required></td>
            </tr>
            <tr>
                <th colspan="2"><input type="submit" name="Guardar" value="GUARDAR"></th>
            </tr>
            <tr>
                <th colspan="2"><a href="/">Regresar</a></th>
            </tr>
        </table>
        </form>
        """.format(
            id=id,
            op=op,
            placa=self.placa or "",
            marca=self._get_combo_db("marca", "id", "descripcion", "marcaCMB", self.marca),
            motor=self.motor or "",
            chasis=self.chasis or "",
            combustible=self._get_radio(combustibles, "combustibleRBT", self.combustible),
            anio=self._get_combo_anio("anio", 1980, self.anio),
            color=self._get_combo_db("color", "id", "descripcion", "colorCMB", self.color),
            flag=flag,
            avaluo=self.avaluo or ""
        )

        return html

    # *************************************************************************************
    def get_list(self):

        d_new = "new/0"
        d_new_final = base64.b64encode(d_new.encode()).decode()

        html = """
        <table border="1" align="center">
            <tr>
                <th colspan="8">Lista de Vehículos</th>
            </tr>
            <tr>
                <th colspan="8"><a href="/?d={dnew}">Nuevo</a></th>
            </tr>
            <tr>
                <th>Placa</th>
                <th>Marca</th>
                <th>Color</th>
                <th>Año</th>
                <th>Avalúo</th>
                <th colspan="3">Acciones</th>
            </tr>
        """.format(dnew=d_new_final)

        sql = """
        SELECT v.id, v.placa, m.descripcion as marca,
               c.descripcion as color, v.anio, v.avaluo
        FROM vehiculo v, color c, marca m
        WHERE v.marca=m.id AND v.color=c.id;
        """

        cur = self.con.cursor(dictionary=True)
        cur.execute(sql)

        for row in cur.fetchall():

            d_del = base64.b64encode(("del/" + str(row["id"])).encode()).decode()
            d_act = base64.b64encode(("act/" + str(row["id"])).encode()).decode()
            d_det = base64.b64encode(("det/" + str(row["id"])).encode()).decode()

            html += """
            <tr>
                <td>{placa}</td>
                <td>{marca}</td>
                <td>{color}</td>
                <td>{anio}</td>
                <td>{avaluo}</td>
                <td><a href="/?d={delid}">Borrar</a></td>
                <td><a href="/?d={actid}">Actualizar</a></td>
                <td><a href="/?d={detid}">Detalle</a></td>
            </tr>
            """.format(
                placa=row["placa"],
                marca=row["marca"],
                color=row["color"],
                anio=row["anio"],
                avaluo=row["avaluo"],
                delid=d_del,
                actid=d_act,
                detid=d_det
            )

        html += "</table>"
        return html

    # *************************************************************************************
    def get_detail_vehiculo(self, id):

        sql = """
        SELECT v.placa, m.descripcion as marca, v.motor, v.chasis,
               v.combustible, v.anio, c.descripcion as color,
               v.foto, v.avaluo
        FROM vehiculo v, color c, marca m
        WHERE v.id={} AND v.marca=m.id AND v.color=c.id;
        """.format(id)

        cur = self.con.cursor(dictionary=True)
        cur.execute(sql)
        row = cur.fetchone()

        if row is None:
            mensaje = "tratar de editar el vehiculo con id= " + str(id)
            return self._message_error(mensaje)

        html = """
        <table border="1" align="center">
            <tr>
                <th colspan="2">DATOS DEL VEHÍCULO</th>
            </tr>
            <tr>
                <td>Placa:</td>
                <td>{placa}</td>
            </tr>
            <tr>
                <td>Marca:</td>
                <td>{marca}</td>
            </tr>
            <tr>
                <td>Motor:</td>
                <td>{motor}</td>
            </tr>
            <tr>
                <td>Chasis:</td>
                <td>{chasis}</td>
            </tr>
            <tr>
                <td>Combustible:</td>
                <td>{combustible}</td>
            </tr>
            <tr>
                <td>Anio:</td>
                <td>{anio}</td>
            </tr>
            <tr>
                <td>Color:</td>
                <td>{color}</td>
            </tr>
            <tr>
                <td>Avalúo:</td>
                <th>${avaluo} USD</th>
            </tr>
            <tr>
                <td>Valor Matrícula:</td>
                <th>${matricula} USD</th>
            </tr>
            <tr>
                <th colspan="2">
                    <img src="imagenes/{foto}" width="300px"/>
                </th>
            </tr>
            <tr>
                <th colspan="2"><a href="/">Regresar</a></th>
            </tr>
        </table>
        """.format(
            placa=row["placa"],
            marca=row["marca"],
            motor=row["motor"],
            chasis=row["chasis"],
            combustible=row["combustible"],
            anio=row["anio"],
            color=row["color"],
            avaluo=row["avaluo"],
            matricula=self._calculo_matricula(row["avaluo"]),
            foto=row["foto"]
        )

        return html

    # *************************************************************************************
    def delete_vehiculo(self, id):

        sql = "DELETE FROM vehiculo WHERE id={};".format(id)

        try:
            cur = self.con.cursor()
            cur.execute(sql)
            self.con.commit()
            return self._message_ok("ELIMINÓ")
        except Exception:
            return self._message_error("eliminar")

    # *************************************************************************************
    def _calculo_matricula(self, avaluo):
        return format(float(avaluo) * 0.10, ".2f")

    # *************************************************************************************
    def _message_error(self, tipo):

        html = """
        <table border="0" align="center">
            <tr>
                <th>Error al {tipo}. Favor contactar a .................... </th>
            </tr>
            <tr>
                <th><a href="/">Regresar</a></th>
            </tr>
        </table>
        """.format(tipo=tipo)

        return html

    # *************************************************************************************
    def _message_ok(self, tipo):

        html = """
        <table border="0" align="center">
            <tr>
                <th>El registro se  {tipo} correctamente</th>
            </tr>
            <tr>
                <th><a href="/">Regresar</a></th>
            </tr>
        </table>
        """.format(tipo=tipo)

        return html

# ============================== FIN SCRIPT ==============================
