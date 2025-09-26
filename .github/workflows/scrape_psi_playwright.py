import asyncio
from playwright.async_api import async_playwright
import json

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.jornaldenegocios.pt/cotacoes/indice/PSI")
        await page.wait_for_selector(".table-responsive tr")

        html = await page.content()
        await browser.close()

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        linhas = soup.select(".table-responsive tr")
        dados = []

        for i, linha in enumerate(linhas):
            if i == 0: continue
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

asyncio.run(main())
