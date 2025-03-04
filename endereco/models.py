from django.db import models as m
from django.contrib.auth.models import User


class Endereco(m.Model):
    usuario = m.OneToOneField(User,on_delete=m.CASCADE, related_name='endereco')
    foto = m.ImageField(upload_to='perfils',null=True, blank=True)
    nome_completo = m.CharField(max_length=255)
    telefone = m.CharField(max_length=11)
    estado = m.CharField(max_length=30)
    cidade = m.CharField(max_length=50)
    rua = m.CharField(max_length=50)
    bairro = m.CharField(max_length=50)
    numero = m.CharField(max_length=10)
    cep = m.CharField(max_length=8)


    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'


    def __str__(self) -> str:
        return self.usuario.username
