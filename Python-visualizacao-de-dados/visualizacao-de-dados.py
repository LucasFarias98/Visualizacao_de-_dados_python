
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import shutil

# ========================================
# 1. LIMPEZA TOTAL (NUNCA REPETE)
# ========================================
print("🧹 LIMPANDO ambiente...")
plt.close('all')  # Fecha todas janelas matplotlib

# Remove pasta results/
if os.path.exists('results'):
    shutil.rmtree('results')

# Remove PNGs antigos
for file in ['top10.png', 'america.png', 'continentes.png', '*.png']:
    if os.path.exists(file):
        os.remove(file)

print("✅ Limpeza OK!")

# ========================================
# 2. CONFIGURAÇÕES
# ========================================
plt.ion()
plt.style.use('default')
sns.set_theme(style='whitegrid')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['font.size'] = 12

print("🚀 Iniciando análise...")

# ========================================
# 3. CARREGAR DADOS
# ========================================
df = pd.read_csv('example-countries-pt.csv')
print(f"📊 {len(df)} países carregados")

print("\n🔍 TOP 5 DOS SEUS DADOS:")
print(df.nlargest(5, 'Population')[['Country (pt)', 'Population']].to_string(index=False))

# ========================================
# 4. GRÁFICO 1 - TOP 10 MUNDIAL
# ========================================
print("\n📈 GRÁFICO 1...")
top10 = df.nlargest(10, 'Population')[['Country (pt)', 'Population']]
top10_m = top10['Population'] / 1000000

plt.figure(figsize=(15, 10))
colors = ['gold' if 'Brasil' in str(nome).upper() else '#2E86AB' for nome in top10['Country (pt)']]
bars = plt.barh(range(len(top10)), top10_m, color=colors)

# Títulos e labels
plt.title('🥇 TOP 10 PAÍSES MAIS POPULOSOS\n(seus dados 2026)', fontsize=22, fontweight='bold', pad=20)
plt.xlabel('Milhões de Habitantes', fontsize=16, fontweight='bold')
plt.ylabel('Países', fontsize=14)

# Nomes no eixo Y
plt.yticks(range(len(top10)), top10['Country (pt)'], fontsize=12)

# Valores nas barras
for i, bar in enumerate(bars):
    plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
             f'{top10_m.iloc[i]:.1f}M', va='center', ha='left', fontweight='bold')

plt.tight_layout()
os.makedirs('results', exist_ok=True)
plt.savefig('results/top10.png', dpi=300, bbox_inches='tight')
plt.show(block=True)
print("✅ results/top10.png")

# ========================================
# 5. GRÁFICO 2 - AMÉRICA DO SUL
# ========================================
print("\n🌎 GRÁFICO 2...")
america_sul = df[df['Continent'] == 'South America'].sort_values('Population', ascending=False)
if len(america_sul) > 0:
    america_m = america_sul['Population'] / 1000000

    plt.figure(figsize=(12, 8))
    colors_sul = ['darkorange' if 'Brasil' in str(nome).upper() else 'lightgreen' for nome in america_sul['Country (pt)']]
    bars_sul = plt.barh(range(len(america_sul)), america_m, color=colors_sul)

    plt.title('🇧🇷 AMÉRICA DO SUL - População', fontsize=20, fontweight='bold', pad=20)
    plt.xlabel('Milhões de Habitantes', fontsize=15, fontweight='bold')
    plt.yticks(range(len(america_sul)), america_sul['Country (pt)'], fontsize=11)

    for i, bar in enumerate(bars_sul):
        plt.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                 f'{america_m.iloc[i]:.1f}M', va='center', ha='left', fontweight='bold')

    plt.tight_layout()
    plt.savefig('results/america.png', dpi=300, bbox_inches='tight')
    plt.show(block=True)
    print(f"✅ results/america.png ({len(america_sul)} países)")
else:
    print("❌ Nenhum país da América do Sul encontrado")

# ========================================
# 6. GRÁFICO 3 - CONTINENTES
# ========================================
print("\n🌍 GRÁFICO 3...")
continentes = df.groupby('Continent')['Population'].sum().sort_values(ascending=False)
continentes_b = continentes / 1000000000

plt.figure(figsize=(12, 7))
bars_c = plt.barh(continentes.index, continentes_b, color='#3498DB')

plt.title('🌎 POPULAÇÃO POR CONTINENTE', fontsize=20, fontweight='bold', pad=20)
plt.xlabel('Bilhões de Habitantes', fontsize=15, fontweight='bold')

for bar, valor in zip(bars_c, continentes_b):
    plt.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
             f'{valor:.2f}B', va='center', ha='left', fontweight='bold', fontsize=12)

plt.tight_layout()
plt.savefig('results/continentes.png', dpi=300, bbox_inches='tight')
plt.show(block=True)
print("✅ results/continentes.png")

# ========================================
# 7. BRASIL
# ========================================
brasil = df[df['Country (pt)'].str.contains('Brasil', case=False, na=False)]
if not brasil.empty:
    b = brasil.iloc[0]
    print(f"\n🇧🇷 BRASIL: {b['Population']/1e6:.0f}M habitantes")
    print(f"   Capital: {b['Capital']}")
else:
    print("\n❌ Brasil não encontrado")

# ========================================
# 8. SALVAR DADOS
# ========================================
top10.to_csv('results/top10.csv', index=False)
df.to_csv('results/dados.csv', index=False)
print(f"\n🎉 CONCLUÍDO!")
print("📁 results/ contém:")
print("   🖼️ top10.png")
print("   🖼️ america.png")
print("   🖼️ continentes.png")
print("   📊 top10.csv")
print("   📊 dados.csv")
