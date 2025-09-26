import requests
import json

url = "https://investing-com6.p.rapidapi.com/web-crawling/api/markets/indices"
headers = {
    "X-RapidAPI-Key": "dbcf86698cmshd04b1b46934dd15p11474ejsn267bbdb81678",  # substitui pela tua chave real
    "X-RapidAPI-Host": "investing-com6.p.rapidapi.com"
}

response = requests.get(url, headers=headers)
if response.status_code != 200:
    raise Exception(f"Erro na API: {response.status_code}")

dados_brutos = response.json()
dados_filtrados = []

for item in dados_brutos.get("data", []):
    if "PSI" in item.get("name", ""):
        dados_filtrados.append({
            "indice": item.get("name"),
            "cotacao": item.get("price"),
            "variacao": item.get("change"),
            "percentual": item.get("change_percent"),
            "hora": item.get("time")
        })

with open("data/psi.json", "w", encoding="utf-8") as f:
    json.dump(dados_filtrados, f, ensure_ascii=False, indent=2)
