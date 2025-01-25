from django.test import TestCase
from django.urls import reverse
from mocks.mocks import MockProduto
import tempfile
from django.test import override_settings
import shutil
from django.conf import settings


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class TestProdutosAppViews(TestCase):
    def tearDown(self) -> None:
        shutil.rmtree(settings.MEDIA_ROOT, True)



    def setUp(self) -> None:
        self.home_url = reverse('produtos:home')
        self.add_carrinho_url = reverse('produtos:add_produto')
        self.carrinho_url = reverse('produtos:carrinho')
        self.mock_produto = MockProduto()

    def test_home_should_render(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)


    def test_detalhe_produto_should_raise_404_if_slug_is_not_correct(self):
        response = self.client.get(
            reverse('produtos:produto',args=('produto-slug',)))
        self.assertEqual(response.status_code, 404)


    def test_detalhe_produto_should_render_if_slug_is_correct(self):
        produto = self.mock_produto.criar_produto_completo(['M','G','GG'])
        response = self.client.get(
            reverse('produtos:produto',args=(produto.slug,)))
        self.assertEqual(response.status_code, 200)


    def test_adicionar_no_carrinho_dont_have_session_if_data_does_not_match(self):
        produto = self.mock_produto.criar_produto()
        variacao = self.mock_produto.criar_variacao()
        self.mock_produto.criar_especificacao('M')

        data = {
            'product': produto.pk,
            'product_name': produto.nome,
            'model': variacao.nome_variacao,
            'size': 'G', #dado errado (alterado)
            'slug': produto.slug,
            'image': variacao.imagem_variacao,
            'promotion': produto.promocao,
            'quant': 10,
            'price': produto.preco,
        }
        self.client.post(self.add_carrinho_url,data)
        carrinho = self.client.session.get('carrinho')
        self.assertIsNone(carrinho)


    def test_adicionar_no_carrinho_have_session_if_data_match(self):
        produto = self.mock_produto.criar_produto()
        variacao = self.mock_produto.criar_variacao()
        self.mock_produto.criar_especificacao('M')
        data = {
            'product': produto.id,
            'product_name': produto.nome,
            'model': variacao.nome_variacao,
            'size': 'M',
            'slug': produto.slug,
            'image': variacao.imagem_variacao,
            'promotion': produto.promocao,
            'quant': 10,
            'price': produto.preco,
        }
        self.client.post(self.add_carrinho_url, data)
        carrinho = self.client.session
        self.assertIn('carrinho', carrinho)
        self.assertIn(str(produto.id), carrinho['carrinho'])


    def test_carrinho_must_have_a_product(self):
        produto = self.mock_produto.criar_produto()
        variacao = self.mock_produto.criar_variacao()
        self.mock_produto.criar_especificacao('M')
        data = {
            'product': produto.id,
            'product_name': produto.nome,
            'model': variacao.nome_variacao,
            'size': 'M',
            'slug': produto.slug,
            'image': variacao.imagem_variacao,
            'promotion': produto.promocao,
            'quant': 10,
            'price': produto.preco,
        }
        self.client.post(self.add_carrinho_url, data)
        response = self.client.get(self.carrinho_url)
        content = response.content.decode('utf-8')
        self.assertIn(produto.nome, content)


    def test_remover_do_carrinho_should_delete_product_from_session(self):
        produto = self.mock_produto.criar_produto()
        variacao = self.mock_produto.criar_variacao()
        self.mock_produto.criar_especificacao('M')
        data = {
            'product': produto.id,
            'product_name': produto.nome,
            'model': variacao.nome_variacao,
            'size': 'M',
            'slug': produto.slug,
            'image': variacao.imagem_variacao,
            'promotion': produto.promocao,
            'quant': 10,
            'price': produto.preco,
        }
        self.client.post(self.add_carrinho_url, data)
        carrinho = self.client.session['carrinho']

        self.assertIn(str(produto.nome), carrinho[str(produto.id)][0]['produto_nome'])

        query = f'?pro={produto.id}&var={variacao.nome_variacao}&tamanho=M'

        response = self.client.get(f'{reverse('produtos:remover_produto')}{query}')

        carrinho2 = self.client.session['carrinho']

        self.assertNotIn(str(produto.id), carrinho2[str(produto.id)])

