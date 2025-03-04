import uuid

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models as m
from django.db.models import Avg
from django.utils.text import slugify


class Categoria(m.Model):
    nome_categoria = m.CharField(max_length=30, null=False, unique=True,verbose_name='nome da categoria')


    def __str__(self) -> str:
        return self.nome_categoria


class Produto(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = m.CharField(max_length=150, null=False)
    preco = m.FloatField(null=False, verbose_name='preço')
    slug = m.SlugField(null=True, blank=True)
    descricao = m.TextField(null=False, verbose_name='descrição')
    promocao = m.PositiveIntegerField(default=0, verbose_name='promoção')
    categoria = m.ManyToManyField(Categoria)


    @property
    def total_avaliacoes(self):
        return self.avaliacoes.count()
    

    @property
    def avaliacoes_uma_estrelas(self):
        return self.avaliacoes.filter(avaliacao=1).count()
    

    @property
    def avaliacoes_duas_estrelas(self):
        return self.avaliacoes.filter(avaliacao=2).count()
    

    @property
    def avaliacoes_tres_estrelas(self):
        return self.avaliacoes.filter(avaliacao=3).count()
    

    @property
    def avaliacoes_quatro_estrelas(self):
        return self.avaliacoes.filter(avaliacao=4).count()
    

    @property
    def avaliacoes_cinco_estrelas(self):
        return self.avaliacoes.filter(avaliacao=5).count()


    @property
    def media_avaliacoes(self):
        media = self.avaliacoes.aggregate(media=Avg('avaliacao'))['media']
        return round(media, 1) if media is not None else 0.0


    def __str__(self) -> str:
        return self.nome
    

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.nome)
        return super().save(*args, **kwargs)
    

class Variacao(m.Model):
    produto = m.ForeignKey(Produto, on_delete=m.CASCADE, related_name='variacoes')
    nome_variacao = m.CharField(max_length=150, null=False, verbose_name='nome da variação')
    #TODO: remover null=True
    imagem_variacao = m.ImageField(upload_to='produtos/img', verbose_name='imagem da variação', null=True, blank=True)


    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'


    def __str__(self) -> str:
        return f'{self.produto.nome} {self.nome_variacao}'
    

class Especificacao(m.Model):
    variacao = m.ForeignKey(Variacao, on_delete=m.CASCADE, related_name='especificacoes')
    tamanho = m.CharField(max_length=2)
    estoque = m.PositiveIntegerField(default=0)


    class Meta:
        verbose_name = 'Especificação'
        verbose_name_plural = 'Especificações'


    def __str__(self) -> str:
        return f'tamanho: {self.tamanho}; estoque: {self.estoque}'


class Avaliacao(m.Model):
    produto = m.ForeignKey(Produto, on_delete=m.CASCADE, related_name='avaliacoes')
    #TODO: remover null=True
    pedido = m.ForeignKey('pedidos.Pedido', on_delete=m.CASCADE, null=True)
    variacao_nome = m.CharField(max_length=150, default='')
    avaliador = m.ForeignKey(User, on_delete=m.CASCADE)
    comentario = m.TextField(max_length=255, null=True, blank=True)
    avaliacao = m.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    criado_em = m.DateTimeField(auto_now_add=True)


    @property
    def foto_url(self):
        return self.avaliador.endereco.foto.url
    

    @property
    def nome_completo(self):
        return f'{self.avaliador.first_name} {self.avaliador.last_name}'


    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'


    def __str__(self):
        return f'{self.avaliador.username} - {self.produto.nome}'
