class Matricula:

    # Constructor: se ejecuta al crear el objeto
    # Recibe la conexión a la base de datos
    def __init__(self, cn):
        # Atributos del objeto (equivalente a private $ en PHP)
        self.__id = None
        self.__fecha = None
        self.__vehiculo = None
        self.__agencia = None
        self.__anio = None

        # Guarda la conexión a la BD para usarla en los métodos
        self.con = cn

    # -------------------------------
    # LISTAR MATRÍCULAS
    # -------------------------------
    def get_list(self):

        # HTML inicial de la tabla
        html = """
        <table border="1" align="center" cellpadding="5">
            <tr>
                <th colspan="8">Lista de Matrículas</th>
            </tr>
            <tr>
                <th>Fecha</th>
                <th>Vehículo</th>
                <th>Agencia</th>
                <th>Año</th>
                <th colspan="3">Acciones</th>
            </tr>
        """

        # Consulta SQL para obtener las matrículas con sus relaciones
        sql = """
        SELECT m.id, m.fecha,
               v.placa AS vehiculo,
               a.descripcion AS agencia,
               m.anio
        FROM matricula m
        LEFT JOIN vehiculo v ON m.vehiculo = v.id
        LEFT JOIN agencia a ON m.agencia = a.id
        """

        # Crea el cursor para ejecutar consultas
        # dictionary=True permite usar row['campo']
        cursor = self.con.cursor(dictionary=True)

        # Ejecuta la consulta SQL
        cursor.execute(sql)

        # Recorre todas las filas obtenidas
        for row in cursor.fetchall(): #fetachall() obtiene todas las filas

            # Debug: imprime el diccionario al estilo print_r de PHP
            html += "<pre>" + print_r_py(row) + "</pre>"

            # Agrega una fila HTML con los datos de la matrícula
            html += f"""
            <tr>
                <td>{row['fecha']}</td>
                <td>{row['vehiculo']}</td>
                <td>{row['agencia']}</td>
                <td>{row['anio']}</td>
                <td>Borrar</td>
                <td>Editar</td>
                <td>Detalle</td>
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
        # Retorna una tabla HTML con un mensaje de error
        return f"""
        <table border="0" align="center">
            <tr>
                <th>Error al {tipo}. Favor contactar al administrador.</th>
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
    # Construye una salida similar a print_r de PHP
    salida = "Array\n(\n"
    for clave, valor in diccionario.items():
        salida += f"    [{clave}] => {valor}\n"
    salida += ")\n"
    return salida
