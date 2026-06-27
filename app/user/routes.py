from flask import Flask, redirect, render_template, url_for, session, request, flash 
from app.utils.data_manager import append_components, load_json
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
    flash('Sua configuração foi salva com sucesso!', 'sucess')

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

