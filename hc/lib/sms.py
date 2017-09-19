from twilio.rest import Client
import os
import random

client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))


def send_sms(to, body):
    return client.messages.create(
        to=to,
        from_=os.getenv('TWILIO_NUMBER'),
        body=body)


def send_confirmation_code(to_number):
    verification_code = generate_code()
    send_sms(to_number, verification_code)
    return verification_code


def generate_code():
    return str(random.randrange(100000, 999999))


def alert(to_number, ctx):
    if ctx['check'].name:
        body = "Check %s with code %s has gone %s" % (ctx['check'].name, ctx['check'].code, ctx['check'].status)
    else:
        body = "Check with code %s has gone %s" %(ctx['check'].code, ctx['check'].status)
    return send_sms(to_number, body)