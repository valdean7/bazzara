from django.test import TestCase
from pytest import mark
from django.urls import reverse
from mocks.mocks import MockEndereco, MockUser


class TestEnderecoAppViews(TestCase):
    def setUp(self):
        self.meu_endereco_url = reverse('endereco:meu_endereco')
        self.criar_endereco_url = reverse('endereco:criar_endereco')
        self.editar_endereco_url = reverse('endereco:editar_endereco')
        self.user_mock = MockUser()
        self.endereco_mock = MockEndereco()

    @mark.endereco
    def test_endereco_should_redirect_if_not_logged_in(self):
        response = self.client.get(self.meu_endereco_url)
        self.assertEqual(response.status_code,302)

    @mark.endereco
    def test_endereco_should_redirect_if_logged_in_and_no_adress(self):
        self.user_mock.create_user()
        is_logged = self.client.login(username='jhon', password='1q2w3e4r')
        self.assertEqual(is_logged,True)
        response = self.client.get(self.meu_endereco_url)
        self.assertEqual(response.status_code, 302)

    @mark.endereco
    def test_endereco_should_not_redirect_if_logged_in_and_have_adress(self):
        user = self.user_mock.create_user()
        self.client.login(username=user.username, password='1q2w3e4r')
        self.endereco_mock.create_endereco(user)
        response = self.client.get(self.meu_endereco_url)
        self.assertEqual(response.status_code, 200)

    @mark.endereco
    def test_criar_endereco_should_redirect_if_not_logged_in(self):
        response = self.client.get(self.criar_endereco_url)
        self.assertEqual(response.status_code,302)

    @mark.endereco
    def test_criar_endereco_should_not_redirect_if_logged_in(self):
        user = self.user_mock.create_user()
        self.client.login(username=user.username, password='1q2w3e4r')
        response = self.client.get(self.criar_endereco_url)
        self.assertEqual(response.status_code,200)

    @mark.endereco
    def test_criar_endereco_should_redirect_when_creating_the_adress(self):
        user = self.user_mock.create_user()
        self.client.login(username=user.username, password='1q2w3e4r')
        data = {
            'nome_completo': 'Jhon Doe',
            'telefone': '89994000000',
            'estado': 'PI',
            'cidade': 'Acoã',
            'rua': 'Pedro Mendes',
            'bairro': 'Centro',
            'numero': '7',
            'cep': '00000000'
        }
        response = self.client.post(self.criar_endereco_url, data=data)
        self.assertEqual(response.status_code,302)

    @mark.endereco
    def test_criar_endereco_should_not_save_if_telefone_field_has_more_than_11_numbers(self):
        user = self.user_mock.create_user()
        self.client.login(username=user.username, password='1q2w3e4r')
        data = {
            'nome_completo': 'Jhon Doe',
            'telefone': '899940000000',
            'estado': 'PI',
            'cidade': 'Acoã',
            'rua': 'Pedro Mendes',
            'bairro': 'Centro',
            'numero': '7',
            'cep': '00000000'
        }
        response = self.client.post(self.criar_endereco_url, data=data)
        html = response.content.decode('utf-8')
        self.assertIn(
            'Certifique-se de que o valor tenha no máximo 11 caracteres (ele possui 12).',
            html
        )

    @mark.endereco
    def test_criar_endereco_should_not_save_if_telefone_field_has_less_than_11_numbers(self):
        user = self.user_mock.create_user()
        self.client.login(username=user.username, password='1q2w3e4r')
        data = {
            'nome_completo': 'Jhon Doe',
            'telefone': '8999400000',
            'estado': 'PI',
            'cidade': 'Acoã',
            'rua': 'Pedro Mendes',
            'bairro': 'Centro',
            'numero': '7',
            'cep': '00000000'
        }
        response = self.client.post(self.criar_endereco_url, data=data)
        html = response.content.decode('utf-8')
        self.assertIn(
            'Telefone precisa ter 11 números',
            html
        )

    @mark.endereco
    def test_criar_endereco_should_not_save_if_cep_field_has_less_than_8_numbers(self):
        user = self.user_mock.create_user()
        self.client.login(username=user.username, password='1q2w3e4r')
        data = {
            'nome_completo': 'Jhon Doe',
            'telefone': '89994000000',
            'estado': 'PI',
            'cidade': 'Acoã',
            'rua': 'Pedro Mendes',
            'bairro': 'Centro',
            'numero': '7',
            'cep': '0000000'
        }
        response = self.client.post(self.criar_endereco_url, data=data)
        html = response.content.decode('utf-8')
        self.assertIn(
            'CEP precisa ter 8 números.',
            html
        )

    @mark.endereco
    def test_editar_endereco_should_redirect_if_not_logged_in(self):
        response = self.client.get(self.editar_endereco_url)
        self.assertEqual(response.status_code, 302)

    @mark.endereco
    def test_editar_endereco_should_redirect_if_logged_in_and_no_adress(self):
        user = self.user_mock.create_user()
        self.client.login(username=user.username, password='1q2w3e4r')
        response = self.client.get(self.editar_endereco_url)
        self.assertEqual(response.status_code, 302)

    @mark.endereco
    def test_editar_endereco_should_not_redirect_if_logged_in_and_have_adress(self):
        user = self.user_mock.create_user()
        self.client.login(username=user.username, password='1q2w3e4r')
        self.endereco_mock.create_endereco(user)

        response = self.client.get(self.editar_endereco_url)
        self.assertEqual(response.status_code, 200)

    @mark.endereco
    def test_editar_endereco_should_not_save_if_telefone_field_has_more_than_11_numbers(self):
        user = self.user_mock.create_user()
        self.client.login(username=user.username, password='1q2w3e4r')
        endereco = self.endereco_mock.create_endereco(user)
        data = {
            'nome_completo': endereco.nome_completo, 'telefone': f'{endereco.telefone}0', 'estado': endereco.estado, 'cidade': endereco.cidade,
            'rua': endereco.rua, 'bairro': endereco.bairro, 'numero': endereco.numero, 'cep': f'{endereco.cep}'
            }

        response = self.client.post(self.editar_endereco_url, data=data)
        html = response.content.decode('utf-8')
        self.assertIn('Certifique-se de que o valor tenha no máximo 11 caracteres (ele possui 12).', html)

    @mark.endereco
    def test_editar_endereco_should_not_save_if_telefone_field_has_less_than_11_numbers(self):
        user = self.user_mock.create_user()
        self.client.login(username=user.username, password='1q2w3e4r')
        endereco = self.endereco_mock.create_endereco(user)
        data = {
            'nome_completo': endereco.nome_completo, 'telefone': f'8999400000', 'estado': endereco.estado, 'cidade': endereco.cidade,
            'rua': endereco.rua, 'bairro': endereco.bairro, 'numero': endereco.numero, 'cep': f'{endereco.cep}'
            }

        response = self.client.post(self.editar_endereco_url, data=data)
        html = response.content.decode('utf-8')
        self.assertIn('Telefone precisa ter 11 números', html)

    @mark.endereco
    def test_editar_endereco_should_not_save_if_cep_field_has_more_than_8_numbers(self):
        user = self.user_mock.create_user()
        self.client.login(username=user.username, password='1q2w3e4r')
        endereco = self.endereco_mock.create_endereco(user)
        data = {
            'nome_completo': endereco.nome_completo, 'telefone': f'{endereco.telefone}', 'estado': endereco.estado, 'cidade': endereco.cidade,
            'rua': endereco.rua, 'bairro': endereco.bairro, 'numero': endereco.numero, 'cep': f'{endereco.cep}0'
            }

        response = self.client.post(self.editar_endereco_url, data=data)
        html = response.content.decode('utf-8')
        self.assertIn('Certifique-se de que o valor tenha no máximo 8 caracteres (ele possui 9).', html)

    @mark.endereco
    def test_editar_endereco_should_not_save_if_cep_field_has_less_than_8_numbers(self):
        user = self.user_mock.create_user()
        self.client.login(username=user.username, password='1q2w3e4r')
        endereco = self.endereco_mock.create_endereco(user)
        data = {
            'nome_completo': endereco.nome_completo, 'telefone': f'{endereco.telefone}', 'estado': endereco.estado, 'cidade': endereco.cidade,
            'rua': endereco.rua, 'bairro': endereco.bairro, 'numero': endereco.numero, 'cep': f'0000000'
            }

        response = self.client.post(self.editar_endereco_url, data=data)
        html = response.content.decode('utf-8')
        self.assertIn('CEP precisa ter 8 números.', html)

    @mark.endereco
    def test_editar_endereco_should_save_if_all_fields_is_ok(self):
        user = self.user_mock.create_user()
        self.client.login(username=user.username, password='1q2w3e4r')
        endereco = self.endereco_mock.create_endereco(user)
        data = {
            'nome_completo': 'Jhon Doe', 'telefone': f'89994112233', 'estado': 'AA', 'cidade': 'Central',
            'rua': endereco.rua, 'bairro': endereco.bairro, 'numero': endereco.numero, 'cep': f'00000000'
            }

        response = self.client.post(self.editar_endereco_url, data=data)
        self.assertEqual(response.status_code, 302)
