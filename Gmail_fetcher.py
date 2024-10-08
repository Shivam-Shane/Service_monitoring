import imaplib
import socket
import ssl
from email import message_from_bytes
from email.header import decode_header
from logger import logging
from gmail_processing_checker import GmailProcceschecker
from util import read_yaml

class GmailFetcher():
    def __init__(self):
        self.config = read_yaml("config.yaml")
        self.GmailProccescheckerobject = GmailProcceschecker()  
        
    def fetch_emails(self):
        try:
            try:
                logging.debug(f"Tring Connecting to {self.config.get('IMAP_SERVER')}")

                self.mail = imaplib.IMAP4_SSL(self.config.get('IMAP_SERVER'))
                self.mail.login(self.config.get('SMTP_USERNAME'), self.config.get('SMTP_PASSWORD'))
                self.mail.select('inbox')
                logging.info(f"Connected to {self.config.get('IMAP_SERVER')}")
            except (socket.gaierror, socket.timeout) as net_err:
                logging.error(f"Network issue while connecting to IMAP server: {str(net_err)}")
                return []
            except ssl.SSLError as ssl_err:
                logging.error(f"SSL error while connecting to IMAP server: {str(ssl_err)}")
                return []
            except imaplib.IMAP4.error as imap_err:
                logging.error(f"IMAP error: {str(imap_err)}")
                return []
            except Exception as e:
                logging.error(f"Failed to connect to IMAP server: {str(e)}")
                return []

            # Search for emails from 'itsupport@ivp.in' and that are unseen
            search_criteria = '(UNSEEN FROM "itsupport@ivp.in")'
            result, data = self.mail.search(None, search_criteria)
            # Check if search result is valid
            if result != 'OK':
                logging.error(f"Search failed with result: {result}")
                return []
            
            email_ids = data[0].split() if data[0] else [] #  # Ensure data[0] exists
            logging.debug(f"Emails found: {email_ids}")
            if not email_ids:
                logging.info("No emails found matching the criteria.")
                return []
            
            emails = [] # all emails retived from the database
            unique_subjects = set() # stores all unique subjects
            filtered_emails = []  # filtered email for futher processing 
            for email_id in email_ids:
                logging.debug(f"Emails {email_id}")
                result, message_data = self.mail.fetch(email_id, '(RFC822)')

                if isinstance(message_data[0], tuple) and isinstance(message_data[0][1], bytes):
                    raw_email = message_data[0][1]  # Making sure it's bytes
                    msg = message_from_bytes(raw_email)
                else:
                    logging.error(f"Unexpected message_data format for email_id {email_id}.")
                    continue 
                # Decode the subject and handle encoding issues
                subject, encoding = decode_header(msg['subject'])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else 'utf-8')

                from_email = msg.get('from', 'Unknown') # eunsing it return something, so don't raise errors
                date = msg.get('date', 'Unknown')

                logging.debug(f"Fetched email - Subject: {subject}, From: {from_email}, Date: {date}")
                emails.append((subject, from_email, date, msg)) # Appends all emails data
            sorted_emails = sorted(emails, key=lambda x: x[2], reverse=True) # sorting the emails by date
            logging.debug(f"Sorted emails {emails}")
            for email in sorted_emails: 
                subject, from_email, date, msg = email
                # ensure subject id not duplicates and checks it should process only legimate emails
                if subject not in unique_subjects and self.GmailProccescheckerobject.should_process_email(subject, from_email, date):
                    filtered_emails.append(email)  # Add to final list
                    unique_subjects.add(subject)  # Mark subject as processed
                else:
                    logging.debug(f"Skipping email - Subject: {subject}, From: {from_email}, Date: {date}")
            logging.debug(f"filtered emails {filtered_emails}")
            self.mail.logout()
            return emails            
        except imaplib.IMAP4.error as e:
            logging.error(f"IMAP error: {str(e)}")
        except Exception as e:
            logging.error(f"General error: {str(e)}")