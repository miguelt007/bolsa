import requests
import re
import json

url = "https://www.jornaldenegocios.pt/cotacoes/indice/PSI"
headers = { "User-Agent": "Mozilla/5.0" }
html = requests.get(url, headers=headers).text

# Regex ajustado para capturar nome, cotação, variação, volume, capitalização e hora
padrao = re.compile(
    r'([A-ZÀ-Úa-zà-ú\\s\\-]+?)\\s+([\\d,]+)€\\s+([\\-\\+\\d,]+%)\\s+([\\d\\.]+)\\s+([\\d\\.]+m€)\\s+(\\d{2}:\\d{2})'
)

matches = padrao.findall(html)

dados = []
for m in matches:
    empresa, cotacao, variacao, volume, capitalizacao, hora = m
    dados.append({
        "empresa": empresa.strip(),
        "cotacao": cotacao.replace(",", ".") + "€",
        "variacao": variacao,
        "volume": volume,
        "capitalizacao": capitalizacao,
        "hora": hora
    })

with open("data/psi.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print(f"✅ {len(dados)} empresas extraídas com sucesso.")
