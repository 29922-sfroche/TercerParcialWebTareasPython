from flask import Flask
import mysql.connector
#from vehiculo import Vehiculo
from routes.matricula import Matricula

# Crea la aplicación Flask (equivalente a index.php)
app = Flask(__name__)

# -------------------------------
# FUNCIÓN DE CONEXIÓN A LA BD
# -------------------------------
def conectar():
    # Datos de conexión a la base de datos
    server = "localhost"
    user = "root"
    password = "123"
    database = "matriculacionfinal"

    # Crea la conexión a MySQL (objeto)
    c = mysql.connector.connect(
        host=server,
        user=user,
        password=password,
        database=database
    )

    # Configura el charset (acentos, ñ, etc.)
    c.set_charset_collation(charset='utf8')

    # Retorna la conexión
    return c

# -------------------------------
# RUTA PRINCIPAL
# -------------------------------
@app.route("/")
def index():
    # Obtiene la conexión
    cn = conectar()

    # Crea los objetos y les pasa la conexión
    #objetoVehiculo = Vehiculo(cn)
    objetoMatricula = Matricula(cn)

    # HTML base de la página
    html = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html>
    <head>
        <title>Matriculas Vehículos PARTE II</title>
        <meta charset="utf-8">
    </head>
    <body>
    """

    # Llama a los métodos que generan las tablas HTML
    #html += objetoVehiculo.get_list()
    html += objetoMatricula.get_list()

    # Cierra el HTML
    html += """
    </body>
    </html>
    """

    # Cierra la conexión a la BD
    cn.close()

    # Devuelve el HTML al navegador
    return html

# -------------------------------
# EJECUCIÓN DE LA APP
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
