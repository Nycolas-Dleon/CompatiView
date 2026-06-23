from flask import Flask

app = Flask(__name__)
app.secret_key = 'efa3a5ed9dcf704b693f5c6b174af151ffa6e5e13ba7a54f7396acae37efc21d'
app.config["nomes"] = {
        'cpus' : 'Processadores',
        'gpus' : 'Placas de vídeo',
        'rams' : 'Memórias ram',
        'motherboards' : 'Placas mãe'
        }
from app.main import routes
