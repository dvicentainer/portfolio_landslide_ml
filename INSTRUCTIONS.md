# 📋 GUIA DE EXECUÇÃO - Landslide ML

## 🏔️ Análise de Susceptibilidade a Deslizamentos de Terra

**Autor:** Denis Vicentainer  
**Email:** denisvicentainer@gmail.com  
**LinkedIn:** https://www.linkedin.com/in/denis-augusto-vicentainer-726832138/

---

## 🎯 **VISÃO GERAL**

Este projeto implementa modelos de machine learning para análise de susceptibilidade a deslizamentos de terra usando dados geoespaciais reais. O projeto inclui:

- ✅ **Análise de correlação de Spearman**
- ✅ **Análise VIF (multicolinearidade)**
- ✅ **3 modelos de ML** (Random Forest, SVM, Neural Network)
- ✅ **Análise de importância das features**
- ✅ **6 visualizações profissionais**

---

## 🚀 **OPÇÕES DE EXECUÇÃO**

### **🔥 OPÇÃO 1: Setup Automático (RECOMENDADO)**

#### **Windows:**
```bash
cd landslide_ml
setup_environment.bat
```

#### **Linux/Mac:**
```bash
cd landslide_ml
chmod +x setup_environment.sh
./setup_environment.sh
```

**O que o setup automático faz:**
- ✅ Verifica Python e dependências
- ✅ Cria ambiente virtual
- ✅ Instala todas as bibliotecas
- ✅ Testa funcionamento
- ✅ Executa verificação completa

---

### **⚙️ OPÇÃO 2: Setup Manual**

#### **1. Verificar Pré-requisitos**
```bash
# Verificar Python (3.8+ necessário)
python --version
# ou
python3 --version
```

#### **2. Criar Ambiente Virtual**
```bash
# Criar ambiente
python -m venv landslide_env

# Ativar ambiente
# Windows:
landslide_env\Scripts\activate

# Linux/Mac:
source landslide_env/bin/activate
```

#### **3. Instalar Dependências**
```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
```

#### **4. Verificar Instalação**
```bash
# Teste básico
python test_notebook.py

# Teste manual
python -c "import pandas, numpy, matplotlib, seaborn, sklearn, rasterio, statsmodels; print('✅ Tudo OK!')"
```

---

### **🔧 OPÇÃO 3: Conda (Se pip falhar)**

```bash
# Criar ambiente conda
conda create -n landslide python=3.9

# Ativar ambiente
conda activate landslide

# Instalar dependências via conda-forge
conda install -c conda-forge rasterio pandas numpy scikit-learn matplotlib seaborn statsmodels jupyter scipy

# Instalar dependências restantes via pip
pip install notebook ipykernel
```

---

## 📊 **COMO EXECUTAR A ANÁLISE**

### **🎯 OPÇÃO A: Notebook Interativo (RECOMENDADO)**

```bash
# 1. Ativar ambiente
# Windows: landslide_env\Scripts\activate
# Linux/Mac: source landslide_env/bin/activate

# 2. Iniciar Jupyter
jupyter notebook

# 3. Abrir notebook
# landslide_susceptibility_model_training.ipynb

# 4. Executar células sequencialmente
# Kernel > Restart & Run All
```

### **🚀 OPÇÃO B: Script Automático**

```bash
# 1. Ativar ambiente
# Windows: landslide_env\Scripts\activate
# Linux/Mac: source landslide_env/bin/activate

# 2. Executar análise completa
python run_analysis.py
```

---

## 📁 **ESTRUTURA DO PROJETO**

```
landslide_ml/
├── 📓 landslide_susceptibility_model_training.ipynb  # Notebook principal
├── 🐍 run_analysis.py                                # Script automático
├── 📋 requirements.txt                               # Dependências
├── 🔧 setup_environment.bat/.sh                      # Setup automático
├── 🧪 test_notebook.py                               # Teste de funcionamento
├── 📖 README.md                                      # Documentação
├── 📋 INSTRUCTIONS.md                                # Este guia
├── 📂 data/
│   └── 🗺️ composite_bands4.tif                      # Dados raster
└── 🖼️ images/                                       # Visualizações (geradas)
    ├── spearman_correlation_matrix.png
    ├── vif_analysis.png
    ├── class_distribution.png
    ├── model_comparison.png
    ├── roc_curves.png
    └── feature_importance_random_forest.png
```

---

## 🔍 **VERIFICAÇÃO E TESTES**

### **Teste Rápido:**
```bash
python test_notebook.py
```

### **Teste Manual das Bibliotecas:**
```bash
# Teste básico
python -c "import pandas; print('✅ Pandas OK')"
python -c "import numpy; print('✅ NumPy OK')"
python -c "import matplotlib; print('✅ Matplotlib OK')"
python -c "import seaborn; print('✅ Seaborn OK')"
python -c "import sklearn; print('✅ Scikit-learn OK')"

# Teste crítico
python -c "import rasterio; print('✅ Rasterio OK')"
python -c "import statsmodels; print('✅ Statsmodels OK')"
```

### **Verificar Dados:**
```bash
# Verificar se arquivo existe
ls -la data/composite_bands4.tif
# Windows: dir data\composite_bands4.tif
```

---

## ⚠️ **SOLUÇÃO DE PROBLEMAS**

### **❌ Problema: Rasterio não instala**

**Solução 1 - Instalação alternativa:**
```bash
pip install rasterio --no-binary rasterio
```

**Solução 2 - Instalar dependências do sistema:**
```bash
# Ubuntu/Debian:
sudo apt update
sudo apt install gdal-bin libgdal-dev

# CentOS/RHEL:
sudo yum install gdal gdal-devel

# macOS:
brew install gdal
```

**Solução 3 - Usar Conda:**
```bash
conda install -c conda-forge rasterio
```

### **❌ Problema: Python não encontrado**

**Windows:**
- Baixe Python 3.8+ de https://python.org
- Marque "Add Python to PATH" durante instalação

**Linux:**
```bash
# Ubuntu/Debian:
sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL:
sudo yum install python3 python3-pip
```

**macOS:**
```bash
# Com Homebrew:
brew install python3

# Ou baixe de https://python.org
```

### **❌ Problema: Jupyter não abre**

```bash
# Reinstalar Jupyter
pip uninstall jupyter notebook
pip install jupyter notebook

# Ou usar JupyterLab
pip install jupyterlab
jupyter lab
```

### **❌ Problema: Arquivo de dados não encontrado**

- Verifique se `data/composite_bands4.tif` existe
- Tamanho esperado: ~200-300 MB
- Se não tiver, solicite os dados originais

---

## 📊 **RESULTADOS ESPERADOS**

### **Métricas dos Modelos:**
- **AUC-ROC**: > 0.80 para todos os modelos
- **Acurácia**: 75-85%
- **F1-Score**: Balanceado entre precisão e recall

### **Visualizações Geradas:**
1. **Matriz de Correlação de Spearman** - Relacionamentos entre variáveis
2. **Análise VIF** - Detecção de multicolinearidade
3. **Distribuição das Classes** - Balanceamento dos dados
4. **Comparação de Modelos** - Performance comparativa
5. **Curvas ROC** - Capacidade discriminatória
6. **Importância das Features** - Ranking das variáveis

### **Top 3 Features Mais Importantes:**
1. **Slope (Declividade)** - Principal fator
2. **Elevation (Elevação)** - Influência significativa
3. **Características topográficas** - Curvaturas e índices

---

## 🆘 **SUPORTE**

### **Contato:**
- **📧 Email:** denisvicentainer@gmail.com
- **🔗 LinkedIn:** https://www.linkedin.com/in/denis-augusto-vicentainer-726832138/

### **Problemas Comuns:**
1. **Rasterio**: Use conda ou instalação alternativa
2. **Memória**: Reduza tamanho dos dados se necessário
3. **Jupyter**: Reinstale ou use JupyterLab
4. **Python**: Verifique versão 3.8+

### **Logs de Erro:**
- Salve mensagens de erro completas
- Inclua versão do Python e SO
- Mencione qual comando falhou

---

## ✅ **CHECKLIST DE EXECUÇÃO**

- [ ] Python 3.8+ instalado
- [ ] Arquivo `data/composite_bands4.tif` presente
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] Teste de funcionamento passou
- [ ] Jupyter notebook abre corretamente
- [ ] Todas as células executam sem erro
- [ ] 6 imagens geradas na pasta `images/`

---

**🎉 Pronto! Seu projeto está funcionando perfeitamente!**
