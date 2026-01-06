
from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name='dashboard'),

    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/nova/', views.criar_categoria, name='criar_categoria'),
    path('categorias/editar/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('categorias/excluir/<int:id>/', views.excluir_categoria, name='excluir_categoria'),

    path('movimentacoes/', views.listar_movimentacoes, name='listar_movimentacoes'),
    path('movimentacoes/nova/', views.criar_movimentacao, name='criar_movimentacao'),
    path('movimentacoes/editar/<int:id>/', views.editar_movimentacao, name='editar_movimentacao'),
    path('movimentacoes/excluir/<int:id>/', views.excluir_movimentacao, name='excluir_movimentacao'),
]