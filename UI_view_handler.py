import os
from gmail_graph import GmailGraph
from main import ServiceMonitoringMainRunner
from util import read_yaml
from logger import logging
import threading

class View_handler():
    def __init__(self):

        logging.info(f"Starting View handler initialization... ")
        self.runner=ServiceMonitoringMainRunner()
        self.graphical_orientation=GmailGraph()
        self._lock = threading.Lock()
        self._is_running = False  # Flag to check if the process is already running
        self.current_batch=None
    
    def main_view_handler(self):

        self.config=read_yaml("config.yaml")
        context = {'config': self.config}
        
        if self.config['STATUS'] == 1:
            logging.info(f"Starting Main handler... ")
            with self._lock:
                if not self._is_running:
                    self._is_running = True  # Set the flag to True
                    try:
                        logging.info("Trying to start monitoring...")
                        self.runner.start()  # Start the process
                    finally:
                        self._is_running = False  # Reset the flag after the process ends
                else:
                    logging.info("Process is already running.")
            logging.info("Returning current batch...")
            graph_data=self.graphical_orientation.plot_graph()
            current_batch,emails_to_process,time_remaining,time_type= self.runner.get_current_running_details()
            logging.debug(f"email length {emails_to_process}")
            return context, current_batch, emails_to_process,time_remaining,time_type,graph_data
        elif self.config['STATUS']==0:
            try:
                logging.info("Trying to stop monitoring...")
                self.runner.stop() # Stop the process
            except Exception as e:
                raise e
            return context, None,None,None,None,None # Return None for rest arguments 
            
        else:
            logging.error("Invalid status in config.yaml")
            return context, None,None,None,None,None # Return None for rest arguments