from flask import Flask, session, redirect

app = Flask(__name__)
app.secret_key = "sesiones_python"

@app.route("/")
def cerrar():
    session.clear()
    return redirect("index.py")
