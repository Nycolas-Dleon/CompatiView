from flask import Flask, redirect, render_template, url_for, session, request, flash
from app.utils.data_manager import add_user, delete_user, load_users
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth import auth_bp
from app.security import login_required
from app.utils.data_manager import update_user

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
    
    if ";" in usuario:
        flash("O usuário não pode conter ponto e vírgula (;)", "error")
        return render_template("auth/cadastro.html")
    
    if len(senha) < 8:
        flash("A senha deve ter pelo menos 8 caracteres.", "error")
        return render_template("auth/cadastro.html")
    
    if len(senha) > 64:
        flash("A senha não pode conter mais que 64 caracteres", "error")
        return render_template("auth/cadastro.html")
    
    if ";" in senha:
        flash("A senha não pode conter ponto e vírgula (;)", "error")
        return render_template("auth/cadastro.html")

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
        usuarios = load_users()

        if username in load_users().keys() and check_password_hash(usuarios[username]['senha'], senha_tentada):
            session['usuario'] = username
            session['senha'] = usuarios[username]['senha']
            flash('Usuário logado com sucesso!', 'sucess')
            return redirect(url_for('main.selectionpage'))

        flash('Usuário ou senha incorretos!', 'error')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('main.homepage'))

@auth_bp.route('/alterar-senha', methods=['GET', 'POST'])
@login_required
def alterar_senha():

    if request.method == 'POST':
        senha_atual_inserida = request.form.get('senha-inserida') 
        senha_hash = session.get('senha')          
        nova_senha = request.form.get('nova_senha')      

        if check_password_hash(senha_hash, senha_atual_inserida):
            
            novo_hash = generate_password_hash(nova_senha)
            
            update_user(session.get('usuario'), senha_hash, novo_username='',nova_senha_hash=novo_hash)
            
            session['senha'] = novo_hash 
            
            flash('Alteração feita com sucesso!', 'sucess')

        else:
            flash('Erro! Senha atual incorreta.', 'error')

        return redirect(url_for('user.perfil'))

    return render_template('user/alterar-senha.html')

@auth_bp.route('/alterar-username', methods=['GET', 'POST'])
@login_required
def alterar_username():

    if request.method == 'POST':
        senha_atual_inserida = request.form.get('senha-inserida') 
        senha_hash_salva = session.get('senha')     
        novo_username = request.form.get('novo_username')

        if check_password_hash(senha_hash_salva, senha_atual_inserida):
            
            update_user(session.get('usuario'), senha_hash_salva, novo_username=novo_username, nova_senha_hash='')
            
            session['usuario'] = novo_username
            
            flash('Alteração feita com sucesso!', 'sucess')

        else:
            flash('Erro! Senha atual incorreta.', 'error')

        return redirect(url_for('user.perfil'))

    return render_template('user/alterar-username.html')

@auth_bp.route('/deletar-perfil', methods=['POST', 'GET'])
def remover_conta():

    if request.method == 'POST':
        username = session.get('usuario')
        senha_real = session.get('senha')
        senha_inserida = request.form.get('senha-inserida')

        if check_password_hash(senha_real, senha_inserida):
            delete_user(username)
            session.clear()
            flash('Sua conta foi deletada.', 'info')

    return redirect(url_for('main.homepage'))
