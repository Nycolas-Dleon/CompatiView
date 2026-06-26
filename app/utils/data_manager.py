import json
from pathlib import Path
from flask import session

'''
O fluxo de relacionar os paths com variáveis usando a biblioteca pathlib serve para evitar problemas de caminho para pastas em outros computadores ou com diferentes sistemas operacionais.
Sem ele, como o caminho relativo dos arquivos pode variar, o sistema pode quebrar.
'''
# Inicializa variável com o caminho da pasta atual (utils/)
PATH_DIR = Path(__file__).resolve().parent
# Do "utils/app/" vai para a pasta "data/"
PATH_DATA = PATH_DIR.parent / 'data'

## Função de leitura do .json (Essa função será importada no models.py para ser utilizada em outras funções que a necessitem.)
def load_json(categoria:str=''):
    '''
    load_json(categoria='') transforma o conteúdo de um arquivo json em um dicionário python.

    No contexto do sistema, esse dicionário listará todas as peças que poderão ser utilizadas nos testes de compatibilidade.

    Parameters 
    ----------
    categoria : str
        Esse parâmetro serve para filtrar a categoria de peça que será retornada, fazendo com que o dicionário seja, consequentemente, menor.
        categorias válidas são -> 'cpus', 'gpus', 'motherboards', 'rams'.
        Ao não passar nenhum parâmetro, o dicionário retornado estará completo, sem nenhum filtro.
    '''
    # Pega o arquivo .json para ser utilizado nas funções
    PATH_JSON = PATH_DATA / 'components.json'

    # Pega o conteúdo que está em components.json e o transforma em um dicionário python.
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
    
    elif categoria == 'rams':
        return componentes_geral["rams"]

def load_users():
    '''
    load_users() transforma o banco de dados em um dicionário python maleável para facilitar a autenticação e listagem de salvamentos.
    '''
    users = {}
    PATH_CSV = PATH_DATA / 'users.csv'

    with open(PATH_CSV, 'r') as arquivo:
        linhas = arquivo.read().splitlines()

    for i in range(1, len(linhas)):
        if not linhas[i].split(';'):
            continue

        linha = linhas[i].split(';')


        if len(linha) < 3:
            continue

        if linha[0] not in users.keys():
            users[linha[0]] = {}
            users[linha[0]]['senha'] = linha[1]
            try:
                users[linha[0]]['salvamentos'] = json.loads(linha[2])
            except json.JSONDecodeError:
                users[linha[0]]['salvamentos'] = []

    return users

def append_components(lista_modificada:list, usuario:str):
    '''
    append_components() modifica a lista de salvamentos de um usuário específico.

    Parameters 
    ----------
    lista_modificada : list
        Esse parâmetro indica a lista que sobrescreverá a lista atual.

    usuario : str
        Esse parâmetro indica qual usuário passará pela mudança.
    '''
    PATH_CSV = PATH_DATA / 'users.csv'
    with open(PATH_CSV, 'r') as arquivo:
        linhas = arquivo.read().splitlines()

    for i in range(1, len(linhas)):
        linha = linhas[i].split(';')

        if linha[0] == usuario:
            salvamentos_str = json.dumps(lista_modificada)
            linha[2] = salvamentos_str
            linhas[i] = ';'.join(linha)
            break

    with open(PATH_CSV, 'w', encoding='utf-8') as arquivo:
        for linha_att in linhas:
            arquivo.write(linha_att + '\n')


