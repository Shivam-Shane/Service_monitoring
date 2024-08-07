import imaplib
import email
from email.header import decode_header
from logger import logging
from gmail_processing_checker import GmailProcceschecker
from util import read_yaml

class GmailFetcher():
    def __init__(self):
        self.config = read_yaml("config.yaml")

    def fetch_emails(self):
        try:
            logging.debug(f"Inside fetch_emails function")
            try:
                logging.debug(f"Connecting to {self.config.IMAP_SERVER}")
                mail = imaplib.IMAP4_SSL(self.config.IMAP_SERVER)
                mail.login(self.config.SMTP_USERNAME, self.config.SMTP_PASSWORD)
                mail.select('inbox')
                logging.debug(f"Connected to {self.config.IMAP_SERVER}")
            except Exception as e:
                logging.error(f"Failed to connect to IMAP server: {str(e)}")
                return []

            # Search for emails from 'itsupport@ivp.in' and that are unseen
            search_criteria = '(UNSEEN FROM "itsupport@ivp.in")'
            result, data = mail.search(None, search_criteria)
            email_ids = data[0].split()
            logging.info(f"Emails found: {email_ids}")

            emails = []
            for email_id in email_ids:
                result, message_data = mail.fetch(email_id, '(RFC822)')
                raw_email = message_data[0][1]
                msg = email.message_from_bytes(raw_email)

                subject, encoding = decode_header(msg['subject'])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else 'utf-8')

                from_email = msg['from']
                date = msg['date']
                logging.debug(f"Fetched email - Subject: {subject}, From: {from_email}, Date: {date}")
                
                if GmailProcceschecker.should_process_email(self,subject, from_email, date):  # This checkes if the email should be processed or not
                    emails.append((subject, from_email, date, msg))
                else:
                    logging.debug(f"Skipping email - Subject: {subject}, From: {from_email}, Date: {date}")
            mail.logout()

            return emails
        except imaplib.IMAP4.error as e:
            logging.error(f"IMAP error: {str(e)}")
        except Exception as e:
            logging.error(f"General error: {str(e)}")
        return []