@echo off
echo ===========================================
echo Iniciando os servidores Flask...
echo ===========================================

:: Ativa o ambiente virtual
call venv\Scripts\activate

:: Inicia o app2.py na porta 5002 em uma nova janela
start "Servidor 1 - app2.py" cmd /k "python app2.py"

:: Inicia o app.py na porta 5001 em uma nova janela
start "Servidor 1 - app.py" cmd /k "python app.py"

:: Inicia o app3.py na porta 5003 em uma nova janela
start "Servidor 1 - app3.py" cmd /k "python app3.py"


echo.
echo Servidores iniciados com sucesso.
echo ===========================================
echo Pressione qualquer tecla para sair...
pause > nul
