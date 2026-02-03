from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <head>
        <meta charset="utf-8">
        <title>LOGIN - PYTHON</title>
    </head>
    <body>
        <center>
            <img src="img/logo.png" width="700" height="200"><br><br>
            <h1>Desarrollo Web para la integración de tecnologías</h1>
            <h2>LOGIN - PYTHON</h2>

            <table border="1" style="width:100%">
                <tr>
                    <td align="center"><h3>TEMA</h3></td>
                    <td align="center"><h3>DESCRIPCIÓN</h3></td>
                </tr>
                <tr>
                    <td>
                        <a href="routes/index.py">SESIONES</a>
                    </td>
                    <td>Sesiones en Python (Flask)</td>
                </tr>
                <tr>
                    <td>AUTENTICACIÓN DE USUARIOS</td>
                    <td>Formulario Login para realizar la sesión</td>
                </tr>
            </table>
        </center>
    </body>
    </html>
    """
