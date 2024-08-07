# monitor/views.py
from django.shortcuts import render, redirect
from util import read_yaml,update_yaml # type:ignore
# from tasks import start_monitoring, stop_monitoring # type: ignore

def index_view(request):
    config = read_yaml("config.yaml")

    return render(request, 'index.html', {'config': config})

