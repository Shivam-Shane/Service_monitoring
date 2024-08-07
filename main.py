import time
import datetime
from logger import logging
from Gmail_processing import GmailProcess
from util import read_yaml

# Run the script continuously
class main():
    def __init__(self):
        self.config = read_yaml("config.yaml")
        self.Gamilprocess_object=GmailProcess()
    def runner(self):
        logging.info(f"Starting email processing at {datetime.datetime.now()}")
        batch=0
        while True:
            try: 
                self.Gamilprocess_object.process_emails()
                batch+=1
            except Exception as e:
                logging.error(f"Error during email processing: {e}")
                raise e
            logging.info(f"Waiting for next batch to start :: {batch} \n Next batch will start in  {self.config.TIME_THRESHOLD // 60 if self.config.TIME_THRESHOLD > 60 else self.config.TIME_THRESHOLD} {'minutes' if self.config.TIME_THRESHOLD > 60 else 'seconds'}")

            time.sleep(self.config.TIME_THRESHOLD)

if __name__ == "__main__":
    main_object=main()
    main_object.runner()