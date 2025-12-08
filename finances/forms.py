from django import forms
from .models import Categoria, Movimentacao

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'tipo']

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['valor', 'descricao', 'data', 'categoria']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'})
        }