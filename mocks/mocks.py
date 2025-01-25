from django.contrib.auth.models import User
from endereco.models import Endereco
from produtos.models import Produto, Variacao, Especificacao, Categoria
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO


class MockUser:
    @classmethod
    def create_user(self):
        user = User.objects.create_user(username='jhon', email='email@mail.com', password='1q2w3e4r')
        return user


    @classmethod
    def get_user(self, username: str):
        user = User.objects.filter(username=username).first()
        return user
    

class MockEndereco(MockUser):
    @classmethod
    def create_endereco(self, usuario):
        endereco = Endereco(
            usuario=usuario,
            nome_completo='Jhon Doe',
            telefone='89994000000',
            estado='PI',
            cidade='Acoã',
            rua='Pedro Mendes',
            bairro='Centro',
            numero='7',
            cep='00000000'
        )
        endereco.save()

        return endereco
    

class MockProduto():

    produto_id = None
    variacao_id = None

    @staticmethod
    def criar_mock_imagem():
        imagem = Image.new('RGB',(100,100), (255,0,0))
        byte_array = BytesIO()
        imagem.save(byte_array,'JPEG')
        byte_array.seek(0)

        return SimpleUploadedFile('teste_imagem.jpg',byte_array.getvalue(),'image/jpeg')

    @classmethod
    def criar_produto(self):
        categoria = self.criar_categoria()
        produto = Produto(
            nome='teste produto nome',
            preco=55,
            slug='teste-produto-slug',
            descricao='test descricao do produto',
        )
        produto.save()
        produto.categoria.add(categoria)
        produto.save()
        self.produto_id = produto.pk

        return produto
    

    @classmethod
    def criar_categoria(self):
        categoria = Categoria.objects.create(nome_categoria='Testes')
        return categoria


    @classmethod
    def criar_variacao(self):
        variacao = Variacao(
            produto_id=self.produto_id,
            nome_variacao='test variacao 1',
            imagem_variacao=self.criar_mock_imagem()
        )
        variacao.save()
        self.variacao_id = variacao.pk
        return variacao


    @classmethod
    def criar_especificacao(self, *tamanhos: str):
        for tamanho in tamanhos:
            especificacao = Especificacao(
                variacao_id=self.variacao_id,
                tamanho=tamanho
            )
            especificacao.save()


    @classmethod
    def criar_produto_completo(self, tamanhos: list[str]):
        produto = self.criar_produto()
        self.criar_variacao()
        self.criar_especificacao(*tamanhos)
        return produto
