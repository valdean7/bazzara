from django.urls import path
from . import views

app_name = 'registro'

urlpatterns = [
   path('', views.registrar, name='registrar'),
   path('login/', views.entrar, name='login'),
   path('logout/', views.sair, name='logout'),

]
