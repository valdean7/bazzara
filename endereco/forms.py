from django import forms
from .models import Endereco


class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = [
            'foto', 'nome_completo', 'telefone', 'estado', 'cidade', 'rua', 'bairro', 'numero', 'cep'
        ]


    def clean(self):
        cleaned = self.cleaned_data
        validation_error_msg = {}


        if cleaned.get('telefone') and len(cleaned.get('telefone')) < 11:
            validation_error_msg['telefone'] = 'Telefone precisa ter 11 números'

        if cleaned.get('cep') and len(cleaned.get('cep')) < 8:
            validation_error_msg['cep'] = 'CEP precisa ter 8 números.'

        if validation_error_msg:
            raise forms.ValidationError(validation_error_msg)