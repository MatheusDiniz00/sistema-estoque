from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Movimentacao, Peca


class DesfazerMovimentacaoTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='senha-teste')
        self.client.force_login(self.user)
        self.peca = Peca.objects.create(
            nome='Tela de teste',
            modelo_celular='Modelo de teste',
            quantidade=3,
            preco_compra='50.00',
            preco_venda='100.00',
        )
        self.saida = Movimentacao.objects.create(
            peca=self.peca,
            tipo='SAIDA',
            quantidade_movimentada=2,
            preco_venda_no_momento='100.00',
        )

    def test_desfaz_saida_restaurando_estoque_e_preservando_filtro(self):
        response = self.client.post(
            reverse('desfazer_movimentacao', args=[self.saida.pk]),
            {'data_inicio': '2026-10-01', 'data_fim': '2026-10-27'},
        )

        self.peca.refresh_from_db()
        self.assertEqual(self.peca.quantidade, 5)
        self.assertFalse(Movimentacao.objects.filter(pk=self.saida.pk).exists())
        self.assertRedirects(
            response,
            '/relatorio/?data_inicio=2026-10-01&data_fim=2026-10-27',
            fetch_redirect_response=False,
        )

    def test_desfazer_aceita_apenas_post(self):
        response = self.client.get(
            reverse('desfazer_movimentacao', args=[self.saida.pk])
        )

        self.peca.refresh_from_db()
        self.assertEqual(response.status_code, 405)
        self.assertEqual(self.peca.quantidade, 3)
        self.assertTrue(Movimentacao.objects.filter(pk=self.saida.pk).exists())

    def test_nao_desfaz_uma_entrada(self):
        entrada = Movimentacao.objects.create(
            peca=self.peca,
            tipo='ENTRADA',
            quantidade_movimentada=4,
        )

        response = self.client.post(
            reverse('desfazer_movimentacao', args=[entrada.pk])
        )

        self.assertEqual(response.status_code, 404)
        self.peca.refresh_from_db()
        self.assertEqual(self.peca.quantidade, 3)
