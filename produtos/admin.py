from django.contrib import admin
from .models import Produto, Variacao, Categoria, Especificacao, Avaliacao


class VariacaoInline(admin.TabularInline):
    model = Variacao
    extra = 1


class EspecificacaoInline(admin.TabularInline):
    model = Especificacao
    extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    inlines = [VariacaoInline]
    list_display = ['nome']


class VariacaoAdmin(admin.ModelAdmin):
    inlines = [EspecificacaoInline]
    list_display = ['nome_variacao']


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao, VariacaoAdmin)
admin.site.register(Categoria)
admin.site.register(Especificacao)
admin.site.register(Avaliacao)
