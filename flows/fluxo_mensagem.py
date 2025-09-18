import re
import time
from utils.config import minha_rede

def data_conexao(texto):

    meses = {
        "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4, "maio": 5,
        "junho": 6, "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10,
        "novembro": 11, "dezembro": 12
    }

def enviar_mensagem(page, minha_rede, mensagem_base, data_inicial):
    
    try:
        page.goto(minha_rede, timeout=60000)
        page.wait_for_timeout(3000)
        connectionsList = page.locator(f"div:[componentkey='ConnectionsPage_ConnectionsList'")
        
        for bloco in connectionsList:
            if page.locator("div").filter(has_text="Conexão feita em {data_inicial}"):
                ...

        
        # nome_elemento = page.locator("h1").first
        # nome = re.sub(r'\(.*?\)', '', nome_elemento.inner_text()).strip()

        # msg_final = mensagem.replace("{{nome}}", nome)

        # #procura botao
        # botao_msg= page.get_by_role("button", name="Mensagem").first
        # if botao_msg.is_visible():
        #     botao_msg.click()
        #     page.wait_for_timeout(2000)

        #     #caixa de txt
        #     caixa_texto = page.locator("div.msg-form__contenteditable")
        #     if caixa_texto.is_visible():
        #         caixa_texto.fill("")
        #         caixa_texto.type(msg_final)
        #         page.wait_for_timeout(2000)

        #         botao_enviar = page.get_by_role("button", name="Enviar").first
        #         if botao_enviar.is_visible():
        #             botao_enviar.click()
        #             print(f"Mensagem enviada com sucesso para {nome}!")
        #             page.wait_for_timeout(2000)
        #             return "enviado"
                
        # return "nao_enviado"

    except Exception as e:
        # print(f"Erro ao enviar mensagem para link{link}: {e}")
        # return "erro"
        ...