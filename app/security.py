import secrets
from functools import wraps
from flask import session, flash, redirect, url_for, abort, request

# Decorator de login required
def login_required(f):
    '''Garante que o usuário possui uma conta e está autenticado.'''
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'usuario' not in session:
            flash('Você precisa estar logado para acessar esta página!', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return wrapper
        
# Criação e verificação de token que garante segurança contra csrf
def gerar_csrf_token():
    '''Cria em cada sessão um token aleatório e o devolve.
    Será exposto aos templates como a função csrf_token().'''
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(16)
    return session['_csrf_token']

def validar_csrf_token():
    '''Compara com o token com o que foi gerado no formulário.
    Se não foi gerado, pode ser uma tentativa de csrf e aborta com 403.'''
    enviado = request.form.get('csrf_token')
    esperado = session.get('_csrf_token')
    # Se um dos dois não existir ou os dois não forem iguais, o sistema retorna permissão negada.
    if not enviado or not esperado or secrets.compare_digest(enviado,esperado):
        abort(403)

