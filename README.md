# Bot-Linkedin ¯_(ツ)_/¯

![Python](https://img.shields.io/badge/Python-3.13%2B-orange)
![GitHub issues](https://img.shields.io/github/issues/SpoonManiac/Bot-Linkedin)
=======
![GitHub closed issues](https://img.shields.io/github/issues-closed/SpoonManiac/Bot-Linkedin?&color=yellow)
>>>>>>> edddd84ad47124e0b107a4286afcdb839e4b6bb7

Um bot criado para auxiliar no processo de conectar-se com usuários no **LinkedIn**, utilizando **Python**, **Playwright** e **Google Spreadsheet** como banco de dados.

---

## 🚀 Funcionalidades

* Automatiza o envio de solicitações de conexão no LinkedIn a partir de uma lista de alvos
* Automatiza o envio de mensagens privadas no LinkedIn a partir da data de conexão
* Gerencia os alvos e status das interações via Google Spreadsheet
* Log e histórico de operações para monitoramento

---

## 🛠 Arquitetura / Tecnologias usadas

* **Python** — linguagem principal
* **Playwright** — automatização do navegador / interação com a interface do LinkedIn
* **Google Sheets API** — para usar uma planilha como banco de dados
* (Possíveis módulos internos utilitários para manipulação de dados, logs, controle de fluxo, etc.)

---

## 📦 Pré-requisitos

Antes de executar o bot, você precisará:

* Ter **Python 3.13+** (ou versão compatível) instalado
* Instalar dependências (veja seção [Como usar / configurar](#como-usar---configurar))
* Credenciais de acesso à **Google Sheets API** (arquivo JSON)
* Uma planilha no Google Sheets configurada com as colunas que o bot espera (ex: `Empresa`, `Contato`, `Primeiro nome`, `Segmento`, `E-mail`, `Cargo`, `Telefone`, `Linkedin`, `Data solicitação`, etc.)
* Conta no LinkedIn (atenção às políticas da plataforma)

---

## ⚙️ Como usar / configurar

1. **Clone este repositório:**

```bash
git clone https://github.com/SpoonManiac/Bot-Linkedin.git
cd Bot-Linkedin
```

2. **Crie um ambiente virtual (opcional, mas recomendado):**

```bash
python -m venv venv
source venv/bin/activate  # no Linux/macOS
.\venv\Scripts\activate   # no Windows
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Configure as credenciais do Google:**

* Siga as instruções da [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python) para gerar credenciais (arquivo JSON).
* Ajuste o código para apontar para esse arquivo de credenciais.
* Compartilhe sua planilha com o e-mail da credencial gerada.

5. **Prepare a planilha de alvos:**

* Crie as colunas esperadas pelo bot (`Empresa`, `Contato`, `Primeiro nome`, `Segmento`, `E-mail`, `Cargo`, `Telefone`, `Linkedin`, `Data solicitação`, etc.).
* Certifique-se de que os cabeçalhos e estrutura estejam compatíveis com o esperado pelo código.

6. **Execute o bot:**

```bash
run.bat
# ou
python main.py
```

---

## 📂 Estrutura do projeto

```
.
├── flows/               # Fluxos de automação
├── requirements/        # Dependências
├── utils/               # Funções utilitárias
├── main.py              # Script principal
├── run.bat              # Script para Windows
└── requirements.txt     # Dependências do projeto
```

---

## 🤝 Contribuição

* Abra *issues* para sugerir melhorias ou reportar bugs.
* Envie *pull requests* com novas funcionalidades, correções ou refinamentos.
* Ajude na documentação e exemplos de uso.

---

## ⚠️ Avisos / Considerações legais

* O uso de bots automatizados em redes sociais pode violar os **Termos de Serviço** dessas plataformas.
* Use com cautela e responsabilidade.
* Não me responsabilizo por bloqueios, suspensões ou penalidades advindas do uso deste bot.
* Utilize limites razoáveis, delays e estratégias de “comportamento humano” para minimizar riscos.
