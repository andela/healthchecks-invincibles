from twilio.rest import Client
import os
account_sid=os.getenv('TWILIO_ACCOUNT_SID')
auth_token=os.getenv('TWILIO_AUTH_TOKEN')
twilio_number=os.getenv('TWILIO_NUMBER')

client = Client(account_sid, auth_token)


def send_sms(to, body):
    client.messages.create(
        to=to,
        from_=twilio_number,
        body=body)


def alert(to_number, ctx):
    if ctx['check'].name:
        body = "Check %s with code %s has gone %s" % (ctx['check'].name, ctx['check'].code, ctx['check'].status)
    else:
        body = "Check with code %s has gone %s" %(ctx['check'].code, ctx['check'].status)
    send_sms(to_number, body)
