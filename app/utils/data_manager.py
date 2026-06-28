import json
from pathlib import Path

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

def load_users(username:str='',saves:bool=False):
    '''
    load_users() transforma o banco de dados em um dicionário python maleável para facilitar a autenticação e listagem de salvamentos.

    Parameters 
    ----------
    username : str
        Esse parâmetro indica o nome de usuário de referência para filtrar sua lista de salvamentos.

    saves : bool
        Esse parâmetro define se o retorno será o dicionário contendo todos os usuários ou apenas uma lista com os salvamentos de um user específico.
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
    if saves:
        return users[username]['salvamentos']

    return users

def append_components(lista_modificada:list, usuario:str):
    '''
    append_components() modifica a lista de salvamentos de um usuário específico.

    Parameters 
    ----------
    lista_modificada : list
        Esse parâmetro indica a modificação que sobrescreverá a lista atual.

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

def add_user(usuario, senha_hash):
    '''
    add_user() adiciona um novo usuário no arquivo csv.

    Parameters 
    ----------
    usuario : str
        Determina o nome de usuário que será salvo.
    
    senha_hash : str
        Determina a senha que será salva naquele usuário.
    '''

    PATH_CSV = PATH_DATA / 'users.csv'

    with open(PATH_CSV, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{usuario};{senha_hash};[]\n")

def update_user(username, senha_hash, novo_username:str='', nova_senha_hash:str=''):
    '''
    update_user() modifica informações do usuário (username e senha).
    Essa função apenas é capaz de modificar um dos parâmetros por vez.

    Parameters 
    ----------
    username : str
        Esse parâmetro indica o nome se usuário que solicitou a mudança dos dados.

    senha_hash : str
        Esse parâmetro indica a senha inserida pelo usuário para requerir mudança de dados. Se essa senha diferir da sua senha atual real, o sistema retornará um erro.

    novo_username : str
        Esse parâmetro indica o novo nome de usuário que irá substituir o antigo. Por padrão, esse parâmetro é vazio, e, se apenas ele estiver vazio, a única mudança ocorrerá na senha.

    nova_senha_hash : str
        Esse parâmetro indica a nova senha que irá substituir a antiga. Por padrão, esse parâmetro também é vazio, e se unicamente ele estiver vazio, isso significa que a única mudança que o usuário quer fazer é na senha.
    '''
    PATH_CSV = PATH_DATA / 'users.csv'
    with open(PATH_CSV, 'r') as arquivo:
        linhas = arquivo.read().splitlines()

    linhas_atualizadas = []
    usuario_encontrado = False

    if linhas:
        linhas_atualizadas.append(linhas[0])

    for linha in linhas[1:]:
        dados = linha.split(';')
        
        if dados[0] == username and dados[1] == senha_hash:
            usuario_encontrado = True

            if novo_username and not nova_senha_hash:
                dados[0] = novo_username

            elif nova_senha_hash and not novo_username:
                dados[1] = nova_senha_hash

        linha = ';'.join(dados)
        linhas_atualizadas.append(linha)
    
    if usuario_encontrado:
        with open(PATH_CSV, 'w') as arq:
            arq.write('\n'.join(linhas_atualizadas) + '\n')

def delete_user(usuario:str):
    '''
    delete_user() deleta todas as informações do usuário passado.
    '''
    PATH_CSV = PATH_DATA / 'users.csv'
    with open(PATH_CSV, 'r') as arquivo:
        linhas = arquivo.read().splitlines()
    
    arquivo_alterado = []
    arquivo_alterado.append(linhas[0])
    usuario_encontrado = False
    
    for linha in linhas[1:]:
        linha_atual = linha.split(';')
        if linha_atual[0] == usuario:
            usuario_encontrado = True
            continue
        arquivo_alterado.append(linha)

    if usuario_encontrado:
        with open(PATH_CSV, 'w') as arq:
            arq.write('\n'.join(arquivo_alterado) + '\n')

