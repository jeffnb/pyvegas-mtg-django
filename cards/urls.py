from django.urls import path

from cards import views

app_name = 'cards'

urlpatterns = [
    path('', views.form_create, name='create-card'),
]