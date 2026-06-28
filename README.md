# CompatiView
IFPB - Projeto Integrador do Primeiro Período - Engenharia de Software 2026.1

O CompatiView é um site dedicado a ajudar você a montar o seu computador. Selecionando as peças do nosso banco de dados você pode verificar se elas são, ou não são, compatíveis, e assim fazer as melhores escolhas na hora de montar o seu Desktop!
Nosso site conta com diversas funcionalidades como criar e salvar suas builds e acessar informações sobre peças como seu preço médio no mercado e suas diferentes marcas disponíveis!

## Integrantes
| Nome | Matrícula |
| --- | --- |
| Lucas Linhares | 202614320020 |
| Wesley Lins | 202614320026 |
| Nycolas D'leon | 2026143200xx |
| João Pedro | 2026143200xx |

## Linguagens Utilizadas
* Python 3
* HTML5
* CSS3
* JavaScript

## Dependências
* Flask 3.1.3
* Werkzeug 3.1.8
* blinker 1.9.0
* click 8.4.1
* colorama 0.4.6
* itsdangerous 2.2.0
* MarkupSafe 3.0.3
* python-dotenv 1.0.1
* Jinja2

## Diagrama de Casos de Uso
![Diagrama de Casos de Uso](/app/static/imgs/diagrama_compatiview_final.drawio.png)

## Estrutura do Projeto
```
CompatiView/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── app/
│ ├── data/
│ │ ├── components.json
│ │ └── users.csv
│ │
│ ├── main/
│ │ ├── init.py
│ │ ├── forms.py
│ │ └── routes.py
│ │
│ ├── utils/
│ │ ├── init.py
│ │ ├── compatibilidade.py
│ │ └── data_manager.py
│ │
│ ├── static/
│ │ ├── css/...
│ │ ├── js/...
│ │ └── imgs/...
│ │
│ └── templates/
│   ├── base.html
│   ├── index.html
│   ├── selection.html
│   └── componentes.html
```

## Como acessar o site
### 1. Clone o repositório:
```bash
git clone https://github.com/Nycolas-Dleon/CompatiView.git
cd CompatiView
```
### 2. Crie e ative a venv:
```bash
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```
### 3. Baixe as dependências:
```bash
pip install -r requirements.txt
```
### 4. Agora é só rodar:
```bash
flask run
```

### 5. E no navegador:
```
http://127.0.0.1:3001
```
