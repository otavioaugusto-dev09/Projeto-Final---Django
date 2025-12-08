from django.contrib import admin
from .models import Categoria, Movimentacao

# Register your models here.



@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'usuario')
    search_fields = ('nome',)
    list_filter = ('tipo', 'usuario')


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'categoria', 'usuario')
    list_filter = ('categoria', 'data', 'usuario')
    search_fields = ('descricao',)