from flask import Flask, redirect, render_template, url_for, session, request, flash
from app.utils.data_manager import add_user, load_users
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth import auth_bp

@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    if request.method == "GET":
        return render_template("auth/cadastro.html")

    usuario = request.form["usuario"].strip()
    senha = request.form["senha"]

    # Validação

    if not usuario.isascii() or not senha.isascii():
        flash("Usuário e senha não podem conter caracteres especias.", "error")
        return render_template("auth/cadastro.html")

    if not usuario:
        flash("Informe um usuário.", "error")
        return render_template("auth/cadastro.html")

    if not senha:
        flash("Informe uma senha.", "error")
        return render_template("auth/cadastro.html")

    if len(usuario) < 3:
        flash("O usuário deve ter pelo menos 3 caracteres.", "error")
        return render_template("auth/cadastro.html")
    
    if len(usuario) > 15:
        flash("O usuário não pode ter mais que 15 caracteres", "error")
        return render_template("auth/cadastro.html")
    
    '''if ";" in usuario or " " in usuario:
        flash("O usuário não pode conter os caracteres ';' ou espaços em branco", "error")
        return render_template("auth/cadastro.html")'''
    
    if len(senha) < 8:
        flash("A senha deve ter pelo menos 8 caracteres.", "error")
        return render_template("auth/cadastro.html")
    
    if len(senha) > 64:
        flash("A senha não pode conter mais que 64 caracteres", "error")
        return render_template("auth/cadastro.html")
    
    '''if ";" in senha or " " in senha:
        flash("A senha não pode conter os caracteres ';' ou espaços em branco", "error")
        return render_template("auth/cadastro.html")'''

    # Verificação de conta

    users = load_users()

    if usuario in users:
        flash("Esse usuário já existe.", "error")
        return render_template("auth/cadastro.html")

    # Cadastro

    senha_hash = generate_password_hash(senha)

    add_user(usuario, senha_hash)

    flash("Cadastro realizado com sucesso!", "success")

    return redirect(url_for("auth.login"))

@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('usuario')
        senha_tentada = request.form.get('senha')

        if username in load_users().keys() and check_password_hash(load_users()[username]['senha'], senha_tentada):
            session['usuario'] = username
            session['senha'] = senha_tentada
            return redirect(url_for('main.selectionpage'))

        flash('Usuário ou senha incorretos!', 'error')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('main.homepage'))

