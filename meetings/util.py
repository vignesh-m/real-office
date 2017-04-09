import smtplib
from email.mime.text import MIMEText


def send_mail(recepients, messages):
    # send mail from realoffice ID
    fro = 'realoffice.iitm@gmail.com'
    fro_pass = 'IITMCSE2014'

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fro, fro_pass)

    for to, msg in zip(recepients, messages):
        msg = MIMEText(msg)
        msg['From'] = fro
        msg['To'] = to

        server.sendmail(fro, [to], msg.as_string())

# send_mail(['premkrishnaa1996@gmail.com '], ['hi prem'])
