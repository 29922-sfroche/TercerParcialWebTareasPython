class Vehiculo:

    # Constructor: se ejecuta cuando se crea un objeto Vehiculo
    # Recibe la conexión a la base de datos
    def __init__(self, cn):
        # Atributos privados del vehículo (equivalente a private $ en PHP)
        self.__id = None            
        self.__placa = None         
        self.__marca = None         
        self.__motor = None         
        self.__chasis = None        
        self.__combustible = None   
        self.__anio = None          
        self.__color = None         
        self.__foto = None          
        self.__avaluo = None        

        # Guarda la conexión a la base de datos para usarla en los métodos
        self.con = cn


    # -------------------------------
    # LISTAR VEHÍCULOS
    # -------------------------------
    def get_list(self):

        # HTML inicial de la tabla de vehículos
        html = """
        <table border="1" align="center">
            <tr>
                <th colspan="8">Lista de Vehículos</th>
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

        # Consulta SQL para obtener los vehículos con su marca y color
        sql = """
        SELECT v.id, v.placa, m.descripcion AS marca,
               c.descripcion AS color, v.anio, v.avaluo
        FROM vehiculo v, color c, marca m
        WHERE v.marca = m.id AND v.color = c.id
        """

        # Crea el cursor para ejecutar la consulta
        # dictionary=True permite usar row['campo']
        cursor = self.con.cursor(dictionary=True)

        # Ejecuta la consulta SQL
        cursor.execute(sql)

        # Recorre todas las filas obtenidas de la base de datos
        for row in cursor.fetchall():

            # Debug: muestra el contenido del diccionario
            # en formato similar a print_r() de PHP
            html += "<pre>" + print_r_py(row) + "</pre>"

            # Agrega una fila HTML con los datos del vehículo
            html += f"""
            <tr>
                <td>{row['placa']}</td>
                <td>{row['marca']}</td>
                <td>{row['color']}</td>
                <td>{row['anio']}</td>
                <td>{row['avaluo']}</td>
                <td>BORRAR</td>
                <td>ACTUALIZAR</td>
                <td>DETALLE</td>
            </tr>
            """

        # Cierra la tabla HTML
        html += "</table>"

        # Cierra el cursor de la base de datos
        cursor.close()

        # Retorna todo el HTML generado
        return html


    # -------------------------------
    # MENSAJE DE ERROR
    # -------------------------------
    def _message_error(self, tipo):
        # Retorna un mensaje de error en formato HTML
        return f"""
        <table border="0" align="center">
            <tr>
                <th>Error al {tipo}. Favor contactar a ..............</th>
            </tr>
            <tr>
                <th><a href="/">Regresar</a></th>
            </tr>
        </table>
        """


# -------------------------------
# FUNCIÓN AUXILIAR TIPO print_r()
# -------------------------------
def print_r_py(diccionario):
    # Construye una salida similar a print_r() de PHP
    salida = "Array\n(\n"

    # Recorre el diccionario (clave => valor)
    for clave, valor in diccionario.items():
        salida += f"    [{clave}] => {valor}\n"

    # Cierra la estructura del array
    salida += ")\n"

    # Retorna el texto formateado
    return salida
