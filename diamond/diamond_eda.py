import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime

# 한글 폰트 설정
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 이미지 폴더 생성
image_folder = 'images'
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# 마크다운 파일 저장
md_file = 'diamond_eda_report.md'

# 마크다운 쓰기를 위한 파일 핸들
md = open(md_file, 'w', encoding='utf-8')

def write_md(text):
    """마크다운 파일에 텍스트 쓰기"""
    md.write(text + '\n')

# ===== 데이터 로드 =====
diamonds = sns.load_dataset('diamonds')

# ===== 헤더 =====
write_md('# Diamond Dataset EDA Report\n')
write_md(f'**생성일**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')
write_md('\n## 목차\n')
write_md('1. [데이터 개요](#데이터-개요)\n')
write_md('2. [기초 기술통계](#기초-기술통계)\n')
write_md('3. [데이터 시각화](#데이터-시각화)\n')

# ===== 1. 데이터 개요 =====
write_md('\n---\n')
write_md('## 데이터 개요\n')
write_md(f'**데이터 크기**: {diamonds.shape[0]} rows × {diamonds.shape[1]} columns\n')
write_md(f'\n**컬럼 정보**:\n')
write_md('```\n')
write_md(str(diamonds.info()))
write_md('\n```\n')

write_md('\n**처음 5개 행**:\n')
write_md(diamonds.head().to_markdown(index=True))
write_md('\n')

# ===== 2. 기초 기술통계 =====
write_md('\n---\n')
write_md('## 기초 기술통계\n')

# 기술통계 1: 전체 수치형 데이터의 기술통계
write_md('\n### 기술통계 1: 전체 수치형 변수 기술통계\n')
descriptive_stats = diamonds.describe()
write_md(descriptive_stats.to_markdown())
write_md('\n')

# 기술통계 2: 카테고리형 변수의 빈도
write_md('\n### 기술통계 2: 카테고리형 변수 빈도\n')
categorical_cols = diamonds.select_dtypes(include=['object']).columns
for col in categorical_cols:
    write_md(f'\n**{col}의 빈도**:\n')
    write_md(diamonds[col].value_counts().to_frame().to_markdown())

# 기술통계 3: 결측치 확인
write_md('\n### 기술통계 3: 결측치 확인\n')
write_md(diamonds.isnull().sum().to_frame(name='결측치 개수').to_markdown())
write_md('\n')

# 기술통계 4: 상관계수 분석
write_md('\n### 기술통계 4: 수치형 변수 상관계수\n')
numeric_cols = diamonds.select_dtypes(include=[np.number]).columns
correlation_matrix = diamonds[numeric_cols].corr()
write_md(correlation_matrix.to_markdown())
write_md('\n')

# 기술통계 5: 그룹별 기술통계 (Cut 기준)
write_md('\n### 기술통계 5: Cut별 가격(price) 기술통계\n')
cut_price_stats = diamonds.groupby('cut')['price'].describe()
write_md(cut_price_stats.to_markdown())
write_md('\n')

# 기술통계 6: 그룹별 기술통계 (Color 기준)
write_md('\n### 기술통계 6: Color별 가격(price) 기술통계\n')
color_price_stats = diamonds.groupby('color')['price'].describe()
write_md(color_price_stats.to_markdown())
write_md('\n')

# ===== 3. 데이터 시각화 =====
write_md('\n---\n')
write_md('## 데이터 시각화\n')

# 시각화 1: Price 분포
write_md('\n### 시각화 1: 가격(Price) 분포\n')
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(diamonds['price'], kde=True, ax=ax, bins=50, color='steelblue')
ax.set_title('Distribution of Diamond Prices', fontsize=14, fontweight='bold')
ax.set_xlabel('Price ($)')
ax.set_ylabel('Frequency')
plt.tight_layout()
plt.savefig(f'{image_folder}/01_price_distribution.png', dpi=100, bbox_inches='tight')
plt.close()

write_md('![Price Distribution](images/01_price_distribution.png)\n')

# 시각화 1 기술통계
write_md('\n**기술통계 (Price 분포)**:\n')
price_stats = {
    '평균': diamonds['price'].mean(),
    '중앙값': diamonds['price'].median(),
    '표준편차': diamonds['price'].std(),
    '최솟값': diamonds['price'].min(),
    '최댓값': diamonds['price'].max(),
    '사분위수 25%': diamonds['price'].quantile(0.25),
    '사분위수 75%': diamonds['price'].quantile(0.75),
}
price_stats_df = pd.DataFrame(price_stats, index=['Value']).T
write_md(price_stats_df.to_markdown())
write_md('\n')

# 시각화 2: Cut별 Price 박스플롯
write_md('\n### 시각화 2: Cut별 가격 분포 (Box Plot)\n')
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=diamonds, x='cut', y='price', palette='Set2', ax=ax)
ax.set_title('Price Distribution by Cut Quality', fontsize=14, fontweight='bold')
ax.set_xlabel('Cut Quality')
ax.set_ylabel('Price ($)')
plt.tight_layout()
plt.savefig(f'{image_folder}/02_cut_price_boxplot.png', dpi=100, bbox_inches='tight')
plt.close()

write_md('![Price by Cut](images/02_cut_price_boxplot.png)\n')

# 시각화 2 기술통계 (교차표)
write_md('\n**기술통계 (Cut별 가격 요약)**:\n')
cut_price_pivot = diamonds.pivot_table(values='price', index='cut', aggfunc=['mean', 'median', 'std', 'count'])
write_md(cut_price_pivot.to_markdown())
write_md('\n')

# 시각화 3: Carat vs Price 산점도
write_md('\n### 시각화 3: Carat vs Price 산점도\n')
fig, ax = plt.subplots(figsize=(10, 6))
scatter = ax.scatter(diamonds['carat'], diamonds['price'], c=diamonds['depth'], 
                     cmap='viridis', alpha=0.5, s=10)
ax.set_title('Carat Weight vs Price (colored by Depth)', fontsize=14, fontweight='bold')
ax.set_xlabel('Carat Weight')
ax.set_ylabel('Price ($)')
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Depth')
plt.tight_layout()
plt.savefig(f'{image_folder}/03_carat_price_scatter.png', dpi=100, bbox_inches='tight')
plt.close()

write_md('![Carat vs Price](images/03_carat_price_scatter.png)\n')

# 시각화 3 기술통계 (Depth 그룹별)
write_md('\n**기술통계 (Depth 구간별 가격)**:\n')
diamonds_depth_binned = diamonds.copy()
diamonds_depth_binned['depth_range'] = pd.cut(diamonds_depth_binned['depth'], bins=5)
depth_pivot = diamonds_depth_binned.pivot_table(values='price', index='depth_range', aggfunc=['mean', 'median', 'count'])
write_md(depth_pivot.to_markdown())
write_md('\n')

# 시각화 4: Color별 가격 바차트
write_md('\n### 시각화 4: 다이아몬드 색상(Color)별 평균 가격\n')
fig, ax = plt.subplots(figsize=(10, 6))
color_price = diamonds.groupby('color')['price'].mean().sort_values(ascending=False)
color_price.plot(kind='bar', ax=ax, color='coral')
ax.set_title('Average Price by Diamond Color', fontsize=14, fontweight='bold')
ax.set_xlabel('Color Grade')
ax.set_ylabel('Average Price ($)')
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{image_folder}/04_color_price_bar.png', dpi=100, bbox_inches='tight')
plt.close()

write_md('![Price by Color](images/04_color_price_bar.png)\n')

# 시각화 4 기술통계 (색상별)
write_md('\n**기술통계 (Color별 가격 요약)**:\n')
color_pivot = diamonds.pivot_table(values='price', index='color', aggfunc=['mean', 'median', 'std', 'min', 'max'])
write_md(color_pivot.to_markdown())
write_md('\n')

# 시각화 5: Clarity별 빈도 및 평균 가격 히트맵
write_md('\n### 시각화 5: Cut과 Clarity별 평균 가격 히트맵\n')
fig, ax = plt.subplots(figsize=(10, 6))
heatmap_data = diamonds.pivot_table(values='price', index='clarity', columns='cut', aggfunc='mean')
sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Average Price ($)'})
ax.set_title('Average Price by Cut and Clarity', fontsize=14, fontweight='bold')
ax.set_xlabel('Cut Quality')
ax.set_ylabel('Clarity Grade')
plt.tight_layout()
plt.savefig(f'{image_folder}/05_cut_clarity_heatmap.png', dpi=100, bbox_inches='tight')
plt.close()

write_md('![Cut & Clarity Heatmap](images/05_cut_clarity_heatmap.png)\n')

# 시각화 5 기술통계 (히트맵 데이터)
write_md('\n**기술통계 (Cut & Clarity별 평균 가격 피봇 테이블)**:\n')
write_md(heatmap_data.to_markdown())
write_md('\n')

# 시각화 6: Carat 분포 (Cut별)
write_md('\n### 시각화 6: Cut별 Carat 무게 분포\n')
fig, ax = plt.subplots(figsize=(10, 6))
sns.violinplot(data=diamonds, x='cut', y='carat', palette='muted', ax=ax)
ax.set_title('Carat Weight Distribution by Cut', fontsize=14, fontweight='bold')
ax.set_xlabel('Cut Quality')
ax.set_ylabel('Carat Weight')
plt.tight_layout()
plt.savefig(f'{image_folder}/06_cut_carat_violin.png', dpi=100, bbox_inches='tight')
plt.close()

write_md('![Carat by Cut](images/06_cut_carat_violin.png)\n')

# 시각화 6 기술통계
write_md('\n**기술통계 (Cut별 Carat 무게 요약)**:\n')
carat_pivot = diamonds.pivot_table(values='carat', index='cut', aggfunc=['mean', 'median', 'std', 'min', 'max'])
write_md(carat_pivot.to_markdown())
write_md('\n')

# 시각화 7: Price와 Table 관계
write_md('\n### 시각화 7: Table 비율과 Price의 관계\n')
fig, ax = plt.subplots(figsize=(10, 6))
ax.hexbin(diamonds['table'], diamonds['price'], gridsize=30, cmap='YlOrRd', mincnt=1)
ax.set_title('Price vs Table Percentage (Hexbin Plot)', fontsize=14, fontweight='bold')
ax.set_xlabel('Table %')
ax.set_ylabel('Price ($)')
plt.colorbar(ax.collections[0], ax=ax, label='Count')
plt.tight_layout()
plt.savefig(f'{image_folder}/07_table_price_hexbin.png', dpi=100, bbox_inches='tight')
plt.close()

write_md('![Price vs Table](images/07_table_price_hexbin.png)\n')

# 시각화 7 기술통계
write_md('\n**기술통계 (Table 구간별 가격)**:\n')
diamonds_table_binned = diamonds.copy()
diamonds_table_binned['table_range'] = pd.cut(diamonds_table_binned['table'], bins=5)
table_pivot = diamonds_table_binned.pivot_table(values='price', index='table_range', aggfunc=['mean', 'median', 'count'])
write_md(table_pivot.to_markdown())
write_md('\n')

# 시각화 8: 상관계수 히트맵
write_md('\n### 시각화 8: 수치형 변수 상관계수 히트맵\n')
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
            ax=ax, square=True, cbar_kws={'label': 'Correlation'})
ax.set_title('Correlation Matrix of Numerical Variables', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(f'{image_folder}/08_correlation_heatmap.png', dpi=100, bbox_inches='tight')
plt.close()

write_md('![Correlation Matrix](images/08_correlation_heatmap.png)\n')

# 시각화 8 기술통계 (상관계수 값)
write_md('\n**기술통계 (상관계수 행렬)**:\n')
write_md(correlation_matrix.to_markdown())
write_md('\n')

# 시각화 9: 다이아몬드 속성별 개수 비교
write_md('\n### 시각화 9: Cut, Color, Clarity별 다이아몬드 개수\n')
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

diamonds['cut'].value_counts().plot(kind='bar', ax=axes[0], color='skyblue')
axes[0].set_title('Count by Cut', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Cut Quality')
axes[0].set_ylabel('Count')
axes[0].tick_params(axis='x', rotation=45)

diamonds['color'].value_counts().plot(kind='bar', ax=axes[1], color='lightcoral')
axes[1].set_title('Count by Color', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Color Grade')
axes[1].set_ylabel('Count')
axes[1].tick_params(axis='x', rotation=45)

diamonds['clarity'].value_counts().plot(kind='bar', ax=axes[2], color='lightgreen')
axes[2].set_title('Count by Clarity', fontsize=12, fontweight='bold')
axes[2].set_xlabel('Clarity Grade')
axes[2].set_ylabel('Count')
axes[2].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig(f'{image_folder}/09_categorical_counts.png', dpi=100, bbox_inches='tight')
plt.close()

write_md('![Categorical Counts](images/09_categorical_counts.png)\n')

# 시각화 9 기술통계
write_md('\n**기술통계 (Cut, Color, Clarity 빈도)**:\n')
write_md('\n*Cut별 개수*:\n')
write_md(diamonds['cut'].value_counts().to_frame(name='Count').to_markdown())
write_md('\n*Color별 개수*:\n')
write_md(diamonds['color'].value_counts().to_frame(name='Count').to_markdown())
write_md('\n*Clarity별 개수*:\n')
write_md(diamonds['clarity'].value_counts().to_frame(name='Count').to_markdown())
write_md('\n')

# 시각화 10: 다중 변수 관계 (Pair plot)
write_md('\n### 시각화 10: 주요 수치형 변수 Pair Plot\n')
sample_diamonds = diamonds.sample(n=500, random_state=42)  # 샘플링으로 성능 향상
pair_cols = ['carat', 'depth', 'table', 'price']
fig = plt.figure(figsize=(12, 10))
pd.plotting.scatter_matrix(sample_diamonds[pair_cols], alpha=0.5, figsize=(12, 10), diagonal='hist')
plt.tight_layout()
plt.savefig(f'{image_folder}/10_pair_plot.png', dpi=100, bbox_inches='tight')
plt.close()

write_md('![Pair Plot](images/10_pair_plot.png)\n')

# 시각화 10 기술통계
write_md('\n**기술통계 (주요 수치형 변수 상관관계)**:\n')
pair_corr = diamonds[pair_cols].corr()
write_md(pair_corr.to_markdown())
write_md('\n')

# ===== 최종 요약 =====
write_md('\n---\n')
write_md('## 주요 발견사항\n')
write_md(f'- **총 다이아몬드 개수**: {len(diamonds):,}개\n')
write_md(f'- **평균 가격**: ${diamonds["price"].mean():,.2f}\n')
write_md(f'- **가격 범위**: ${diamonds["price"].min():,} - ${diamonds["price"].max():,}\n')
write_md(f'- **평균 Carat 무게**: {diamonds["carat"].mean():.3f}\n')
write_md(f'- **가장 많은 Cut**: {diamonds["cut"].mode()[0]}\n')
write_md(f'- **가장 흔한 Color**: {diamonds["color"].mode()[0]}\n')
write_md(f'- **가장 흔한 Clarity**: {diamonds["clarity"].mode()[0]}\n')

write_md('\n---\n')
write_md('*Report generated automatically by Python EDA Script*\n')

# 파일 닫기
md.close()

print("✓ EDA 분석이 완료되었습니다!")
print(f"✓ 마크다운 파일: {md_file}")
print(f"✓ 시각화 이미지: {image_folder}/ (총 10개)")
print("\n생성된 파일:")
for img in sorted(os.listdir(image_folder)):
    print(f"  - {image_folder}/{img}")
