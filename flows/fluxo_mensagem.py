import datetime
import re
from utils.config import sheet, minha_rede



def conexao_feita_em(texto):
    meses = {
        "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4, "maio": 5,
        "junho": 6, "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10,
        "novembro": 11, "dezembro": 12
    }
    # Exemplo texto: "Conexão feita em 12 de março de 2024"
    match = re.search(r"(\d{1,2}) de (\w+) de (\d{4})", texto.lower())
    if match:
        dia, mes, ano = match.groups()
        numero_mes= meses.get(mes, 0)
        return datetime.date(int(ano), numero_mes, int(dia))
    return None


def enviar_mensagem(page, minha_rede, mensagem_base, data_inicial):
    enviados = []
    try:
        page.goto(minha_rede, timeout=60000)
        page.wait_for_timeout(5000)

        conexoes = page.locator("div.entity-result__item")
        total = conexoes.count()

        for i in range(total):
            bloco = conexoes.nth(i)
            texto_data = bloco.inner_text()
            print("entrou loop i")

            if "Conexão feita em" in texto_data:
                data_conexao = data_conexao(texto_data)
                print("Viu se tem 'Conexão feita em'")

                if data_conexao and data_conexao >= data_inicial:
                    nome = bloco.locator("span.entity-result__title-text").inner_text().strip()
                    print(f"[OK] {nome} - {data_conexao.strftime('%d/%m/%Y')}")

                    if bloco.locator("button:has-text('Mensagem')").is_visible():
                        bloco.locator("button:has-text('Mensagem')").click()
                        page.wait_for_timeout(2000)

                        textarea = page.locator("div[role='textbox']").first
                        textarea.fill(mensagem_base.replace("{{nome}}", nome))
                        page.keyboard.press("Enter")
                        print(f"Mensagem enviada para {nome}")

                        enviados.append({
                            "nome": nome,
                            "data_envio": datetime.date.today().strftime("%d/%m/%Y")
                        })
                        page.wait_for_timeout(2000)

        # atualiza a planilha
        for item in enviados:
            nome = item["nome"]
            data_envio = item["data_envio"]
            try:
                cell = sheet.find(nome)
                if cell:
                    sheet.update_cell(cell.row, 10, data_envio)  # coluna J (10ª)
                    print(f"Atualizado planilha: {nome} na linha {cell.row} com data {data_envio}")
                else:
                    print(f"⚠ Nome {nome} não encontrado na planilha")
            except Exception as e:
                print(f"Erro ao atualizar {nome} na planilha: {e}")

        return "enviado" if enviados else "nenhum"

    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
        return "erro"
