import os, time, datetime
from playwright.sync_api import sync_playwright
from flows.fluxo_conexao import enviar_convite, verifica_status 
from flows.fluxo_mensagem import enviar_mensagem
from utils.config import sheet
import sys

def resource_path(relative_path):
        
    if getattr(sys, 'frozen', False):  # se for .exe
        base_path = sys._MEIPASS
    else:  # se rodar no Python normal
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)    

def main():
    modo = input("Digite '1' para conexões e '2' para mensagens: ").strip()
    data_inicial = None

    if modo == "2":
        data_inicial = input("Digite a data inicial (dd/mm/aa): ").strip()
        
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

    # parte do sheets
        links = sheet.col_values(8)  # coluna H
        datas = sheet.col_values(9)  # coluna I
        mensagens = sheet.col_values(10) # colouna J

        hoje = datetime.date.today().strftime("%d/%m/%Y")

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

            if modo == "1":
                status = enviar_convite(page, link)  # agora retorna "enviado", "pendente" ou "erro"

                if status in ["enviado", "pendente"]:
                    sheet.update_cell(l, 9, hoje)  # registra a data mesmo se estiver pendente
                    print(f"Linha {l} marcada como '{status}' com a data {hoje}")
                else:
                    sheet.update_cell(l, 9, "Erro")
                    print(f"Linha {l} não foi possível conectar, marcada como 'Erro'")

            elif modo == "2":
                mensagem_base = (
                    "Olá {{nome}}!\n\n"
                    "Agradeço por sua conexão.\n\n"
                    "Em um cenário repleto de alternativas para resolver problemas, como escolher a solução certa?\n\n"
                    "Na GBPA, nosso DNA é entender o seu Business Case e implementar soluções sob medida, "
                    "com o apoio do nosso time e parceiros. De Automação de Processos a IA Generativa, "
                    "transformamos desafios em oportunidades!\n\n"
                    "Sua jornada com IA começa aqui.\n\n"
                    "Visite nossa página: https://www.linkedin.com/company/grupogbpa/posts/?feedView=all\n\n"
                    "Conheça os Cases!"
                    )
                status_msg = enviar_mensagem(page, link, mensagem_base)
                
                if status_msg == "enviado":
                    sheet.update_cell(l, 10, hoje)
                    print(f"Mensagem enviada para {link} em {hoje}")
                else:
                    print(f"Não foi pssível enviar mensagem para {link}")
                
            time.sleep(3)

        drive.close()

if __name__ == "__main__":
    main()