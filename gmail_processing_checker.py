from logger import logging
from util import read_yaml
import pytz
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime

class GmailProcceschecker():
    def __init__(self):
        self.config=read_yaml("config.yaml")

    # Function to check if the email should be processed, it should process if the email is greater than a defined threshold
    def should_process_email(self,subject, from_email, date):
        
        if from_email.lower() != 'noreply via itsupport <itsupport@ivp.in>':
            logging.debug(f"Not found mails from {from_email.lower()} ")
            return False
        ist = pytz.timezone('Asia/Kolkata')  # Define IST timezone
        now = datetime.now(ist)  # Make 'now' timezone-aware with IST
        
        logging.debug(f"current time {now}")
        try:
            email_date = parsedate_to_datetime(date)  #converts the email date string into a datetime object.
        except Exception as e:
            logging.error(f"Error parsing date: {e}")
            return False
        
        if now - email_date > timedelta(minutes=self.config.TIME_THRESHOLD):  # if the email data is not greater than  a defined threshold
            return False
        else:
            logging.debug(f"Email {subject} is greater than {self.config.TIME_THRESHOLD} minutes timeout")
        return True