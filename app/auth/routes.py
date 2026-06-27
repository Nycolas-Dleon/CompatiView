from flask import Flask, redirect, render_template, url_for, session, request, flash
from app.utils.data_manager import add_user, load_users
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth import auth_bp


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "GET":
        return render_template("auth/cadastro.html")
    usuario = request.form["usuario"]
    senha = request.form["senha"]
    senha_hash = generate_password_hash(senha)

    # função que adiciona usuário no arquivo csv.
    add_user(usuario, senha_hash)

    flash('Usuário cadastrado com sucesso!', 'sucess')
    return redirect(url_for("main.homepage"))

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('usuario')
        senha_tentada = request.form.get('senha')

        if username in load_users().keys() and check_password_hash(load_users()[username]['senha'], senha_tentada):
            session['usuario'] = username
            session['senha'] = senha_tentada
            flash('Usuário logado com sucesso!', 'sucess')
            return redirect(url_for('main.selectionpage'))

        flash('Usuário ou senha incorretos!', 'error')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('main.homepage'))

