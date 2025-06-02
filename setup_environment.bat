@echo off
echo ========================================
echo  SETUP AMBIENTE - LANDSLIDE ML
echo  Autor: Denis Vicentainer
echo  Email: denisvicentainer@gmail.com
echo ========================================

echo.
echo 🔍 Verificando Python...
python --version || (
    echo ❌ Python nao encontrado!
    echo    Instale Python 3.8+ de https://python.org
    pause
    exit /b 1
)

echo.
echo 📁 Verificando estrutura do projeto...
if not exist "data\composite_bands4.tif" (
    echo ❌ Arquivo de dados nao encontrado: data\composite_bands4.tif
    echo    Certifique-se de que os dados estao na pasta correta
    pause
    exit /b 1
)

echo.
echo 🗂️ Criando diretorios necessarios...
if not exist "images" mkdir images
if not exist "landslide_env" (
    echo 📦 Criando ambiente virtual...
    python -m venv landslide_env
) else (
    echo ✅ Ambiente virtual ja existe
)

echo.
echo 🔧 Ativando ambiente virtual...
call landslide_env\Scripts\activate.bat

echo.
echo ⬆️ Atualizando pip...
python -m pip install --upgrade pip

echo.
echo 📚 Instalando dependencias...
pip install -r requirements.txt

echo.
echo 🧪 Testando instalacao...
echo    Testando bibliotecas principais...
python -c "import pandas, numpy, matplotlib, seaborn, sklearn; print('✅ Bibliotecas principais OK')" || (
    echo ❌ Erro nas bibliotecas principais
    pause
    exit /b 1
)

echo    Testando rasterio...
python -c "import rasterio; print('✅ Rasterio OK')" || (
    echo ⚠️ Rasterio com problemas
    echo    Tentando instalacao alternativa...
    pip install rasterio --no-binary rasterio
    python -c "import rasterio; print('✅ Rasterio OK (instalacao alternativa)')" || (
        echo ❌ Rasterio falhou - use conda como alternativa
        echo    conda create -n landslide python=3.9
        echo    conda activate landslide
        echo    conda install -c conda-forge rasterio pandas numpy scikit-learn matplotlib seaborn statsmodels jupyter
    )
)

echo    Testando statsmodels...
python -c "import statsmodels; print('✅ Statsmodels OK')" || (
    echo ❌ Erro no statsmodels
    pause
    exit /b 1
)

echo.
echo 🎯 Executando teste completo...
python test_notebook.py

echo.
echo ========================================
echo  🎉 SETUP CONCLUIDO COM SUCESSO!
echo ========================================
echo.
echo 🚀 OPCOES DE EXECUCAO:
echo.
echo   1. NOTEBOOK INTERATIVO (Recomendado):
echo      landslide_env\Scripts\activate.bat
echo      jupyter notebook landslide_susceptibility_model_training.ipynb
echo.
echo   2. SCRIPT AUTOMATICO:
echo      landslide_env\Scripts\activate.bat
echo      python run_analysis.py
echo.
echo   3. TESTE DE FUNCIONAMENTO:
echo      landslide_env\Scripts\activate.bat
echo      python test_notebook.py
echo.
echo 📧 Suporte: denisvicentainer@gmail.com
echo 🔗 LinkedIn: https://www.linkedin.com/in/denis-augusto-vicentainer-726832138/
echo.
pause
