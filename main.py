import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def send_mail(msg, receiver):

    date = datetime.now()
    sender = "shahinhoushidari@gmail.com"
    receivers = ["cebhanhoushidari@gmail.com"]

    message = MIMEMultipart()

    message["Subject"] = f'Timetable for week beginning {date.day}/{date.month}/{date.year}'

    title = '<b> Title line here. </b>'
    messageText = MIMEText(f'{msg}','html')
    message.attach(messageText)

    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    s.login("studystack.shahin@gmail.com", "uwmj crqg cllp apsk")

    s.sendmail("studystack.shahin@gmail.com", receiver, message.as_string())

    s.quit()
