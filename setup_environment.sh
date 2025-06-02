#!/bin/bash

echo "========================================"
echo " SETUP AMBIENTE - LANDSLIDE ML"
echo " Autor: Denis Vicentainer"
echo " Email: denisvicentainer@gmail.com"
echo "========================================"

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Função para verificar Python
check_python() {
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        PYTHON_CMD="python"
    else
        echo "❌ Python não encontrado!"
        echo "   Instale Python 3.8+ usando:"
        echo "   - Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
        echo "   - CentOS/RHEL: sudo yum install python3 python3-pip"
        echo "   - macOS: brew install python3"
        exit 1
    fi
    
    echo "🔍 Verificando Python..."
    $PYTHON_CMD --version
}

# Verificar Python
check_python

echo ""
echo "📁 Verificando estrutura do projeto..."
if [ ! -f "data/composite_bands4.tif" ]; then
    echo "❌ Arquivo de dados não encontrado: data/composite_bands4.tif"
    echo "   Certifique-se de que os dados estão na pasta correta"
    exit 1
fi

echo ""
echo "🗂️ Criando diretórios necessários..."
mkdir -p images

if [ ! -d "landslide_env" ]; then
    echo "📦 Criando ambiente virtual..."
    $PYTHON_CMD -m venv landslide_env
else
    echo "✅ Ambiente virtual já existe"
fi

echo ""
echo "🔧 Ativando ambiente virtual..."
source landslide_env/bin/activate

echo ""
echo "⬆️ Atualizando pip..."
python -m pip install --upgrade pip

echo ""
echo "📚 Instalando dependências..."
pip install -r requirements.txt

echo ""
echo "🧪 Testando instalação..."
echo "   Testando bibliotecas principais..."
python -c "import pandas, numpy, matplotlib, seaborn, sklearn; print('✅ Bibliotecas principais OK')" || {
    echo "❌ Erro nas bibliotecas principais"
    exit 1
}

echo "   Testando rasterio..."
python -c "import rasterio; print('✅ Rasterio OK')" || {
    echo "⚠️ Rasterio com problemas"
    echo "   Tentando instalação alternativa..."
    pip install rasterio --no-binary rasterio
    python -c "import rasterio; print('✅ Rasterio OK (instalação alternativa)')" || {
        echo "❌ Rasterio falhou - use conda como alternativa:"
        echo "   conda create -n landslide python=3.9"
        echo "   conda activate landslide"
        echo "   conda install -c conda-forge rasterio pandas numpy scikit-learn matplotlib seaborn statsmodels jupyter"
    }
}

echo "   Testando statsmodels..."
python -c "import statsmodels; print('✅ Statsmodels OK')" || {
    echo "❌ Erro no statsmodels"
    exit 1
}

echo ""
echo "🎯 Executando teste completo..."
python test_notebook.py

echo ""
echo "========================================"
echo " 🎉 SETUP CONCLUÍDO COM SUCESSO!"
echo "========================================"
echo ""
echo "🚀 OPÇÕES DE EXECUÇÃO:"
echo ""
echo "  1. NOTEBOOK INTERATIVO (Recomendado):"
echo "     source landslide_env/bin/activate"
echo "     jupyter notebook landslide_susceptibility_model_training.ipynb"
echo ""
echo "  2. SCRIPT AUTOMÁTICO:"
echo "     source landslide_env/bin/activate"
echo "     python run_analysis.py"
echo ""
echo "  3. TESTE DE FUNCIONAMENTO:"
echo "     source landslide_env/bin/activate"
echo "     python test_notebook.py"
echo ""
echo "📧 Suporte: denisvicentainer@gmail.com"
echo "🔗 LinkedIn: https://www.linkedin.com/in/denis-augusto-vicentainer-726832138/"
echo ""
