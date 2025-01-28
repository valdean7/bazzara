from django.shortcuts import redirect, resolve_url
from django.contrib import messages
from django.conf import settings


def login_required_warning(redirect_url: str = None):
    """
    Redireciona para a url de login e cria uma message informando o usuario
    para realizar o login.
    """
    def wrapper(func):
        def iner(request, *args, **kwargs):
            url = resolve_url(redirect_url or settings.LOGIN_URL)
            if not url:
                raise Exception('Se o parametro `redirect_url` não for passado, o `LOGIN_URL` tem que ser configurado no settings.py.')
            
            if not request.user.is_authenticated:
                messages.warning(request, 'Você precisa estar logado para fazer essa ação. Realize o login.')
                return redirect(url)
            return func(request, *args, **kwargs)
        return iner
    return wrapper
