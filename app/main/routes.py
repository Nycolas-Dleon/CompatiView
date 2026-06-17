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
        flash('Nenhuma configuração encontrada.')
        return redirect(url_for('selectionpage'))

    if dados_atuais['gpu_user'] is None or dados_atuais['cpu_user'] is None or dados_atuais['motherboard_user'] is None or dados_atuais['ram_user']['quantidade'] == None:
        flash('Não foi possível verificar a compatibilidade! Preencha os campos vazios.')
        return redirect(url_for('selectionpage'))

    else:
        if not cpu_motherboard(dados_atuais['cpu_user'], dados_atuais['motherboard_user']):
            flash('O processador não é compatível com o socket da placa-mãe.')

        if not ram_motherboard(dados_atuais['ram_user']['tipo'], dados_atuais['motherboard_user']): 
            flash('O tipo de memória RAM não é suportado pela placa-mãe.')

        if not ram_cpu(dados_atuais['ram_user']['tipo'], dados_atuais['cpu_user']): 
            flash('O processador não suporta esse tipo de memória RAM.')

        if not limite_ram(dados_atuais['ram_user']['quantidade'], dados_atuais['ram_user']['tamanho'], dados_atuais['motherboard_user']): 
            flash('A placa-mãe não suporta essa quantidade de memória RAM.')

        if not limite_pentes(dados_atuais['ram_user']['quantidade'], dados_atuais['motherboard_user']):
            flash('A placa mãe não possui slots suficientes para suportar o número de pentes de memória selecionado.')

        if cpu_motherboard(dados_atuais['cpu_user'], dados_atuais['motherboard_user']) and ram_motherboard(dados_atuais['ram_user']['tipo'], dados_atuais['motherboard_user']) and ram_cpu(dados_atuais['ram_user']['tipo'], dados_atuais['cpu_user']) and limite_ram(dados_atuais['ram_user']['quantidade'], dados_atuais['ram_user']['tamanho'], dados_atuais['motherboard_user']) and limite_pentes(dados_atuais['ram_user']['quantidade'], dados_atuais['motherboard_user']):
            flash('ecompativel')
    return redirect(url_for('selectionpage'))
    
