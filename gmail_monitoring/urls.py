"""
URL configuration for gmail_monitoring project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# monitor/urls.py
from django.urls import path
from views import View_Functions
from django.urls import path

view_list=View_Functions()
urlpatterns = [
    
    path('', view_list.index_view, name='index_view'),
    path('start/', view_list.start_monitoring, name='start_monitoring'),
    path('stop/', view_list.stop_monitoring, name='stop_monitoring'),
]
