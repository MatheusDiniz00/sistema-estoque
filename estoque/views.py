from django.shortcuts import render, redirect, get_object_or_404
from .models import Peca, Movimentacao, Fornecedor, Categoria
from .forms import PecaForm, MovimentacaoForm, FornecedorForm, UsuarioForm, CategoriaForm
from django.contrib import messages
from django.db import transaction
from django.db.models import Q, Sum, F
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# --- Gestão de Usuários ---
@login_required
def listar_usuarios(request):
    usuarios = User.objects.all()
    contexto = {'titulo': 'Usuários do Sistema', 'usuarios': usuarios}
    return render(request, 'estoque/lista_usuarios.html', contexto)

@login_required
def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Novo usuário registrado com sucesso!')
            return redirect('listar_usuarios')
    else:
        form = UserCreationForm()
    
    contexto = {'titulo': 'Registrar Novo Usuário', 'form': form}
    return render(request, 'registration/registro_usuario.html', contexto)

@login_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dados do usuário atualizados!')
            return redirect('listar_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    
    contexto = {'titulo': f'Editar Usuário: {usuario.username}', 'form': form}
    return render(request, 'estoque/form_usuario.html', contexto)

@login_required
def deletar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if usuario == request.user:
        messages.error(request, 'Não pode apagar o seu próprio usuário!')
        return redirect('listar_usuarios')

    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuário apagado com sucesso!')
        return redirect('listar_usuarios')
    
    contexto = {'titulo': 'Apagar Usuário', 'usuario': usuario}
    return render(request, 'estoque/confirmar_delecao_usuario.html', contexto)

# --- Gestão de Categorias (NOVO) ---
@login_required
def listar_categorias(request):
    categorias = Categoria.objects.all()
    contexto = {'titulo': 'Gestão de Categorias', 'categorias': categorias}
    return render(request, 'estoque/lista_categorias.html', contexto)

@login_required
def adicionar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria cadastrada com sucesso!')
            return redirect('listar_categorias')
    else:
        form = CategoriaForm()
    contexto = {'titulo': 'Nova Categoria', 'form': form}
    return render(request, 'estoque/form_categoria.html', contexto)

@login_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    contexto = {'titulo': f'Editar: {categoria.nome}', 'form': form}
    return render(request, 'estoque/form_categoria.html', contexto)

# --- Views de Fornecedor ---
@login_required
def listar_fornecedores(request):
    fornecedores = Fornecedor.objects.all()
    contexto = {'titulo': 'Gestão de Fornecedores', 'fornecedores': fornecedores}
    return render(request, 'estoque/lista_fornecedores.html', contexto)

@login_required
def adicionar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor cadastrado com sucesso!')
            return redirect('listar_fornecedores')
    else:
        form = FornecedorForm()
    contexto = {'titulo': 'Novo Fornecedor', 'form': form}
    return render(request, 'estoque/form_fornecedor.html', contexto)

@login_required
def editar_fornecedor(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor atualizado com sucesso!')
            return redirect('listar_fornecedores')
    else:
        form = FornecedorForm(instance=fornecedor)
    contexto = {'titulo': f'Editar: {fornecedor.nome}', 'form': form}
    return render(request, 'estoque/form_fornecedor.html', contexto)

# --- Views Principais ---
@login_required
def dashboard(request):
    total_modelos = Peca.objects.count()
    total_itens_estoque = Peca.objects.aggregate(Sum('quantidade'))['quantidade__sum'] or 0
    hoje = timezone.now().date()
    saidas_hoje = Movimentacao.objects.filter(data_movimentacao__date=hoje, tipo='SAIDA').aggregate(Sum('quantidade_movimentada'))['quantidade_movimentada__sum'] or 0
    valor_custo_total = Peca.objects.aggregate(total=Sum(F('preco_compra') * F('quantidade')))['total'] or 0
    pecas_baixo_estoque = Peca.objects.filter(quantidade__lt=5).order_by('quantidade')[:5]
    
    contexto = {
        'titulo': 'Dashboard Operacional',
        'total_modelos': total_modelos,
        'total_itens_estoque': total_itens_estoque,
        'saidas_hoje': saidas_hoje,
        'valor_custo_total': valor_custo_total,
        'pecas_baixo_estoque': pecas_baixo_estoque,
    }
    return render(request, 'estoque/dashboard.html', contexto)

@login_required
def listar_pecas(request):
    query = request.GET.get('q')
    categoria_id = request.GET.get('categoria')
    pecas = Peca.objects.all().order_by('nome')
    if query:
        pecas = pecas.filter(Q(nome__icontains=query) | Q(modelo_celular__icontains=query))
    if categoria_id:
        pecas = pecas.filter(categoria_id=categoria_id)
    categorias = Categoria.objects.all()
    contexto = {
        'titulo': 'Controle de Estoque de Peças', 
        'pecas': pecas, 
        'query': query,
        'categorias': categorias,
        'filtro_ativo': int(categoria_id) if categoria_id else None
    }
    return render(request, 'estoque/lista_pecas.html', contexto)

@login_required
def adicionar_peca(request):
    if request.method == 'POST':
        form = PecaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Peça cadastrada com sucesso!')
            return redirect('lista_pecas')
    else:
        form = PecaForm()
    contexto = {'titulo': 'Cadastrar Nova Peça', 'form': form}
    return render(request, 'estoque/nova_peca.html', contexto)

@login_required
def editar_peca(request, pk):
    peca = get_object_or_404(Peca, pk=pk)
    if request.method == 'POST':
        form = PecaForm(request.POST, instance=peca)
        if form.is_valid():
            form.save()
            messages.success(request, 'Peça atualizada com sucesso!')
            return redirect('lista_pecas')
    else:
        form = PecaForm(instance=peca)
    contexto = {'titulo': f'Editar: {peca.nome}', 'form': form, 'peca': peca}
    return render(request, 'estoque/editar_peca.html', contexto)

@login_required
@transaction.atomic
def movimentar_estoque(request):
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            peca = movimentacao.peca
            quantidade = movimentacao.quantidade_movimentada
            if movimentacao.tipo == 'ENTRADA':
                peca.quantidade += quantidade
                messages.success(request, f'{quantidade}x de {peca.nome} adicionados ao estoque.')
            elif movimentacao.tipo == 'SAIDA':
                if peca.quantidade < quantidade:
                    messages.error(request, f'Erro: Não há {quantidade}x de {peca.nome} em estoque. Quantidade atual: {peca.quantidade}.')
                    return redirect('movimentar_estoque')
                peca.quantidade -= quantidade
                messages.success(request, f'{quantidade}x de {peca.nome} removidos do estoque.')

            peca.save()
            movimentacao.save()
            # MUDANÇA AQUI: Redireciona para o dashboard após sucesso
            return redirect('dashboard')
    else:
        form = MovimentacaoForm()
    contexto = {'titulo': 'Movimentação de Estoque', 'form': form}
    return render(request, 'estoque/movimentar_peca.html', contexto)

@login_required
def relatorio_movimentacoes(request):
    hoje = timezone.now().date()
    data_inicio = request.GET.get('data_inicio', hoje.strftime('%Y-%m-%d'))
    data_fim = request.GET.get('data_fim', hoje.strftime('%Y-%m-%d'))
    filtro_rapido = request.GET.get('filtro')
    if filtro_rapido == 'mes':
        data_inicio = hoje.replace(day=1).strftime('%Y-%m-%d')
        data_fim = hoje.strftime('%Y-%m-%d')
    movimentacoes = Movimentacao.objects.filter(
        data_movimentacao__date__range=[data_inicio, data_fim],
        tipo='SAIDA'
    ).order_by('-data_movimentacao')
    total_itens = movimentacoes.aggregate(Sum('quantidade_movimentada'))['quantidade_movimentada__sum'] or 0
    contexto = {
        'titulo': 'Relatório de Saídas',
        'movimentacoes': movimentacoes,
        'total_itens': total_itens,
        'data_inicio': data_inicio,
        'data_fim': data_fim
    }
    return render(request, 'estoque/relatorio.html', contexto)