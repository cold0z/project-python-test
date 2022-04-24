from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from api.constants import KEY_SENDGRID

def mailSendGrid(code,email):
    content = "<h3>You're on your way! Let's confirm your email address.</h3><h4>Verification Code : <span style='color:#00d5f6'><b>"+code+"</b></span></h4>"
    content += '<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Dailymotion_logo_%282015%29.svg/1772px-Dailymotion_logo_%282015%29.svg.png" width="150">'
    sendgrid = SendGridAPIClient(KEY_SENDGRID)
    message = Mail(
        from_email='haddou.jihad@weberfly-group.com',
        to_emails=email,
        subject='Welcome to Dailymotion! Confirm Your Email',
        html_content = content)
    try:
        response = sendgrid.send(message)
        if response.status_code == 202 :
            return True
        return False
    except Exception as error:
        print(error)
        return False
        