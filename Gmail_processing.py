import pandas as pd
from datetime import datetime,timedelta
from logger import logging
from util import read_yaml
from Gmail_fetcher import GmailFetcher
from Gmail_sender import GmailClient

class GmailProcess():
    def __init__(self) -> None:
        self.config=read_yaml("config.yaml")
        self.mail_fetcher = GmailFetcher()
        self.mail_sender = GmailClient()

    # Function to process emails
    def process_emails(self,):
        logging.debug(f"Inside process_emails function")
        try:
            data = pd.read_csv(self.config.get('CSV_FILE'))     # Initaily data reading from CSV file
            logging.info("CSV file read successfully.")
        except Exception as e:
            logging.error(f"Failed to read CSV file: {e}") # exception  occurred during reading csv file    
            raise

        # Ensure 'Last Sent' column exists if not it will create a new column Last Sent
        if 'Last Sent' not in data.columns:
            data['Last Sent'] = ''

        # will fetch all the latest mails.
        emails = self.mail_fetcher.fetch_emails() # return subject, from, data and message packed in list
        
        if not emails:
            logging.info(f"No new emails to process till {datetime.now()}")   # if the returned emails is none then no processing.

        else:
            logging.info(f"Processing {len(emails)} new emails at {datetime.now()}")
        
            now = datetime.now()
            for subject, from_email, date, msg in emails:
                for index, row in data.iterrows():
                    logging.debug(f"Processing {index}")
                    csv_subject = row['Subject'].strip().lower()  
                    additional_recipients = row['additional_recipients'].split(';') if pd.notna(row.get('additional_recipients', '')) else []

                    # Check if today's date is already in the 'Last Sent' column
                    last_sent_str = row['Last Sent'] if pd.notna(row.get('Last Sent', '')) else ''
                    last_sent_date = datetime.strptime(last_sent_str, '%Y-%m-%d %H:%M:%S') if last_sent_str else None
                    logging.debug(f'sent_for_crtitcal ')
                    sent_for_critical = str(row.get('sent_for_critical', '')).strip().lower() == 'received'
                    logging.debug(f'sent_for_down ')
                    sent_for_down = str(row.get('sent_for_down', '')).strip().lower() == 'received'
                    is_critical = 'critical' in subject.lower()
                    is_down = 'down' in subject.lower()

                    if last_sent_date and (now - last_sent_date < timedelta(hours=5)) and not (is_critical and sent_for_down) and not (is_down and sent_for_critical):
                        logging.info(f"Email for subject '{csv_subject}' was already sent today. Skipping...")
                        continue

                    if csv_subject in subject.lower() and any(keyword in subject.lower() for keyword in self.config.get('KEYWORDS')):
                        logging.info(f"Subject matches: {subject}") 
                        all_recipients = [row['Email_list']] + additional_recipients
                        
                        # Handle multipart email content
                        if msg.is_multipart():
                            body = ''.join(part.get_payload(decode=True).decode() for part in msg.walk() if part.get_content_type() == 'text/plain')
                        else:
                            body = msg.get_payload(decode=True).decode()
                        reply=self.config.get('REPLY_MESSAGE')
                        reply_body = f"{reply}\n\nOriginal Message:\n{body}"                   

                        # Create the forward message and attach the original email
                        original_email_str = msg.as_string()
                        self.mail_sender.send_email(all_recipients, f"Fwd: {subject}", reply_body, original_email_str)

                        # Update CSV to keep track of sent emails
                        if is_critical:
                            data.at[index,'sent_for_critical'] = 'received'
                        if is_down:
                            data.at[index,'sent_for_down'] = 'received'
                        data.at[index, 'Last Sent'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        data.to_csv(self.config.get('CSV_FILE'), index=False)
                        logging.info(f"Updated CSV with sent email for subject: {csv_subject}")
                        logging.info(f"Re-reading csv file: {self.config.get('CSV_FILE')}")
                        data = pd.read_csv(self.config.get('CSV_FILE')) # Re-reading the updated CSV file.
                        break
                    else:
                        pass    # if not matched, just ignoring 
            return len(emails)