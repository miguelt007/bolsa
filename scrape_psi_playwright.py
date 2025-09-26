import asyncio
from playwright.async_api import async_playwright
import json
from bs4 import BeautifulSoup

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.jornaldenegocios.pt/cotacoes/indice/PSI")

        # Aceitar cookies se aparecer
        try:
            await page.click("button:has-text('Aceitar')", timeout=3000)
        except:
            pass  # Ignora se não existir

        # Simula scroll para forçar carregamento
        await page.mouse.wheel(0, 1000)
        await page.wait_for_timeout(6000)

        html = await page.content()
        await browser.close()

        soup = BeautifulSoup(html, "html.parser")
        linhas = soup.select(".table-responsive tr")
        dados = []

        for i, linha in enumerate(linhas):
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
