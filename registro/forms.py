from django import forms
from django.contrib.auth.models import User


class RegistroForm(forms.ModelForm):
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput()
    )


    class Meta:
        model = User
        fields = [
            'username','first_name', 'last_name', 'email', 'password',
            'password2'
        ]


    def clean(self):
        cleaned = self.cleaned_data
        validation_error_msg = {}

        if cleaned:
            if User.objects.filter(username=cleaned.get('username')).exists():
                validation_error_msg['username'] = 'Nome de usuário já existe.'

            if cleaned.get('username') and len(cleaned.get('username')) < 3:
                validation_error_msg['username'] = 'Nome de usuário precisa \
                    ter 3 ou mais caracteres.'

            if len(cleaned.get('email')) < 1:
                validation_error_msg['email'] = 'Este campo é obrigatório.'

            if len(cleaned.get('first_name')) < 1:
                validation_error_msg['first_name'] = 'Este campo é obrigatório.'

            if len(cleaned.get('first_name')) < 3 \
            and len(cleaned.get('first_name')) >= 1:
                validation_error_msg['first_name'] = 'Nome precisa ter 3 ou \
                    mais caracteres.'

            if len(cleaned.get('last_name')) < 1:
                validation_error_msg['last_name'] = 'Este campo é obrigatório.'

            if cleaned.get('email'):
                if User.objects.filter(email=cleaned.get('email')).exists():
                    validation_error_msg['email'] = 'Esse e-mail já existe.'

            if cleaned.get('password') and len(cleaned.get('password')) < 8:
                validation_error_msg['password'] = 'Senha deve ter 8 ou mais \
                    caracteres.'

            if cleaned.get('password2') and len(cleaned.get('password2')) < 8:
                validation_error_msg['password2'] = 'Senha deve ter 8 ou mais \
                    caracteres.'

            if cleaned.get('password') != cleaned.get('password2'):
                validation_error_msg['password2'] = 'Senha não coincide com a \
                    anterior.'
            

        if validation_error_msg:
            raise forms.ValidationError(validation_error_msg)