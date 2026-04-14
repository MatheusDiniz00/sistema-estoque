from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('pecas/', views.listar_pecas, name='lista_pecas'), 
    path('nova/', views.adicionar_peca, name='adicionar_peca'),
    path('editar/<int:pk>/', views.editar_peca, name='editar_peca'),
    path('movimentar/', views.movimentar_estoque, name='movimentar_estoque'),
    path('relatorio/', views.relatorio_movimentacoes, name='relatorio'),
    path('deletar/<int:pk>/', views.deletar_peca, name='deletar_peca'),
    
    # Categorias
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('categorias/nova/', views.adicionar_categoria, name='adicionar_categoria'),
    path('categorias/editar/<int:pk>/', views.editar_categoria, name='editar_categoria'),

    # Fornecedores
    path('fornecedores/', views.listar_fornecedores, name='listar_fornecedores'),
    path('fornecedores/novo/', views.adicionar_fornecedor, name='adicionar_fornecedor'),
    path('fornecedores/editar/<int:pk>/', views.editar_fornecedor, name='editar_fornecedor'),

    # Usuários
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/novo/', views.registrar_usuario, name='registrar_usuario'),
    path('usuarios/editar/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/deletar/<int:pk>/', views.deletar_usuario, name='deletar_usuario'),
]