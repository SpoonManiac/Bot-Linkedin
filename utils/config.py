import gspread
from google.oauth2.service_account import Credentials

scope = ["https://spreadsheets.google.com/feeds",
          "https://www.googleapis.com/auth/drive"]


creds_file = "automacaolinkedin-471017-5052e7cd33ea.json"
creds = Credentials.from_service_account_file(creds_file, scopes=scope)
client = gspread.authorize(creds)



minha_rede = 'https://www.linkedin.com/mynetwork/invite-connect/connections/'
spreadsheet_url = "https://docs.google.com/spreadsheets/d/1aJ-JsXpFGllgDGdGODmnVIh_jT9oRUAuAahmqHn0tN8/edit?gid=1515599369#gid=1515599369"
#spreadsheet_url = input("Insira o Link da planilha do Google: ").strip()
sheet = client.open_by_url(spreadsheet_url)
sheet_Leads = sheet.worksheet("Leads")
try:

    sheet_Envio_Mensagens = sheet.worksheet("Envio de Mensagens")
except gspread.exceptions.WorksheetNotFound:
    sheet_Envio_Mensagens = sheet.add_worksheet(title="Envio de Mensagens", rows="100", cols="20")
    print("Worksheet 'Envio de Mensagens' criada pois não existia.")
    cabecalho = ["EMPRESA", "CONTATO", "NOME", "SEGMENTO", "EMAIL", "CARGO", "TELEFONE", "LINKEDIN", "DATA MENSAGEM"]
    sheet_Envio_Mensagens.append_row(cabecalho)