from flask import Flask
import mysql.connector
from routes.vehiculo import Vehiculo
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
# RUTA ÚNICA
# -------------------------------
@app.route("/")
def index():

    cn = conectar()
    objetoVehiculo = Vehiculo(cn)
    objetoMatricula = Matricula(cn)

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Vehículos y Matrículas</title>

        <style>
            body {
                font-family: Arial;
                margin: 0;
                background-color: #f4f4f9;
            }
            .navbar {
                height: 64px;
                background-color: #2c3e50;
                color: white;
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0 40px;
            }
            .contenido {
                padding: 30px;
            }
            select {
                padding: 6px;
                font-size: 15px;
            }
        </style>

        <script>
            // 2 = Vehículos (por defecto)
            // 3 = Matrículas
            let vista = 2;

            function cambiarVista(valor) {
                vista = parseInt(valor);

                document.getElementById("vehiculos").style.display =
                    (vista === 2) ? "block" : "none";

                document.getElementById("matriculas").style.display =
                    (vista === 3) ? "block" : "none";
            }
        </script>

    </head>
    <body>

        <div class="navbar">
            <div><b>Ejercicios</b></div>
            <div>
                <select onchange="cambiarVista(this.value)">
                    <option value="2" selected>Vehículos</option>
                    <option value="3">Matrículas</option>
                </select>
            </div>
        </div>

        <div class="contenido">

            <!-- VEHÍCULOS -->
            <div id="vehiculos">
    """

    # ambas tablas se generan UNA sola vez
    html += objetoVehiculo.get_list()

    html += """
            </div>

            <!-- MATRÍCULAS -->
            <div id="matriculas" style="display:none">
    """

    html += objetoMatricula.get_list()

    html += """
            </div>

        </div>
    </body>
    </html>
    """

    cn.close()
    return html

# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)