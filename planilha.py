import gspread
from oauth2client.service_account import ServiceAccountCredentials
from playwright.sync_api import sync_playwright
import re
import datetime
import time
import os
import sys

def resource_path(relative_path):
    
    if getattr(sys, 'frozen', False):  # se for .exe
        base_path = sys._MEIPASS
    else:  # se rodar no Python normal
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = creds = ServiceAccountCredentials.from_json_keyfile_name("automacaolinkedin-471017-5052e7cd33ea.json", scope)

client = gspread.authorize(creds)

spreadsheet_url = "https://docs.google.com/spreadsheets/d/1aJ-JsXpFGllgDGdGODmnVIh_jT9oRUAuAahmqHn0tN8/edit?gid=1515599369#gid=1515599369"
#spreadsheet_url = input("Insira o Link da planilha do Google: ").strip()
sheet = client.open_by_url(spreadsheet_url).sheet1


def enviar_convite(page, url):
    page.goto(url, timeout=60000)
    page.wait_for_timeout(5000)

    try:
        page.wait_for_selector('button', timeout=15000)

        nome_elemento = page.locator("h1").first
        nome = re.sub(r'\(.*?\)', '',nome_elemento.inner_text()).strip()
        aria_label = f"Convidar {nome} para se conectar"

        print(f"[DEBUG] Nome extraído: '{nome}'")
        print(f"[DEBUG] aria-label montado: '{aria_label}'")

        
        botao_conectar = page.locator(f'button:has-text("Conectar")').first
        if botao_conectar.is_visible():
            botao_conectar.click()
            print("Clicou no botão 'Conectar'")
            page.wait_for_timeout(2000)
            if page.locator('button[aria-label="Enviar sem nota"]').is_visible():
                page.wait_for_selector('button[aria-label="Enviar sem nota"]', timeout=5000)
                page.locator('button[aria-label="Enviar sem nota"]').click()
                page.wait_for_timeout(3000)
                return "enviado"
            else:
                pendente = page.locator('button:has-text("Conectar")').first
                if not pendente.is_visible():
                    return "pendente"

        
    

        botao_mais = page.get_by_role("button", name="Mais").first
        if botao_mais.is_visible():
            botao_mais.click()
            print("Clicou no botão 'Mais'")
            page.wait_for_timeout(2500) #2.5s

            botao_conectar_menu = page.get_by_role("button", name=aria_label).first
            if botao_conectar_menu.is_visible():
                botao_conectar_menu.click()
                print("Clicou no botão 'Conectar' (menu)")
                page.wait_for_timeout(2000)
                if page.locator('button[aria-label="Enviar sem nota"]').is_visible():
                    page.wait_for_selector('button[aria-label="Enviar sem nota"]', timeout=5000)
                    page.locator('button[aria-label="Enviar sem nota"]').click()
                    page.wait_for_timeout(3000)
                    return "enviado"
                else:
                    return "pendente"
                
            return "pendente"

    except Exception as e:
        print(f"Erro em {url}: {e}")
    return False

def verifica_status(page,url):
    page.goto(url,timeout=60000)
    page.wait_for_selector('body', timeout=10000)

    try:
        if "Esta página não existe" in page.content():
            return "não_existe"
        
    except Exception as e:
        print(f"Erro ao verificar {url}: {e}")
        return "ok"


# --- Automação principal ---
with sync_playwright() as pw:
    drive = pw.chromium.launch(headless=False, slow_mo=200)  # headless=True (Padrão) tem o efeito de executar a automação sem o browser estar visível

    # verifica se existe sessão salva
    if os.path.exists("linkedin_state.json"):
        context = drive.new_context(storage_state="linkedin_state.json")
    else:
        context = drive.new_context()

    page = context.new_page()

    #login manual do linkedin pela primeira vez
    if not os.path.exists("linkedin_state.json"):
        page.goto("https://www.linkedin.com/login")
        print("Faça login manual no LinkedIn e depois pressione ENTER aqui...")
        input()
        context.storage_state(path="linkedin_state.json")  # salva sessão

    links = sheet.col_values(8)  # coluna H
    datas = sheet.col_values(9)  # coluna I

    for l, link in enumerate(links[1:], start=2):  # pula cabeçalho
        if not link:
            continue

        #pegando status atual da coluna i, de tem erro reprocessa, senão pula
        status = datas[l-1] if l < len(datas) else ""
        if status and status.lower()!= "erro":
            print(f"Linha {l} ja processada ({status}), pulando...")
            continue

        perfil_status = verifica_status(page, link)
        if perfil_status == "não_existe":
            sheet.update_cell(l,9,"Não existe")
            print(f"Linha {l} marcada como 'Não existe'")
            time.sleep(5)
            continue

        print(f"Processando {link}...")
        status = enviar_convite(page, link)  # agora retorna "enviado", "pendente" ou "erro"
        hoje = datetime.date.today().strftime("%d/%m/%Y")

        if status in ["enviado", "pendente"]:
            sheet.update_cell(l, 9, hoje)  # registra a data mesmo se estiver pendente
            print(f"Linha {l} marcada como '{status}' com a data {hoje}")
        else:
            sheet.update_cell(l, 9, "Erro")
            print(f"Linha {l} não foi possível conectar, marcada como 'Erro'")

        time.sleep(3)

    drive.close()
