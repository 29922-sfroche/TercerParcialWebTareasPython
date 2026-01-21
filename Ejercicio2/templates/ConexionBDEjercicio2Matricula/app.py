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
<style>
    /* Reset básico */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: sans-serif;
        background-color: #f4f4f9;
    }

    /* ===== NAVBAR ===== */
    .navbar {
        width: 100%;
        height: 64px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #2c3e50;
        padding: 0 40px;
        color: #ecf0f1;
    }

    .navbar-left {
        font-size: 20px;
        font-weight: bold;
        letter-spacing: 0.5px;
    }

    .navbar-right {
        display: flex;
        gap: 20px;
    }

    .navbar-right a {
        color: #ecf0f1;
        text-decoration: none;
        font-weight: 600;
        padding: 8px 12px;
        border-radius: 4px;
        transition: background-color 0.2s ease;
    }

    .navbar-right a:hover {
        background-color: rgba(255, 255, 255, 0.15);
    }

    /* ===== CONTENIDO ===== */
    .contenido {
        padding: 40px;
    }

    .contenedor-carpetas {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
    }

    .tarjeta-carpeta {
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .titulo-carpeta {
        font-weight: bold;
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        margin-bottom: 15px;
        padding-bottom: 5px;
    }

    ul {
        list-style: none;
    }

    li {
        margin: 8px 0;
    }

    a.link-html {
        text-decoration: none;
        color: white;
        display: block;
        padding: 8px;
        background-color: #3498db;
        border-radius: 4px;
    }

    a.link-html:hover {
        background-color: #2980b9;
    }

    a.link-py {
        text-decoration: none;
        color: white;
        display: block;
        padding: 8px;
        background-color: #e67e22;
        border-radius: 4px;
    }

    a.link-py:hover {
        background-color: #d35400;
    }
</style>

    </head>
    <body>
        <nav class="navbar">
            <div class="navbar-left">Ejercicios</div>
            <div class="navbar-right">
                <a href="/ConexionBDEjercicio1Vehiculo/app.py">Vehículos</a>
                <a href="/ConexionBDEjercicio2Matricula/app.py">Matrículas</a>
            </div>
        </nav>
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
