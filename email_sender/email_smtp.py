import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import re


class EmailSender:

    def __init__(self, email):
        self.email = email

    def email_usuario(self):
        padrao = re.search(
            r'[a-zA-Z0-9_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{1,3}$', self.email)
        if padrao:
            print('email Valido')

        else:
            print('Digite um email valido!!!')

    def send_email(self):
        endereco_remetente = 'senDERemai2@outlook.com'
        senha_remetente = "Sua senha"

        msg = MIMEMultipart()
        msg['From'] = endereco_remetente
        msg['To'] = self.email
        msg['Subject'] = 'Email com Anexo'

        corpo_email = "Olá, este é um email com um arquivo Excel anexado."
        msg.attach(MIMEText(corpo_email, 'plain'))
        arquivo_excel = 'twitter_scrap.xlsx'
        with open(arquivo_excel, 'rb') as file:
            anexo = MIMEApplication(file.read(), Name='exemplo_pandas_excel.xlsx')
        anexo['Content-Disposition'] = f'attachment; filename="{arquivo_excel}"'
        msg.attach(anexo)
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(endereco_remetente, senha_remetente)
        server.sendmail(endereco_remetente, self.email, msg.as_string())
        server.quit()
