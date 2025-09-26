import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent": "Mozilla/5.0"
}
url = "https://pt.investing.com/indices/psi-20-components"
html = requests.get(url, headers=headers).text
soup = BeautifulSoup(html, "html.parser")

tabela = soup.find("table", {"id": "cr1"})
linhas = tabela.find("tbody").find_all("tr")

dados = []
for linha in linhas:
    cols = linha.find_all("td")
    if len(cols) >= 7:
        dados.append({
            "empresa": cols[1].text.strip(),
            "cotacao": cols[2].text.strip(),
            "variacao": cols[3].text.strip(),
            "maximo": cols[4].text.strip(),
            "minimo": cols[5].text.strip(),
            "volume": cols[6].text.strip()
        })

with open("data/psi.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)
