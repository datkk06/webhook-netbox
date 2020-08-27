from flask import Flask, request, abort
import requests
import config

from flask_mail import Mail, Message

app = Flask(__name__)
mail_settings = {
    "MAIL_SERVER": config.EMAIL_HOST,
    "MAIL_PORT": config.EMAIL_PORT,
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": config.EMAIL_HOST_USER,
    "MAIL_PASSWORD": config.EMAIL_HOST_PASSWORD
}
app.config.update(mail_settings)

mail = Mail(app)


@app.route('/webhook/<path>', methods=['POST'])
def webhook(path):
    try:
        if request.method == 'POST':
            print(request.json)

            if config.TELEGRAM_TOKEN != "" and config.TELEGRAM_CHAT_ID != "":
                telegram_bot_sendtext(message=request.json.get('data'))
            if config.SLACK_TOKEN != "" and config.SLACK_CHANNEL != "":
                slack_bot_sendtext(message=request.json.get('data'))
            if config.EMAIL_HOST != "" and config.EMAIL_HOST_USER != "" and config.EMAIL_HOST_PASSWORD != "":
                send_email(message=request.json.get('data'))
            return path, 200
        else:
            abort(400)
    except:
        abort(400)

def telegram_bot_sendtext(message):

    bot_token = config.TELEGRAM_TOKEN
    bot_chatID = config.TELEGRAM_CHAT_ID
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message

    response = requests.get(send_text)

    return response.json()

def slack_bot_sendtext(message):
    slack_token = config.SLACK_TOKEN
    slack_channel = config.SLACK_CHANNEL
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack_token,
        'channel': slack_channel,
        'text': message,
    }).json()

def send_email(message):
    try:
        msg = Message(subject="[Thông báo] Thay đổi trên hệ thống Netbox",
                      sender=config.EMAIL_SENDER,
                      recipients=config.EMAIL_RECEIVE,
                      body=message)
        mail.send(msg)

    except Exception as ex:
        print(str(ex))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
