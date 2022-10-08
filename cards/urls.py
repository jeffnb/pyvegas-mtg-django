from django.urls import path

from cards import views

app_name = 'cards'

urlpatterns = [
    path('', views.index, name='index'),
]