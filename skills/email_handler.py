import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config

def send_email(to, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = config.EMAIL_ADDRESS
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
        server.sendmail(config.EMAIL_ADDRESS, to, msg.as_string())
        server.quit()

        return f"Email sent to {to} successfully Boss"
    except Exception as e:
        return f"Failed to send email Boss: {str(e)}"