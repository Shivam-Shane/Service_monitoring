from logger import logging
from util import read_yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import logging

class GmailClient():
    def __init__(self):
        self.config=read_yaml("config.yaml")

    def send_email(self, to_emails, subject, body, original_email_str=None):
        msg = MIMEMultipart()
        msg['From'] = f'{self.config.SENDER_NAME} <{self.config.SMTP_USERNAME}>'
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if original_email_str:
            part = MIMEBase('message', 'rfc822')
            part.set_payload(original_email_str)
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename='original_message.eml')
            msg.attach(part)

        try:
            server = smtplib.SMTP(self.config["SMTP_SERVER"], self.config["SMTP_PORT"])
            server.starttls()
            server.login(self.config["SMTP_USERNAME"], self.config["SMTP_PASSWORD"])
            server.sendmail(self.config["SMTP_USERNAME"], to_emails, msg.as_string())
            logging.info(f"Email sent to {', '.join(to_emails)}")
        except Exception as e:
            logging.error(f"Failed to send email to {', '.join(to_emails)}: {str(e)}")
        finally:
            server.quit()