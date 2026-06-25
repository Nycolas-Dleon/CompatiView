from flask import Flask, render_template, request
from config import DevelopmentConfig
from app.security import gerar_csrf_token, validar_csrf_token

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Disponibiliza a função gerar_csrf_token() nos templates jinja2 com o nome csrf_token().
    app.jinja_env.globals['csrf_token'] = gerar_csrf_token

    # Faz validação do token csrf em toda a requisição que for post antes de chegar na rota.
    @app.before_request
    def proteger_csrf():
        if request.method == 'POST':
            validar_csrf_token()

    # Registro de blueprints.
    from app.main import main_bp
    from app.user import user_bp
    from app.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(auth_bp)

    # Configura "nomes" no app. Isso serve para formatar os titulos que estão no banco de dados na hora da listagem.
    app.config["nomes"] = {
            'cpus' : 'Processadores',
            'gpus' : 'Placas de vídeo',
            'rams' : 'Memórias ram',
            'motherboards' : 'Placas mãe'
            }
    return app
