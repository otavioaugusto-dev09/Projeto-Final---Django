import django_filters
from .models import Movimentacao

class MovimentacaoFilter(django_filters.FilterSet):

    descricao = django_filters.CharFilter(
        field_name='descricao',
        lookup_expr='icontains',
        label='Descrição'
    )

    valor__gte = django_filters.NumberFilter(
        field_name='valor',
        lookup_expr='gte',
        label='Valor mínimo'
    )

    valor__lte = django_filters.NumberFilter(
        field_name='valor',
        lookup_expr='lte',
        label='Valor máximo'
    )

    categoria = django_filters.ModelChoiceFilter(
        queryset=Movimentacao.objects.none(),  # corrigimos já já
        label='Categoria'
    )

    data = django_filters.DateFromToRangeFilter(
        label='Período'
    )

    class Meta:
        model = Movimentacao
        fields = []
    
    def __init__(self, *args, **kwargs):
        user = kwargs['request'].user
        super().__init__(*args, **kwargs)
        self.filters['categoria'].queryset = user.categoria_set.all()
