from django.urls import path

from cards import views

urlpatterns = [path('', views.index, name='index'),]