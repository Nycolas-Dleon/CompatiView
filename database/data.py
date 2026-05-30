import json
# Programa utilizado para converter o banco de dados em algo mais legível
with open("nomedoarquivooriginal.json", "r", encoding="utf-8") as arquivo:
    dados = json.load(arquivo)

with open("nomedonovoarquivo.json", "w", encoding="utf-8") as arquivo:
    json.dump(dados, arquivo, indent=4, ensure_ascii=False)