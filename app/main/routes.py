from flask import Flask, redirect, render_template, url_for, session, request, flash
from app.utils.compatibilidade import *
from app.utils.data_manager import load_json
from app import app 

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/selection')
def selectionpage():
    components = load_json()
    nomes = app.config["nomes"]
    if 'dados_usuario' not in session:
        session['dados_usuario'] =  {
            'cpu_user': None,
            'gpu_user': None,
            'motherboard_user': None,
            'ram_user': {
                'tamanho': None,
                'tipo': None,
                'quantidade': None
            }
        }
    dados_atuais = session.get('dados_usuario', {})
    return render_template('selection.html', components=components, nomes=nomes, escolha=dados_atuais)

@app.route('/adicionar', methods=['POST'])
def adicionar_componente():
    dados = session.get('dados_usuario')
    if not dados:
        return redirect(url_for('selectionpage'))

    form_enviado = request.form

    if 'tamanho' in form_enviado or 'tipo' in form_enviado or 'quantidade' in form_enviado:
        if form_enviado.get('tamanho'):
            dados['ram_user']['tamanho'] = form_enviado.get('tamanho')
        if form_enviado.get('tipo'):
            dados['ram_user']['tipo'] = form_enviado.get('tipo')
        if form_enviado.get('quantidade'):
            dados['ram_user']['quantidade'] = form_enviado.get('quantidade')

    if 'cpus' in form_enviado: 
        dados['cpu_user'] = form_enviado.get('cpus')
        
    if 'gpus' in form_enviado: 
        dados['gpu_user'] = form_enviado.get('gpus')
        
    if 'motherboards' in form_enviado:
        dados['motherboard_user'] = form_enviado.get('motherboards')

    session['dados_usuario'] = dados
    session.modified = True
    
    return redirect(url_for('selectionpage'))


@app.route('/remover', methods=['GET', 'POST'])
def remover_componente():
    dados = session.get('dados_usuario', {})
    form_enviado = request.form
    if form_enviado.get('tipo_componente') == 'cpu':
        dados['cpu_user'] = None

    if form_enviado.get('tipo_componente') == 'gpu': 
        dados['gpu_user'] = None

    if form_enviado.get('tipo_componente') == 'motherboard':
        dados['motherboard_user'] = None

    if form_enviado.get('tipo_componente') == 'ram':
        dados['ram_user']['tamanho'] = None
        dados['ram_user']['tipo'] = None
        dados['ram_user']['quantidade'] = None

    session['dados_usuario'] = dados
    session.modified = True
    return redirect(url_for('selectionpage'))

@app.route('/testarcompat', methods=['GET', 'POST'])
def testar_compatibilidade():
    dados_atuais = session.get('dados_usuario')
    if not dados_atuais:
        flash('01Nenhuma configuração encontrada.')
        return redirect(url_for('selectionpage'))

    if dados_atuais['gpu_user'] is None or dados_atuais['cpu_user'] is None or dados_atuais['motherboard_user'] is None or dados_atuais['ram_user']['quantidade'] == None or dados_atuais['ram_user']['tipo'] == None or dados_atuais['ram_user']['tamanho'] == None:
        flash('02Não foi possível verificar a compatibilidade! Preencha os campos vazios.')
        return redirect(url_for('selectionpage'))

    else:
        if not cpu_motherboard(dados_atuais['cpu_user'], dados_atuais['motherboard_user']):
            flash('03O processador não é compatível com o socket da placa-mãe.')

        if not ram_motherboard(dados_atuais['ram_user']['tipo'], dados_atuais['motherboard_user']): 
            flash('04O tipo de memória RAM não é suportado pela placa-mãe.')

        if not ram_cpu(dados_atuais['ram_user']['tipo'], dados_atuais['cpu_user']): 
            flash('05O processador não suporta esse tipo de memória RAM.')

        if not limite_ram(dados_atuais['ram_user']['quantidade'], dados_atuais['ram_user']['tamanho'], dados_atuais['motherboard_user']): 
            flash('06A placa-mãe não suporta essa quantidade de memória RAM.')

        if not limite_pentes(dados_atuais['ram_user']['quantidade'], dados_atuais['motherboard_user']):
            flash('07A placa mãe não possui slots suficientes para suportar o número de pentes de memória selecionados.')

        if cpu_motherboard(dados_atuais['cpu_user'], dados_atuais['motherboard_user']) and ram_motherboard(dados_atuais['ram_user']['tipo'], dados_atuais['motherboard_user']) and ram_cpu(dados_atuais['ram_user']['tipo'], dados_atuais['cpu_user']) and limite_ram(dados_atuais['ram_user']['quantidade'], dados_atuais['ram_user']['tamanho'], dados_atuais['motherboard_user']) and limite_pentes(dados_atuais['ram_user']['quantidade'], dados_atuais['motherboard_user']):
            flash('ecompativel')
    return redirect(url_for('selectionpage'))
    
@app.route("/componentes")
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
        "componentes.html",
        componentes=componentes_pagina,
        page=page,
        total_paginas=total_paginas
    )