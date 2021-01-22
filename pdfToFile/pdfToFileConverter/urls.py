from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name="index"),
    path('index',views.index,name="index"),
    path('textFileConverter',views.textFileConverter,name="textFileConverter"),
    path('export_text_file', views.export_text_file, name='export_text_file')
]