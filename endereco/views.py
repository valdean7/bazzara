from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http.request import HttpRequest
from .forms import EnderecoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Endereco


@login_required(login_url='registro:registrar')
def endereco(request: HttpRequest):
    if not Endereco.objects.filter(usuario=request.user).exists():
        return redirect('endereco:criar_endereco')
    endereco = get_object_or_404(Endereco, usuario=request.user)
    return render(request, 'endereco.html', {'endereco': endereco})


@login_required(login_url='registro:registrar')
def editar_endereco(request: HttpRequest):
    if request.method == 'GET':
        http_referer = request.META.get('HTTP_REFERER')
        if '/pagar_pedidos/' in http_referer:
            request.session['temp_url'] = reverse('pedidos:pagar_pedidos')
            request.session.modified = True

        if not Endereco.objects.filter(usuario=request.user).exists():
            return redirect('endereco:criar_endereco')
        endereco = get_object_or_404(Endereco, usuario=request.user)
        return render(request, 'editar_endereco.html', {'endereco': endereco})
    
    if request.method == 'POST':
        endereco = get_object_or_404(Endereco, usuario=request.user)
        form = EnderecoForm(request.POST, request.FILES, instance=endereco)

        try:
            if form.is_valid():
                form.save()
                if request.session.get('temp_url'):
                    del request.session['temp_url']
                    return redirect('pedidos:pagar_pedidos')
                
                return redirect('endereco:meu_endereco')
            else:
                form = EnderecoForm(request.POST, request.FILES, instance=endereco)
                return render(request, 'editar_endereco.html', {
                'endereco': request.POST, 
                'form': form
                })
        except:
            messages.error(request, 'Falha ao editar o endereco.')
            return redirect('endereco:meu_endereco')
            


@login_required(login_url='registro:registrar')
def criar_endereco(request: HttpRequest):
    if request.method == 'GET':
        if Endereco.objects.filter(usuario=request.user).exists():
            return redirect('endereco:meu_endereco')
        
        return render(request, 'criar_endereco.html', {'form': {}})
    
    if request.method == 'POST':
        form = EnderecoForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                endereco = form.save(commit=False)
                endereco.usuario = request.user
                endereco.save()
                messages.success(request, 'Endereço criado com sucesso.')
                return redirect('endereco:meu_endereco')
            else:
                return render(request, 'criar_endereco.html', {'form': form})
        except:
            messages.error(request, 'Falha ao criar o endereço.')
            return redirect('endereco:criar_endereco')


@login_required(redirect_field_name='endereco:criar_endereco')
def apagar_endereco(request: HttpRequest):
    endereco = Endereco.objects.filter(usuario=request.user).first()
    if endereco:
        try:
            endereco.delete()
        except:
            messages.error(request, 'Houve uma falha ao apagar o endereço.')
            return redirect('endereco:meu_endereco')
    return redirect('endereco:criar_endereco')