import smtplib
from email.mime.text import MIMEText


def send_mail(recepients, messages, subject):
    # send mail from realoffice ID
    fro = 'realoffice.iitm@gmail.com'
    fro_pass = 'IITMCSE2014'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fro, fro_pass)

    for to in (recepients):
        msg = MIMEText(messages)
        msg['From'] = fro
        msg['To'] = to
        msg['Subject'] = subject

        server.sendmail(fro, [to], msg.as_string())

# send_mail(['premkrishnaa1996@gmail.com '], ['hi prem'])
