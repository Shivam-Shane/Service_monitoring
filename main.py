import time
import datetime
from logger import logging 
from Gmail_processing import GmailProcess  
from util import read_yaml  
import threading  
import os  


# Class to monitor and run the email processing service continuously
class ServiceMonitoringMainRunner:

    def __init__(self):    
        self.config = read_yaml("config.yaml")
        self.GmailProcessObject = GmailProcess()
        self.running = threading.Event()
        self.lock = threading.Lock()  # Lock to ensure single processing of process email
        self.thread = None
        self.current_batch = 0
        self.total_batches_processed = 0  # Persistent across multiple runs on runner method.
        self.emails_to_process=0
        self.time_remaining = 0

    def runner(self):
        """Runs the service monitoring service
        Args: None
        Returns: Current_batch(integer)
        """
        logging.info(f"Starting Service monitoring at {datetime.datetime.now()}")
        self.current_batch = 0

        # loop: runs continuously until the stop signal is received
        while self.running.is_set():
            start_time = time.time()  # Record the start time of the current batch

            try:
                # Acquire the lock before processing emails to ensure only one execution at a time
                with self.lock:
                    self.emails_to_process=self.GmailProcessObject.process_emails()
                    self.current_batch += 1
                    self.total_batches_processed += 1

            except Exception as e:
                logging.error(f"Error during email processing: {e}")
                break  

            # Calculate the time taken for processing
            elapsed_time = time.time() - start_time
            # Determine remaining time to wait before starting the next batch
            remaining_time = max(self.config.get('TIME_THRESHOLD') - elapsed_time, 0)
            self.time_remaining=remaining_time

            logging.info(f"Waiting for next batch to start :: {self.total_batches_processed} \n"
                         f"Next batch will start in {remaining_time // 60 if remaining_time > 60 else remaining_time} "
                         f"{'minutes' if remaining_time > 60 else 'seconds'}")

            # Sleep in short intervals to allow checking for stop signals
            sleep_interval = 1  # Sleep interval in seconds
            total_sleep_time = 0  # Total time slept
            
            # Continue sleeping until the remaining time is reached
            while total_sleep_time < remaining_time:
                if not self.running.is_set():
                    # Exit early if a stop signal is received
                    logging.info("Stop signal received. Exiting early.")
                    return self.current_batch  # Return current_batch when exiting early

                time.sleep(sleep_interval)  # Sleep for a short interval
                total_sleep_time += sleep_interval  # Increment the total sleep time

        # Clear the console when the processing stops
        os.system('cls')
        logging.info("Processing stopped.")
        return self.current_batch, self.emails_to_process,self.time_remaining # Return current_batch when the loop ends

    def get_current_batch(self):
        """ Returns the current batch only if the runner is active.
        Args: None

        Return: total_batch_size_that_are_processed
        """
        if self.running.is_set():
            return self.total_batches_processed,self.emails_to_process,self.time_remaining  # Return the total processed batches
        else:
            return None  # Runner is not active

    # Method to start the service
    def start(self):
        """Start the monitoring process
        Args: None
        Returns: None
        """
        if self.thread and self.thread.is_alive():
            # Prevent starting multiple threads if the service is already running
            logging.warning("Service is already running.")
            return

        # Set the running event and start the service in a new thread
        self.running.set()
        self.thread = threading.Thread(target=self.runner)
        self.thread.start()

    # Method to stop the service
    def stop(self):
        """Stop the monitoring process
        Desc: Stop the monitor process when a stop signal received from the UI, terminate any working process of service
        Args: None
        Returns: None
        """
        self.running.clear()  # Clear the running event to signal stopping

        if self.thread and self.thread.is_alive():
            # Wait for the thread to stop, with a timeout to avoid indefinite waiting
            self.thread.join(timeout=60) # 60 Seconds to wait for the thread to stop
            if self.thread.is_alive():
                # Log a warning if the thread did not stop in time
                logging.warning("Thread did not stop in time.")
                # forceful termination if required
        else:
            logging.info("Thread was not running.")  