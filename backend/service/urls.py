from django.urls import path

from . import views

urlpatterns = [
    path('ws_port/', views.WsPort.as_view(), name='ws_port'),
    path('document_xml/', views.DocumentXML.as_view(), name='document_xml')
]
