import datetime
import re
from utils.config import sheet_Envio_Mensagens, minha_rede

def conexao_feita_em(texto):
    meses = {
        "janeiro": 1, "fevereiro": 2, "março": 3, "mar": 3,
        "abril": 4, "mai": 5, "maio": 5,
        "junho": 6, "jul": 7, "julho": 7,
        "agosto": 8, "ago": 8,
        "setembro": 9, "set": 9, "set.": 9,
        "outubro": 10, "out": 10,
        "novembro": 11, "nov": 11,
        "dezembro": 12, "dez": 12, "dez.": 12
    }
    texto = texto.lower()
    match = re.search(r"conexão feita em (\d{1,2}) de (\w+)\.? de (\d{4})", texto)
    if match:
        dia, mes, ano = match.groups()
        numero_mes = meses.get(mes, 0)
        if numero_mes:
            return datetime.date(int(ano), numero_mes, int(dia))
    return None


def enviar_mensagem(page, minha_rede, mensagem_base, data_inicial):
    enviados = []

    try:
        page.goto(minha_rede, timeout=60000)
        page.wait_for_timeout(3000)

        # --- SCROLL AUTOMÁTICO PARA CARREGAR TODAS AS CONEXÕES ---
        prev_height = 0
        while True:
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            page.wait_for_timeout(2000)
            curr_height = page.evaluate("document.body.scrollHeight")
            if curr_height == prev_height:
                break
            prev_height = curr_height

        page.wait_for_selector('div[data-view-name="connections-list"] > div', timeout=10000)
        blocos = page.locator('div[data-view-name="connections-list"] > div').all()

        blocos_validos = []
        for bloco in blocos:
            texto_bloco = bloco.inner_text()
            data_conexao = conexao_feita_em(texto_bloco)
            if data_conexao and data_conexao >= data_inicial:
                blocos_validos.append((bloco, data_conexao))

        if not blocos_validos:
            print("Nenhuma mensagem foi enviada (nenhuma conexão dentro da data informada).")
            return "nenhum", []

        for bloco, data_conexao in blocos_validos:
            
            nome_elem = bloco.locator('a[href*="/in/"]').first
            nome = nome_elem.inner_text().strip()
            link = nome_elem.get_attribute("href")
            print(nome)
            print(f"{nome} - Conectados desde -> {data_conexao.strftime('%d/%m/%Y')}")

            botao_mensagem = bloco.locator("span:has-text('Mensagem')").first
            if botao_mensagem.is_visible():
                botao_mensagem.click()
                page.wait_for_timeout(1000)

                textarea = page.locator("div[role='textbox']").first
                print("Encontrou a caixa de texto para o envio da mensagem")
                textarea.fill(mensagem_base.replace("{{nome}}", nome))
                #botao_enviar = page.locator("button[class='msg-form_send-button']")
                #print("Encontrou o botão 'Enviar' ")
                #botao_enviar.click()
                print(f"Mensagem enviada para {nome}")

                # aqui adiciona na lista de enviados
                data_envio = datetime.date.today().strftime("%d/%m/%Y")
                enviados.append({
                    "nome": nome,
                    "data_envio": data_envio
                })

                # adiciona na planilha
                try:
                   
                    celulas = sheet_Envio_Mensagens.findall(nome)
                    if not celulas:
                        linha = ["", "", nome, "", "", "", "", link, data_envio]
                        sheet_Envio_Mensagens.append_row(linha)
                        print(f"Adicionado na planilha: {nome} | {data_envio}")
                    else:
                        print(f"{nome} já existe na planilha, pulando...")
                        
                except Exception as e:
                    print(f"Erro ao adicionar {nome} na planilha: {e}")

                    page.wait_for_timeout(1000)

        return "enviado", enviados

    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        return "erro", []
