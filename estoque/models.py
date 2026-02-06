from django.db import models

class Categoria(models.Model):
    """Ex: Tela, Bateria, Conector, Carcaça"""
    nome = models.CharField(max_length=50, unique=True)
    
    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Empresa/Fornecedor")
    cnpj = models.CharField(max_length=20, blank=True, null=True, verbose_name="CNPJ/CPF")
    telefone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    observacao = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Peca(models.Model):
    nome = models.CharField(max_length=100, unique=True, verbose_name="Nome da Peça")
    # Novo Campo de Categoria
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Categoria")
    
    modelo_celular = models.CharField(max_length=50, verbose_name="Modelo do Celular (Ex: iPhone 11)")
    quantidade = models.IntegerField(default=0)
    localizacao = models.CharField(max_length=50, blank=True, null=True, verbose_name="Localização (Prateleira, etc)")
    preco_compra = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Preço de Compra Unitário")
    preco_venda = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Preço Sugerido de Venda")
    
    class Meta:
        verbose_name = "Peça"
        verbose_name_plural = "Peças"
    
    def __str__(self):
        return f"{self.nome} ({self.modelo_celular})"

class Movimentacao(models.Model):
    TIPO_MOVIMENTACAO = (
        ('ENTRADA', 'Entrada (Compra/Recebimento)'),
        ('SAIDA', 'Saída (Venda/Uso em Serviço)'),
    )
    
    peca = models.ForeignKey(Peca, on_delete=models.CASCADE)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True)
    
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMENTACAO)
    quantidade_movimentada = models.IntegerField()
    data_movimentacao = models.DateTimeField(auto_now_add=True)
    observacao = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"
        
    def __str__(self):
        return f"[{self.data_movimentacao.strftime('%d/%m/%Y')}] {self.tipo} - {self.peca.nome}"