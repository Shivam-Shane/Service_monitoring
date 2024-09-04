import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import io
from logger import logging
import matplotlib
from util import read_yaml

class GmailGraph:
    def __init__(self):
        matplotlib.use('Agg') # Using Agg so there is no issue of main thread execution that matplotlib accepts
        self.data_config=read_yaml("config.yaml")

    def load_data(self): # For loading the dataset
        return pd.read_csv(self.data_config.get('CSV_FILE'))
    
    def plot_graph(self):
        try:

            email_sent_per_day=self.email_sent_per_day_graph()
            email_sent_for_per_service=self.email_sent_for_per_service_graph()
            heatmap_of_activity=self.heatmap_of_activity_graph()
        
            return {
            'email_sent_per_day': email_sent_per_day,
            'email_sent_for_per_service': email_sent_for_per_service,
            'heatmap_of_activity': heatmap_of_activity }
        except Exception as e:
            logging.error(f"Failed to generate graphs: {str(e)}")
            raise e
    
    def email_sent_per_day_graph(self):
        # Load data from CSV file and convert 'Last Sent' to datetime format
        self.data=self.load_data()

        if self.data['Last Sent'].empty:
            logging.warning("DataFrame is empty. Skipping plot creation.")
            return None
        
        self.data['Last Sent']=pd.to_datetime(self.data['Last Sent'], errors='coerce') 
        self.data = self.data.dropna(subset=['Last Sent'])    # remove any null values
        emails_per_day = self.data.groupby(self.data['Last Sent'].dt.date).size()
        
        fig, ax = plt.subplots(figsize=(8, 4))
        # Plotting 
        plt.plot(emails_per_day.index, emails_per_day.values, marker='o', linestyle='-', color='b')
        plt.title('Number of Emails Sent Per Day')
        plt.xlabel('Date')
        plt.ylabel('Number of Emails')
        plt.xticks(rotation=45)
        plt.tight_layout()
        # Save the plot to a BytesIO object
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        plt.close(fig)

        # Free up memory
        del self.data

        logging.debug('Returning Number of Emails Sent Per Day chart in form of BytesIO')
        return img_buffer

    def email_sent_for_per_service_graph(self):
        self.data=self.load_data()

        if self.data['Last Sent'].empty:
            logging.warning("DataFrame is empty. Skipping plot creation.")
            return None
        
        # Count the number of emails sent for each 'service'
        name_counts = self.data['Name'].value_counts()
        names=name_counts[0:5]

        # Plotting
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.barplot(x=names.index, y=names.values,hue=names.index, palette='coolwarm')
        plt.title('Number of Emails Sent for Each Service')
        plt.ylabel('Number of Emails')
        plt.xlabel('Services')
        plt.xticks(rotation=45)
        plt.tight_layout()
        # Save the plot to a BytesIO object
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        plt.close(fig)

        # Free up memory
        del self.data

        logging.debug('Returning Emails Sent for Each Service chart in form of BytesIO')
        return img_buffer


    def heatmap_of_activity_graph(self):
        self.data=self.load_data()

        if self.data['Last Sent'].empty:
            logging.warning("DataFrame is empty. Skipping plot creation.")
            return None  
             
        self.data['Last Sent']=pd.to_datetime(self.data['Last Sent'], errors='coerce') # convert to datetime format
        self.data = self.data.dropna(subset=['Last Sent'])  # remove any null values
        self.data['Hour'] = self.data['Last Sent'].dt.hour #Getting hour from dates
        self.data['Day'] = self.data['Last Sent'].dt.day_name() # getting day from dates
        
        # Plotting
        fig, ax = plt.subplots(figsize=(8, 4))
        pivot_table = self.data.pivot_table(index='Hour', columns='Day', aggfunc='size', fill_value=0)
        if pivot_table.empty:
            logging.warning("No data to generate Heatmap. Skipping plot creation.")
            return None
        sns.heatmap(pivot_table, cmap="YlGnBu", linewidths=.5, annot=True, fmt="d")
        plt.title('Heatmap of Email Activity by Hour and Day')
        plt.xlabel('Day of the Week')
        plt.ylabel('Hour of the Day')
        plt.tight_layout()

        # Save the plot to a BytesIO object
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        plt.close(fig)

        # Free up memory
        del self.data
    
        logging.debug('Returning Heatmap email activity graph in form of BytesIO')
        return img_buffer