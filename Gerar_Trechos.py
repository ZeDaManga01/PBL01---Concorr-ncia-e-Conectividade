import json
# Lista de capitais brasileiras
capitais = [
    "Aracaju", "Belém", "Belo Horizonte", "Boa Vista", "Brasília", 
    "Campo Grande", "Cuiabá", "Curitiba", "Florianópolis", "Fortaleza", 
    "Goiânia", "João Pessoa", "Macapá", "Maceió", "Manaus", 
    "Natal", "Palmas", "Porto Alegre", "Porto Velho", "Recife", 
    "Rio Branco", "Rio de Janeiro", "Salvador", "São Luís", "São Paulo", 
    "Teresina", "Vitória"
]
# Gerando os voos entre todas as capitais
voos = []
for origem in capitais:
    for destino in capitais:
        if origem != destino:  # Não cria voo de uma capital para si mesma
            voo = {
                "Origem": origem.lower(),
                "Destino": destino.lower(),
                "Vagas": 15  # Quantidade fixa de vagas por voo
            }
            voos.append(voo)
file_path = 'Voos.json'
with open(file_path, 'w') as f:
    json.dump(voos, f, ensure_ascii=False, indent=4)
file_path
