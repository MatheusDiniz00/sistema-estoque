@echo off
:: ==========================================
:: INICIAR SISTEMA DE ESTOQUE
:: ==========================================

echo Iniciando o servidor...
echo Por favor, NAO FECHE esta janela enquanto usar o sistema.
echo Para sair, basta fechar esta janela.

:: 1. Navega para a pasta do projeto (Caminho que você mandou nos prints)
cd /d "c:\Users\conse\OneDrive\Documents\SistemaEstoque"

:: 2. Ativa o ambiente virtual
call venv\Scripts\activate

:: 3. Abre o navegador automaticamente após 3 segundos
timeout /t 3 >nul
start http://127.0.0.1:8000/

:: 4. Inicia o servidor Django
python manage.py runserver

pause