import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# SMTP configuration
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your-email@example.com'
SMTP_PASSWORD = 'your-password'


def send_email(subject, recipient, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = SMTP_USERNAME
        msg['To'] = recipient

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, recipient, msg.as_string())

        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        traceback.print_exc()
        return False


def send_email_with_html_body(subject, recipient, html_body):
    try:
        # Create a multipart message
        msg = MIMEMultipart("alternative")
        msg['Subject'] = subject
        msg['From'] = SMTP_USERNAME
        msg['To'] = recipient

        # Attach the HTML body
        msg.attach(MIMEText(html_body, "html"))

        # Send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, recipient, msg.as_string())

        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        traceback.print_exc()
        return False

