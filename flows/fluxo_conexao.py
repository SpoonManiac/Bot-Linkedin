import re
import logging

def enviar_convite(page, link):
    page.goto(link, timeout=60000)
    page.wait_for_timeout(5000)

    try:
        page.wait_for_selector('button', timeout=15000)

        nome_elemento = page.locator("h1").first
        nome = re.sub(r'\(.*?\)', '',nome_elemento.inner_text()).strip()
        aria_label = f"Convidar {nome} para se conectar"

        print(f"DEBUG - Nome extraído: '{nome}'")
        print(f"DEBUG - aria-label montado: '{aria_label}'")

        
        botao_conectar = page.locator(f'button:has-text("Conectar")').first
        if botao_conectar.is_visible():
            botao_conectar.click()
            logging.info(" Clicou no botão 'Conectar'")
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
            logging.info(" Clicou no botão 'Mais'")
            page.wait_for_timeout(2500) #2.5s

            botao_conectar_menu = page.get_by_role("button", name=aria_label).first
            if botao_conectar_menu.is_visible():
                botao_conectar_menu.click()
                logging.info(" Clicou no botão 'Conectar' (menu)")
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
        print(f"Erro em {link}: {e}")
    return False

def verifica_status(page,link):
    page.wait_for_selector('body', timeout=10000)

    try:
        if "Esta página não existe" in page.content():
            return "não_existe"
        
    except Exception as e:
        logging.error(" Erro ao verificar {link}: {e}")
        return "ok"