import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


@app.route('/send-email', methods=['POST'])
def send_email():
    email_data = request.get_json()

    from_email = f"{email_data['name']} <{EMAIL_HOST_USER}>"
    to_email = email_data['to']
    subject = email_data['subject']
    html_message = email_data['html_message']

    try:
        send_email_smtp(from_email, to_email, subject, html_message)
        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Internal Server Error', 'error': str(e)}), 500


def send_email_smtp(from_email, to_email, subject, html_message):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_message, 'html'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    server.send_message(msg)
    server.quit()


@app.route('/', methods=['GET'])
def health_check():
    return jsonify({'message': 'Hello world!, This service is running as expected'}), 200


if __name__ == '__main__':
    app.run(port=456)
