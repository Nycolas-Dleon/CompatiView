from flask import Flask, redirect, render_template, url_for, session, request, flash
from werkzeug.security import generate_password_hash 
from app.utils.data_manager import append_components, load_json, update_user
from app.security import login_required
from app.utils.data_manager import load_users
from . import user_bp

@user_bp.route("/componentes")
@login_required
def listar_componentes():
    components = load_json() # Os componentes na forma de dicionário Python
    componentes = [] # Uma lista vazia onde cada elemento da lista é um dict contendo as informações de cada linha da listagem das peças

    for categoria, itens in components.items(): #.items() devolve uma sequência de pares (chave, valor)

        # Isso ignora a RAM
        if categoria == "rams":
            continue # faz o loop seguir

        for nome, dados in itens.items(): # pares na nova lista itens 

            componentes.append({ # cada elemento da lista é um dicionário contendo nome, categoria e preço
                "nome": dados.get("chipset", nome), # se não houver chipset devolve nome
                "categoria": categoria,
                "preco": dados.get("price") * 5.50
            })

    # Filtragem
    categoria_filtro = request.args.get("categoria", "")
    
    if categoria_filtro != "":
        componentes_filtrados = []

        for componente in componentes:

            if componente["categoria"] == categoria_filtro:

                componentes_filtrados.append(componente)

        componentes = componentes_filtrados

    # Paginação
    ITENS_POR_PAGINA = 12 # constante que determina número de itens por página

    page = request.args.get("page", 1, type=int) # page faz parte da url, se não especificar page é 1

    inicio = (page - 1) * ITENS_POR_PAGINA # isso calcula a primeira linha, se for 1 a primeira linha é o indice 0
    fim = inicio + ITENS_POR_PAGINA # isso naturalmente calcula onde acaba a lista da página

    componentes_pagina = componentes[inicio:fim] # fatiando a lista pra mostrar só o que a página deve mostrar

    def calcular_total_paginas(total_itens, itens_por_pagina): # pra ver e arredonadar o numero de paginas
        if total_itens % itens_por_pagina == 0:
         return total_itens // itens_por_pagina

        return (total_itens // itens_por_pagina) + 1

    total_paginas = calcular_total_paginas(len(componentes), ITENS_POR_PAGINA)

    return render_template(
        "user/componentes.html",
        componentes=componentes_pagina,
        page=page,
        total_paginas=total_paginas
    )

@user_bp.route("/salvar", methods=['POST', 'GET'])
@login_required
def salvar():
    dados_atuais = session.get('dados_usuario', {}).copy()

    if dados_atuais['gpu_user'] is None or dados_atuais['cpu_user'] is None or dados_atuais['motherboard_user'] is None or dados_atuais['ram_user']['quantidade'] == None or dados_atuais['ram_user']['tipo'] == None or dados_atuais['ram_user']['tamanho'] == None:
        flash('00Não foi possível salvar essa configuração! Preencha todos os campos.')
        return redirect(url_for('main.selectionpage'))

    username = session.get('usuario', {})
    lista = load_users(username, saves=True)
    dados_atuais['id'] = len(lista) # Cria um id de salvamento (será útil no endpoint de remoção).
    lista.append(dados_atuais) 
    append_components(lista, username)
    flash('08Sua configuração foi salva com sucesso!')

    return redirect(url_for('main.selectionpage'))

@user_bp.route('/remover-salvamento', methods=['POST', 'GET'])
@login_required
def remover_salvamento(save_id:int):
    nome_usuario = session.get('usuario','')
    saves_usuario = load_users(nome_usuario, saves=True)
    saves_usuario.pop(save_id - 1)
    append_components(saves_usuario, nome_usuario)
    flash('Sua save foi removida com sucesso!', 'sucess')
    return redirect(url_for('user/perfil'))

@user_bp.route('/alterar-senha', methods=['GET', 'POST'])
@login_required
def alterar_senha():

    if request.method == 'POST':
        senha_atual_inserida = request.form.get('senha')
        senha_atual_correta = session.get('senha')
        nova_senha = request.form.get('nova_senha')

        if senha_atual_inserida == senha_atual_correta:
            update_user(session.get('usuario'), senha_atual_inserida, nova_senha_hash=generate_password_hash(nova_senha))
            flash('Alteração feita com sucesso!', 'sucess')

        else:
            flash('Erro! Usuário não encontrado ou senha atual incorreta.', 'error')

        return redirect(url_for('user/perfil.html'))

    return render_template('user/alterar-senha.html')

@user_bp.route('/alterar-username', methods=['GET', 'POST'])
@login_required
def alterar_username():

    if request.method == 'POST':

        senha_atual_inserida = request.form.get('senha')
        senha_atual_correta = session.get('senha')
        novo_username = request.form.get('novo_username')

        if senha_atual_inserida == senha_atual_correta:
            update_user(session.get('usuario'), senha_atual_inserida, novo_username=novo_username)
            flash('Alteração feita com sucesso!', 'sucess')

        else:
            flash('Erro! Usuário não encontrado ou senha atual incorreta.', 'error')

        return redirect(url_for('user/perfil.html'))

    return render_template('user/alterar-username.html')
