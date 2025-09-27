import os, time, datetime
from playwright.sync_api import sync_playwright
from flows.fluxo_conexao import enviar_convite, verifica_status 
from flows.fluxo_mensagem import enviar_mensagem
from utils.config import sheet_Leads, minha_rede
import sys
import logging

logging.basicConfig(
    level=logging.DEBUG,  # define o nível de logs que será mostrado
    format="%(levelname)s -%(message)s",  # formato do log
)

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
        data_inicial = input("Digite a data inicial (dd/mm/aaaa): ").strip()
        data_inicial = datetime.datetime.strptime(data_inicial, "%d/%m/%Y").date()

        
    with sync_playwright() as pw:
        drive = pw.chromium.launch(headless=False, args=["--start-maximized"], slow_mo=200)  # headless=True (Padrão) tem o efeito de executar a automação sem o browser estar visível

        # verifica se existe sessão salva
        if os.path.exists("linkedin_state.json"):
            context = drive.new_context(storage_state="linkedin_state.json", viewport= None)
            
        else:
            context = drive.new_context(viewport= None)
            

        page = context.new_page()
        page.evaluate("() => window.moveTo(0,0); window.resizeTo(screen.width, screen.height);")


        #login manual do linkedin pela primeira vez
        if not os.path.exists("linkedin_state.json"):
            page.goto("https://www.linkedin.com/login")
            print("Faça login manual no LinkedIn e depois pressione ENTER aqui...")
            input()
            context.storage_state(path="linkedin_state.json")  # salva sessão

        if modo == "1":
        # parte do sheets
            links = sheet_Leads.col_values(8)  # coluna H
            datas = sheet_Leads.col_values(9)  # coluna I

            hoje = datetime.date.today().strftime("%d/%m/%Y")

            for l, link in enumerate(links[1:], start=2):  # pula cabeçalho
                if not link:
                    continue

                #pegando status atual da coluna i, de tem erro reprocessa, senão pula
                status = datas[l-1] if l < len(datas) else ""
                if status and status.lower()!= "erro":
                    logging.info(f" Linha {l} ja processada ({status}), pulando...")
                    continue

                perfil_status = verifica_status(page, link)
                if perfil_status == "não_existe":
                    sheet_Leads.update_cell(l,9,"Não existe")
                    logging.info(f" Linha {l} marcada como 'Não existe'")
                    time.sleep(5)
                    continue

                logging.info(f" Processando {link}...")

            
                status = enviar_convite(page, link)  # agora retorna "enviado", "pendente" ou "erro"

                if status in ["enviado", "pendente"]:
                    sheet_Leads.update_cell(l, 9, hoje)  # registra a data mesmo se estiver pendente
                    logging.info(f" Linha {l} marcada como '{status}' com a data {hoje}")
                else:
                    sheet_Leads.update_cell(l, 9, "Erro")
                    logging.info(f" Linha {l} não foi possível conectar, marcada como 'Erro'")

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

            status_msg, enviados = enviar_mensagem(page, minha_rede, mensagem_base, data_inicial)
                
            if status_msg == "enviado":
                logging.info(f" Mensagens enviadas com sucesso em {datetime.date.today().strftime('%d/%m/%Y')}")
            elif status_msg == "nenhum":
                logging.info(" Nenhuma mensagem foi enviada (nenhuma conexão dentro da data informada).")
            else:
                logging.error(" Ocorreu um erro ao tentar enviar mensagens.")
                
                        
        time.sleep(3)
        drive.close()

if __name__ == "__main__":
    main()