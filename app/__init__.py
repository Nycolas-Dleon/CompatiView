from flask import Flask

app = Flask(__name__)
app.config["nomes"] = {
        'cpus' : 'Processadores',
        'gpus' : 'Placas de vídeo',
        'rams' : 'Memórias ram',
        'motherboards' : 'Placas mãe',
        'slot_amount' : 'Quantidade',
        'ram_size' : 'Tamanho',
        'memory_type' : 'Tipo'
        }
from app.main import routes
