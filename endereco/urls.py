from django.urls import path
from . import views


app_name = 'endereco'

urlpatterns = [
    path('', views.endereco, name='meu_endereco'),
    path('editar/', views.editar_endereco, name='editar_endereco'),
    path('criar/', views.criar_endereco, name='criar_endereco'),
    path('apagar/', views.apagar_endereco, name='apagar_endereco'),
]
