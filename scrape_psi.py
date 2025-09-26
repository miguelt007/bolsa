import requests
import json

url = "https://investing-com6.p.rapidapi.com/web-crawling/api/markets/v2/indices/performance"
headers = {
    "X-RapidAPI-Key": "dbcf86698cmshd04b1b46934dd15p11474ejsn267bbdb81678",
    "X-RapidAPI-Host": "investing-com6.p.rapidapi.com"
}
params = {
    "market": "PT"
}

response = requests.get(url, headers=headers, params=params)
if response.status_code != 200:
    raise Exception(f"Erro na API: {response.status_code}")

dados_brutos = response.json()
print("🔍 Dados recebidos da API:")
print(json.dumps(dados_brutos, indent=2, ensure_ascii=False))  # Log para debugging

dados_filtrados = []
for item in dados_brutos:
    dados_filtrados.append({
        "indice": item.get("name"),
        "cotacao": item.get("price"),
        "variacao": item.get("change"),
        "percentual": item.get("change_percent"),
        "hora": item.get("time")
    })

with open("data/psi.json", "w", encoding="utf-8") as f:
    json.dump(dados_filtrados, f, ensure_ascii=False, indent=2)

print("✅ psi.json gerado com sucesso.")
