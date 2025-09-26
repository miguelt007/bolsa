import requests
from bs4 import BeautifulSoup
import json

proxy_url = "https://api.codetabs.com/v1/proxy?quest=https://www.jornaldenegocios.pt/cotacoes/indice/PSI"
html = requests.get(proxy_url, headers={"User-Agent": "Mozilla/5.0"}).text
soup = BeautifulSoup(html, "html.parser")

linhas = soup.select(".table-responsive tr")
dados = []

for i, linha in enumerate(linhas):
    if i == 0: continue  # Ignora cabeçalho
    cols = linha.find_all("td")
    if len(cols) >= 6:
        dados.append({
            "empresa": cols[0].text.strip(),
            "cotacao": cols[1].text.strip(),
            "variacao": cols[2].text.strip(),
            "volume": cols[3].text.strip(),
            "capitalizacao": cols[4].text.strip(),
            "hora": cols[5].text.strip()
        })

with open("data/psi.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print(f"✅ {len(dados)} empresas extraídas com sucesso.")
