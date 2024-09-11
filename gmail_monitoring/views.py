from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from util import update_yaml # type:ignore
from gmail_graph import GmailGraph
from logger import logging
from UI_view_handler import View_handler
from io import BytesIO
import base64
from datetime import datetime
from django.http import JsonResponse
from django.template.loader import render_to_string

class View_Functions():
    def __init__(self):
        self.viewhandler=View_handler()
        self.graphical_orientation=GmailGraph()

    def index_view(self,request):
        # Fetch configuration details, current batch, and emails to process from view handler
        configuration_details,current_batch,emails_to_process,time_remaining,time_type,graph_data=self.viewhandler.main_view_handler()
        encoded_graphs = {}
        if graph_data is None:
             encoded_graphs=encoded_graphs
        else:
            for key, buffer in graph_data.items():
                if isinstance(buffer, BytesIO):
                    # If buffer is a BytesIO object, get its value directly
                    img_data = buffer.getvalue()
                else:
                    # If buffer is not BytesIO, it should be handled accordingly
                    img_data = buffer
                
                # Encode image data to base64
                encoded_graphs[key] = base64.b64encode(img_data).decode('utf-8') if img_data else None

        last_refresh_time = datetime.now().strftime('%H:%M:%S')
        # Combine all context data
        context = {
            'configuration_details': configuration_details,
            'current_batch': current_batch,
            'time_remaining':time_remaining,
            'time_type':time_type,
            'emails_to_process': emails_to_process,
            'email_sent_per_day': encoded_graphs.get('email_sent_per_day'),
            'email_sent_for_per_service': encoded_graphs.get('email_sent_for_per_service'),
            'heatmap_of_activity': encoded_graphs.get('heatmap_of_activity'),
            'last_refresh_time': last_refresh_time,
        }
        
        return render(request, 'index.html', context)
    
    def start_monitoring(self,request: HttpRequest)-> HttpResponse:
        if request.method == 'POST':
            try:
                update_yaml("config.yaml", {"STATUS":1})
            except Exception as e:
                logging.error(f"Failed to start monitoring: {e}")  # exception occurred during starting monitoring
                raise e
            return redirect('index_view')    # Transfer control to index view
        return redirect('index_view')

    def stop_monitoring(self,request: HttpRequest)-> HttpResponse:
        if request.method == 'POST':
            try:
                update_yaml("config.yaml", {"STATUS":0})
                return redirect('index_view')  # Transfer control to index view
            except Exception as e:
                logging.error(f"Failed to stop monitoring: {e}")  # exception occurred during starting monitoring
                raise e
        return redirect('index_view')  # Transfer control to index view