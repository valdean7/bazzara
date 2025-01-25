from django.test import TestCase
from django.urls import reverse
from mocks.mocks import MockUser


class TestRegistroApp(TestCase):
    def setUp(self) -> None:
        self.registrar_url = reverse('registro:registrar')
        self.login_url = reverse('registro:login')
        self.user_mock = MockUser()


    def test_entrar_should_redirect_without_the_right_credencials(self):
        data = {'credencial': 'newUser', 'passwordd': '1q2w3e4r'}
        response = self.client.post(self.login_url, data=data)
        ...

    def test_loginng_a_new_user(self):
        ...


    def test_registrar_is_rendering(self):
        response = self.client.get(self.registrar_url)
        self.assertEqual(response.status_code, 200)


    def test_registrar_should_(self):
        data = {
            'username': 'valdean', 
            'email': 'valdean@mail.com',
            'password': '1q2w3e4r',
            'password2': '1q2w3e4r'
        }
        response = self.client.post(self.registrar_url, data=data)
        ...


