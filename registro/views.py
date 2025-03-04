from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http.request import HttpRequest
from django.contrib import messages
from .forms import RegistroForm
from django.contrib.auth import login, authenticate, logout
from utils.validators import is_email
from copy import deepcopy

def registrar(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'index.html', {'form': {}})
    
    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            try:
                password = form.cleaned_data.get('password')
                usuario = form.save(commit=False)
                usuario.set_password(password)
                usuario.save()
                messages.success(request, 'Conta criada com sucesso.')
                return redirect('registro:registrar')
            except:
                messages.error(request, 'Houve uma falha ao criar a conta, tente novamente.')
                return redirect('registro:registrar')
        else:
            return render(request, 'index.html', {'form': form})


def entrar(request: HttpRequest):
    if request.method == 'POST':
        credencial = request.POST.get('credencial')
        password = request.POST.get('passwordd')

        username = ''

        if is_email(credencial):
            if User.objects.filter(email=credencial).exists():
                username = User.objects.filter(email=credencial).first().username
            else:
                username = credencial
        else:
            username = credencial

        usuario = authenticate(request, username=username, password=password)
        
        if not usuario:
            messages.info(request, 'Usuário/E-mail ou senha está incorreto.')
            return redirect('registro:registrar')
        
        login(request, usuario)

        return redirect('produtos:home')


def sair(request: HttpRequest):
    if request.session.get('carrinho'):
        carrinho = deepcopy(request.session['carrinho'])
        logout(request)
        request.session['carrinho'] = carrinho
        request.session.save()
    else:
        logout(request)
    return redirect('produtos:home')
    