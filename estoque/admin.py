from django.contrib import admin
from .models import Peca, Movimentacao, Fornecedor, Categoria
admin.site.register(Peca)
admin.site.register(Movimentacao)
admin.site.register(Fornecedor)
admin.site.register(Categoria)