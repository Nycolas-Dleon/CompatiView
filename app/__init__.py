from flask import Flask

app = Flask(__name__)
app.config["nomes"] = {
        'cpus' : 'Processadores',
        'gpus' : 'Placas de vídeo',
        'memory' : 'Memórias ram',
        'motherboards' : 'Placas mãe'
        }
from app.main import routes
