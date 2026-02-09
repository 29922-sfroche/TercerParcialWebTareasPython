# app.py
from flask import Flask, request, send_from_directory
import os
from index_python import ejecutar_index

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ===============================
# PANTALLA INICIAL (index.html)
# ===============================
@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
  <head>
    <title>FORMULARIO</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>

    <link rel="stylesheet" href="/Recursos/estilos.css" type="text/css"/>
  </head>

  <body>

    <div id="header">
      <img src="/Recursos/img/logo_ESPE.png"
           style="position:absolute;left:350px;top:40px;width:500px;height:89px;">
    </div>

    <div id="navBar" class="Texto">
      <table align="center" border="0">
        <tr>
          <td><a href="/index?mod=vehiculo">Formulario Vehiculo</a></td>
          <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td>
          <td><a href="/index?mod=matricula">Formulario Matricula</a></td>
        </tr>
      </table>
    </div>

    <div id="leftMenu">
      <a href="FormLogin.html" class="Boton">LOGIN</a>
    </div>

    <div id="content" class="Texto">
      <h2>Desarrollo de aplicaciones WEB</h2>
      <p>Estudiante: Alisson Cuenca</p>
      <p>NRC: ______</p>
      <p>Fecha: 27/01/2026</p>
    </div>

    <div id="rightMenu">
      <iframe height="290" width="390"
              src="https://www.youtube.com/embed/WS_3AjYN-TA"
              frameborder="1" allowfullscreen></iframe>
    </div>

    <div id="footer" class="Texto">
      <a href="FormContacto.html">Contacto</a>
    </div>

  </body>
</html>
"""


# ===============================
# INDEX DINÁMICO (index.php)
# ===============================
@app.route("/index", methods=["GET", "POST"])
def index_python():
    return ejecutar_index(request)

@app.route("/index_python", methods=["GET", "POST"])
def index_python_alias():
    return ejecutar_index(request)

# ===============================
# RECURSOS ESTÁTICOS
# ===============================
@app.route("/Recursos/<path:archivo>")
def recursos(archivo):
    return send_from_directory(os.path.join(BASE_DIR, "Recursos"), archivo)


@app.route("/imagenes/<path:archivo>")
def imagenes(archivo):
    return send_from_directory(os.path.join(BASE_DIR, "imagenes"), archivo)


# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
