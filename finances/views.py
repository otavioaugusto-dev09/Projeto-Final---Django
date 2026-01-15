# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Categoria, Movimentacao
from .forms import CategoriaForm, MovimentacaoForm
from django.contrib import messages
from .filters import MovimentacaoFilter
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.cache import never_cache
from django.db.models.functions import TruncMonth

@never_cache
@login_required
def listar_categorias(request):
    categorias = Categoria.objects.filter(usuario=request.user)
    return render(request, 'finances/listar_categorias.html', {'categorias': categorias})

@never_cache
@login_required
def criar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save(commit=False)
            categoria.usuario = request.user
            categoria.save()
            messages.success(request, "Categoria criada com sucesso!")
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()

    return render(request, 'finances/form_categoria.html', {'form': form})

@never_cache
@login_required
def editar_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id, usuario=request.user)

    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoria atualizada!")
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'finances/form_categoria.html', {'form': form})

@never_cache
@login_required
def excluir_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id, usuario=request.user)
    categoria.delete()
    messages.success(request, "Categoria removida!")
    return redirect('listar_categorias')

@never_cache
@login_required
def listar_movimentacoes(request):
    queryset = Movimentacao.objects.filter(usuario=request.user)

    filtro = MovimentacaoFilter(request.GET, queryset=queryset, request=request)
    movimentacoes = filtro.qs

    total_receitas = movimentacoes.filter(
        categoria__tipo='receita'
    ).aggregate(total=Sum('valor'))['total'] or 0

    total_despesas = movimentacoes.filter(
        categoria__tipo='despesa'
    ).aggregate(total=Sum('valor'))['total'] or 0

    saldo = total_receitas - total_despesas

    return render(request, 'finances/listar_movimentacoes.html', {
        'movimentacoes': movimentacoes,
        'filtro': filtro,
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'saldo': saldo,
    })

@never_cache
@login_required
def criar_movimentacao(request):
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.usuario = request.user
            movimentacao.save()
            return redirect('listar_movimentacoes')
    else:
        form = MovimentacaoForm(usuario=request.user)

    return render(request, 'finances/form_movimentacao.html', {
        'form': form,
        'titulo': 'Nova Movimentação'
    })

@never_cache
@login_required
def editar_movimentacao(request, id):
    movimentacao = get_object_or_404(
        Movimentacao, id=id, usuario=request.user
    )

    if request.method == 'POST':
        form = MovimentacaoForm(request.POST, instance=movimentacao)
        if form.is_valid():
            form.save()
            return redirect('listar_movimentacoes')
    else:
        form = MovimentacaoForm(instance=movimentacao)

    return render(request, 'finances/form_movimentacao.html', {
        'form': form,
        'titulo': 'Editar Movimentação'
    })

@never_cache
@login_required
def excluir_movimentacao(request, id):
    movimentacao = get_object_or_404(
        Movimentacao, id=id, usuario=request.user
    )

    if request.method == 'POST':
        movimentacao.delete()
        return redirect('listar_movimentacoes')

    return render(request, 'finances/confirmar_exclusao_movimentacao.html', {
        'movimentacao': movimentacao
    })

@never_cache
@login_required
def dashboard(request):
    usuario=request.user

    receitas = Movimentacao.objects.filter(
        usuario=request.user,
        categoria__tipo='receita'
    ).aggregate(total=Sum('valor'))['total'] or 0

    despesas = Movimentacao.objects.filter(
        usuario=request.user,
        categoria__tipo='despesa'
    ).aggregate(total=Sum('valor'))['total'] or 0

    saldo = receitas - despesas

    totais_por_categoria = (
        Movimentacao.objects
        .filter(usuario=usuario)
        .values('categoria__nome', 'categoria__tipo')
        .annotate(total=Sum('valor'))
    )
    
    return render(request, 'finances/dashboard.html', {
        'receitas': receitas,
        'despesas': despesas,
        'saldo': saldo,
        'totais_por_categoria': totais_por_categoria,
    })

@never_cache
@login_required
def info(request):
    return render(request, 'finances/info.html')