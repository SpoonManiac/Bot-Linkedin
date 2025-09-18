import re
import time




def enviar_mensagem(page, link, mensagem):
    
    try:
        page.goto(link, timeout=60000)
        page.wait_for_timeout(3000)

        nome_elemento = page.locator("h1").first
        nome = re.sub(r'\(.*?\)', '', nome_elemento.inner_text()).strip()

        msg_final = mensagem.replace("{{nome}}", nome)

        #procura botao
        botao_msg= page.get_by_role("button", name="Mensagem").first
        if botao_msg.is_visible():
            botao_msg.click()
            page.wait_for_timeout(2000)

            #caixa de txt
            caixa_texto = page.locator("div.msg-form__contenteditable")
            if caixa_texto.is_visible():
                caixa_texto.fill("")
                caixa_texto.type(msg_final)
                page.wait_for_timeout(2000)

                botao_enviar = page.get_by_role("button", name="Enviar").first
                if botao_enviar.is_visible():
                    botao_enviar.click()
                    print(f"Mensagem enviada com sucesso para {nome}!")
                    page.wait_for_timeout(2000)
                    return "enviado"
                
        return "nao_enviado"

    except Exception as e:
        print(f"Erro ao enviar mensagem paralink{link}: {e}")
        return "erro"