from twilio.rest import Client

account = "ACdbaec810c92fa59c1581b5f4998cb58a"
token = "634aaec0b3d9ce81811b33f77f296873"
client = Client(account, token)

twilio_phone = "+14387956089"
felix_phone = "+14388283973"


def send_sms(text):
    message = client.messages.create(to=felix_phone, from_=twilio_phone, body=text)
    return message
