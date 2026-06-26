from flask import render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from app.auth import auth_bp


@auth_bp.route("/registro", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("auth/registro.html")

    usuario = request.form["usuario"]
    senha = request.form["senha"]

    senha_hash = generate_password_hash(senha)

    with open("data/users.csv", "a", encoding="utf-8") as f:
        f.write(f"{usuario};{senha_hash};\n")

    return redirect(url_for("main.index"))