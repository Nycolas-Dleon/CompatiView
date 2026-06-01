import json
import csv
from pathlib import Path

'''
O fluxo de relacionar os paths com variáveis usando a biblioteca pathlib serve para evitar problemas de caminho para pastas em outros computadores ou com diferentes sistemas operacionais.
Sem ele, como o caminho relativo dos arquivos pode variar, o sistema pode quebrar.
'''
# Inicializa variável com o caminho da pasta atual (app/)
PATH_DIR = Path(__file__).resolve().parent
# Do "app/" vai para a pasta "data/"
PATH_DATA = PATH_DIR / 'data'

## Função de leitura do .json (Essa função será importada no models.py para ser utilizada em outras funções que a necessitem.)
def load_json(categoria:str=''):
    '''
    load_json(categoria='') transforma o conteúdo de um arquivo json em um dicionário python.

    No contexto do sistema, esse dicionário listará todas as peças que poderão ser utilizadas nos testes de compatibilidade.

    Parameters 
    ----------
    categoria : str
        Esse parâmetro serve para filtrar a categoria de peça que será retornada, fazendo com que o dicionário seja, consequentemente, menor.
        categorias válidas são -> 'cpus', 'gpus', 'motherboards', 'psu', 'memory' e ''.
    '''
    # Pega o arquivo .json para ser utilizado nas funções
    PATH_JSON = PATH_DATA / 'components.json'

    # Pega o conteúdo que estão em components.json e transforma em um dicionário python.
    with open(PATH_JSON, 'r', encoding='utf-8') as arquivo:
        componentes_geral = json.load(arquivo)

    # Retorna um resultado dependente do parâmetro que foi passado.
    if categoria == '':
        return componentes_geral

    elif categoria == 'cpus':
        return componentes_geral["cpus"]

    elif categoria == 'gpus':
        return componentes_geral["gpus"]

    elif categoria == 'motherboards':
        return componentes_geral["motherboards"]
    
    elif categoria == 'memory':
        return componentes_geral["memory"]

