#!/usr/bin/env python3
"""
Script executável para análise de susceptibilidade a deslizamentos de terra
Executa todo o pipeline de análise automaticamente

Autor: Denis Vicentainer
Email: denisvicentainer@gmail.com
LinkedIn: https://www.linkedin.com/in/denis-augusto-vicentainer-726832138/
"""

import os
import sys
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Suprimir warnings
warnings.filterwarnings('ignore')

def setup_environment():
    """Configurar ambiente e verificar dependências"""
    print("🔧 Configurando ambiente...")
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('data/composite_bands4.tif'):
        print("❌ Erro: Execute este script no diretório landslide_ml")
        print("   O arquivo data/composite_bands4.tif não foi encontrado")
        return False
    
    # Criar diretório de imagens se não existir
    os.makedirs('images', exist_ok=True)
    
    # Configurar paleta de cores
    global colors
    colors = {
        'primary': '#2E86AB',      # Azul principal
        'secondary': '#A23B72',    # Rosa/roxo
        'accent': '#F18F01',       # Laranja
        'success': '#C73E1D',      # Vermelho
        'neutral': '#6C757D',      # Cinza
        'light': '#E9ECEF'         # Cinza claro
    }
    
    # Configurar estilo dos gráficos
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_palette([colors['primary'], colors['secondary'], colors['accent'], colors['success']])
    
    print("✅ Ambiente configurado com sucesso!")
    return True

def load_data():
    """Carregar e preparar dados"""
    print("\n📂 Carregando dados...")
    
    try:
        import rasterio
        
        file_path = 'data/composite_bands4.tif'
        band_names = ['aspect', 'elevation', 'geology', 'landslide_scars', 'ndvi',
                      'plan_curv', 'profile_curv', 'slope', 'spi', 'twi']
        
        with rasterio.open(file_path) as src:
            data = src.read()
            num_layers, height, width = data.shape
            
            print(f"📐 Dimensões do raster:")
            print(f"   - Bandas: {num_layers}")
            print(f"   - Altura: {height} pixels")
            print(f"   - Largura: {width} pixels")
            print(f"   - Total de pixels: {height * width:,}")
            
            # Reshape para formato tabular
            reshaped_data = data.reshape(num_layers, -1).T
            df = pd.DataFrame(reshaped_data, columns=band_names)
        
        print(f"✅ DataFrame criado: {df.shape}")
        return df, band_names
        
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return None, None

def clean_data(df):
    """Limpar e preparar dados"""
    print("\n🧹 Limpando dados...")
    
    # Converter tipos
    df['geology'] = df['geology'].astype(int)
    df['landslide_scars'] = df['landslide_scars'].astype(int)
    df['elevation'] = df['elevation'].astype(int)
    
    # Aplicar limpeza de outliers
    df.loc[~df['elevation'].between(-30, 942), 'elevation'] = np.nan
    df.loc[~df['aspect'].between(-1, 360), 'aspect'] = np.nan
    df.loc[df['geology'] < 0, 'geology'] = np.nan
    df.loc[df['landslide_scars'] < -1, 'landslide_scars'] = np.nan
    df.loc[~df['ndvi'].between(-1, 1), 'ndvi'] = np.nan
    df.loc[~df['plan_curv'].between(-8.04696, 6.0631), 'plan_curv'] = np.nan
    df.loc[~df['profile_curv'].between(-8.8354, 10.5086), 'profile_curv'] = np.nan
    df.loc[~df['slope'].between(0, 64.991), 'slope'] = np.nan
    df.loc[~df['spi'].between(-14.5964, 7.18534), 'spi'] = np.nan
    df.loc[~df['twi'].between(-6907.75, 12986.3), 'twi'] = np.nan
    
    # Remover linhas com valores ausentes
    df_clean = df.dropna()
    
    print(f"📊 Dados após limpeza: {df_clean.shape}")
    print(f"Dados removidos: {len(df) - len(df_clean):,} ({((len(df) - len(df_clean))/len(df)*100):.1f}%)")
    
    return df_clean

def run_analysis():
    """Executar análise completa"""
    print("🏔️ ANÁLISE DE SUSCEPTIBILIDADE A DESLIZAMENTOS")
    print("=" * 60)
    print("Autor: Denis Vicentainer")
    print("Email: denisvicentainer@gmail.com")
    print("=" * 60)
    
    # 1. Configurar ambiente
    if not setup_environment():
        return False
    
    # 2. Carregar dados
    df, band_names = load_data()
    if df is None:
        return False
    
    # 3. Limpar dados
    df_clean = clean_data(df)
    
    # 4. Criar variável target
    print("\n🎯 Criando variável target...")
    df_clean['ls'] = 0
    df_clean.loc[df_clean['landslide_scars'] != -1, 'ls'] = 1
    
    class_counts = df_clean['ls'].value_counts()
    print(f"Classe 0 (Não-deslizamento): {class_counts[0]:,}")
    print(f"Classe 1 (Deslizamento): {class_counts[1]:,}")
    
    # 5. Balancear dados
    print("\n⚖️ Balanceando dados...")
    from sklearn.utils import resample
    
    df_landslide = df_clean[df_clean['ls'] == 1]
    df_no_landslide = df_clean[df_clean['ls'] == 0]
    
    df_no_landslide_downsampled = resample(df_no_landslide,
                                           replace=False,
                                           n_samples=len(df_landslide),
                                           random_state=42)
    
    df_balanced = pd.concat([df_landslide, df_no_landslide_downsampled])
    df_balanced = df_balanced.sample(frac=1, random_state=42).reset_index(drop=True)
    
    print(f"✅ Dados balanceados: {df_balanced.shape}")
    
    # 6. Treinar modelos
    print("\n🤖 Treinando modelos...")
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import SVC
    from sklearn.neural_network import MLPClassifier
    from sklearn.metrics import accuracy_score, roc_auc_score
    
    feature_cols = ['aspect', 'elevation', 'geology', 'ndvi', 'plan_curv', 
                    'profile_curv', 'slope', 'spi', 'twi']
    
    X = df_balanced[feature_cols]
    y = df_balanced['ls']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Normalizar dados
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Treinar modelos
    models = {}
    
    # Random Forest
    print("   🌳 Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)
    rf_auc = roc_auc_score(y_test, rf.predict_proba(X_test)[:, 1])
    models['Random Forest'] = {'model': rf, 'auc': rf_auc, 'accuracy': accuracy_score(y_test, rf_pred)}
    
    # SVM
    print("   ⚡ SVM...")
    svm = SVC(random_state=42, probability=True)
    svm.fit(X_train_scaled, y_train)
    svm_pred = svm.predict(X_test_scaled)
    svm_auc = roc_auc_score(y_test, svm.predict_proba(X_test_scaled)[:, 1])
    models['SVM'] = {'model': svm, 'auc': svm_auc, 'accuracy': accuracy_score(y_test, svm_pred)}
    
    # Neural Network
    print("   🧠 Neural Network...")
    nn = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=1000, random_state=42)
    nn.fit(X_train_scaled, y_train)
    nn_pred = nn.predict(X_test_scaled)
    nn_auc = roc_auc_score(y_test, nn.predict_proba(X_test_scaled)[:, 1])
    models['Neural Network'] = {'model': nn, 'auc': nn_auc, 'accuracy': accuracy_score(y_test, nn_pred)}
    
    # 7. Resultados
    print("\n📊 RESULTADOS:")
    print("=" * 40)
    for name, info in models.items():
        print(f"{name:15s} - AUC: {info['auc']:.3f} | Accuracy: {info['accuracy']:.3f}")
    
    # Melhor modelo
    best_model = max(models.items(), key=lambda x: x[1]['auc'])
    print(f"\n🏆 MELHOR MODELO: {best_model[0]} (AUC: {best_model[1]['auc']:.3f})")
    
    # 8. Importância das features (Random Forest)
    print("\n🎯 IMPORTÂNCIA DAS FEATURES:")
    print("=" * 40)
    importances = rf.feature_importances_
    feature_importance = pd.DataFrame({
        'Feature': feature_cols,
        'Importance': importances
    }).sort_values('Importance', ascending=False)
    
    for i, (_, row) in enumerate(feature_importance.iterrows(), 1):
        print(f"{i:2d}. {row['Feature']:15s} - {row['Importance']:.4f}")
    
    print(f"\n✅ Análise concluída!")
    print(f"📊 Para visualizações detalhadas, execute o notebook:")
    print(f"   jupyter notebook landslide_susceptibility_model_training.ipynb")
    
    return True

if __name__ == "__main__":
    try:
        success = run_analysis()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Análise interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro durante a análise: {e}")
        sys.exit(1)
