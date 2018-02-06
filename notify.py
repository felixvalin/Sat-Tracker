from twilio.rest import Client
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, text, toaddr):
    fromaddr = "felixantoinevalin@gmail.com"
    pswd = "555987xilef"
    # toaddr = "felixantoinevalin@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject

    body = text
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, pswd)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    return


def send_simple_email(text, toaddr):
    fromaddr = "felixantoinevalin@gmail.com"
    pswd = "555987xilef"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, pswd)

    msg = text
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()


def send_fake_sms(text):
    print("The Satellite is Visible")


def send_sms(text):

    # Twilio account settings
    account = "ACdbaec810c92fa59c1581b5f4998cb58a"
    token = "634aaec0b3d9ce81811b33f77f296873"
    client = Client(account, token)

    twilio_phone = "+14387956089"
    felix_phone = "+14388283973"

    message = client.messages.create(to=felix_phone, from_=twilio_phone, body=text)
    return message


# sat_name = "The Humanity Star"
# send_email(sat_name, sat_name+" is no longer visible!", "felixantoinevalin@gmail.com")
