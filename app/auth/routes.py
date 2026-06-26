from flask import Flask, redirect, render_template, url_for, session, request, flash
from app.utils.data_manager import load_users
from werkzeug.security import generate_password_hash, check_password_hash
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

    return redirect(url_for("main.homepage"))

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('usuario')
        senha_tentada = request.form.get('senha')

        if username in load_users().keys() and check_password_hash(load_users()[username]['senha'], senha_tentada):
            session['usuario'] = username
            return redirect(url_for('main.selectionpage'))

        flash('Usuário ou senhas incorretos.', 'error')

    return render_template('auth/login.html')
