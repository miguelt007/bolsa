import requests
from bs4 import BeautifulSoup
import json

url = "https://www.investing.com/indices/psi-20-components"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "pt-PT,pt;q=0.9"
}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

linhas = soup.select("table tbody tr")
dados = []

for linha in linhas:
    cols = linha.find_all("td")
    if len(cols) >= 9:
        dados.append({
            "empresa": cols[1].text.strip(),
            "cotacao": cols[2].text.strip(),
            "variacao_abs": cols[3].text.strip(),
            "variacao_pct": cols[4].text.strip(),
            "maximo": cols[5].text.strip(),
            "minimo": cols[6].text.strip(),
            "volume": cols[7].text.strip(),
            "hora": cols[8].text.strip()
        })

with open("data/psi.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print(f"✅ {len(dados)} empresas extraídas com sucesso.")
