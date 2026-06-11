from flask import Flask, redirect, render_template, url_for, session, request
from app.utils.data_manager import load_json
from app import models
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

@app.route('/testarcompat')
def testar_compatibilidade():
    return render_template('selectionpage.html')
    
