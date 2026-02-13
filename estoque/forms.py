from django import forms
from django.contrib.auth.models import User
from .models import Peca, Movimentacao, Fornecedor, Categoria

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input w-full rounded-md border-gray-300 shadow-sm'}),
        }

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_staff']
        labels = {
            'username': 'Nome de Usuário',
            'is_active': 'Usuário Ativo (Pode logar)',
            'is_staff': 'Administrador (Acesso total)',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-indigo-600'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-indigo-600'}),
        }

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['nome', 'cnpj', 'telefone', 'email', 'observacao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-input'}),
            'telefone': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'observacao': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }

class PecaForm(forms.ModelForm):
    class Meta:
        model = Peca
        fields = ['nome', 'categoria', 'modelo_celular', 'quantidade', 'localizacao', 'preco_compra', 'preco_venda']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'modelo_celular': forms.TextInput(attrs={'class': 'form-input'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'localizacao': forms.TextInput(attrs={'class': 'form-input'}),
            'preco_compra': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
        }

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['peca', 'tipo', 'quantidade_movimentada', 'fornecedor', 'observacao']
        widgets = {
            'peca': forms.Select(attrs={
                'class': 'select2 form-select'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-select'
            }),
            'quantidade_movimentada': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': 1
            }),
            'fornecedor': forms.Select(attrs={
                'class': 'form-select'
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3
            }),
        }
