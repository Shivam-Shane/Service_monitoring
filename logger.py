import logging
import os
logger=logging.getLogger("Gmail_Monitoring")               #using named loggers, we can control the logging level for different parts

LOG_FILE = "gmail_monitoring.log"                          # What type of log file name to use
LOGS_PATH = os.path.join(os.getcwd(), "LOGS", LOG_FILE)    # Path where the log will be stored   
os.makedirs(LOGS_PATH, exist_ok=True)                      # Making sure the directory exists
LOG_FILE_PATH = os.path.join(LOGS_PATH, LOG_FILE)          # Saving the log file path for log files

# Configure logging
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)          # console logging level to DEBUG
logging.getLogger().addHandler(console_handler)  # console handler to the root logger