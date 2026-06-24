import os

# Inicializa classe Config com atributos de classe que pegam a chave secreta da memória e adicinam segurança contra http, xss e csrf.
class Config: 
    SECRET_KEY = os.environ.get('SECRET_KEY')

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = False

# Inicializa configuração de produção, que herda a classe de config mas muda o secure (agora o cookie apenas trafega se o protocolo for seguro).
class ProductionConfig(Config): 
    SESSION_COOKIE_SECURE = True

class DevelopmentConfig(Config):
    DEBUG = True
