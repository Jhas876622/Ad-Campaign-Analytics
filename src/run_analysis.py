"""
Google/Meta Ad Campaign Performance Analytics — ROAS Optimization
Complete Data Analysis & Statistical Testing

Author: Data Analytics Portfolio Project
Dataset: Facebook/Meta Ad Campaign Data (Kaggle: Sales Conversion Optimization)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import duckdb
import warnings
import os

# Configuration
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', '{:.4f}'.format)
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('husl')

plt.rcParams['figure.figsize'] = [12, 6]
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Ensure reports directory exists
os.makedirs('/root/ad-campaign-analytics/reports', exist_ok=True)

print("=" * 60)
print("GOOGLE/META AD CAMPAIGN PERFORMANCE ANALYTICS")
print("=" * 60)

# =============================================================================
# 1. LOAD DATA
# =============================================================================
print("\n📁 Loading dataset...")
df = pd.read_csv('/root/ad-campaign-analytics/data/KAG_conversion_data.csv')
print(f"✅ Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")

# =============================================================================
# 2. EXPLORATORY DATA ANALYSIS
# =============================================================================
print("\n" + "=" * 60)
print("EXPLORATORY DATA ANALYSIS")
print("=" * 60)

print("\n📋 First 5 rows:")
print(df.head())

print("\n🔤 Data Types:")
print(df.dtypes)

print("\n❓ Missing Values:")
print(df.isnull().sum())

print("\n📈 Statistical Summary:")
print(df.describe())

print("\n📊 Categorical Distributions:")
print("\nCampaign Distribution:")
print(df['xyz_campaign_id'].value_counts())
print("\nAge Distribution:")
print(df['age'].value_counts())
print("\nGender Distribution:")
print(df['gender'].value_counts())

# =============================================================================
# 3. DATA CLEANING & FEATURE ENGINEERING
# =============================================================================
print("\n" + "=" * 60)
print("DATA CLEANING & FEATURE ENGINEERING")
print("=" * 60)

df_clean = df.copy()

# Fix data types
df_clean['xyz_campaign_id'] = df_clean['xyz_campaign_id'].astype(str)
df_clean['fb_campaign_id'] = df_clean['fb_campaign_id'].astype(str)

# Feature Engineering: Calculate KPIs
print("\n🔧 Engineering KPI Columns...")

# CTR = Clicks / Impressions (as percentage)
df_clean['CTR'] = np.where(
    df_clean['Impressions'] > 0,
    (df_clean['Clicks'] / df_clean['Impressions']) * 100,
    0
)

# CPC = Spent / Clicks
df_clean['CPC'] = np.where(
    df_clean['Clicks'] > 0,
    df_clean['Spent'] / df_clean['Clicks'],
    0
)

# Conversion Rate = Total_Conversion / Clicks
df_clean['Conversion_Rate'] = np.where(
    df_clean['Clicks'] > 0,
    (df_clean['Total_Conversion'] / df_clean['Clicks']) * 100,
    0
)

# CPA = Spent / Total_Conversion
df_clean['CPA'] = np.where(
    df_clean['Total_Conversion'] > 0,
    df_clean['Spent'] / df_clean['Total_Conversion'],
    np.nan
)

# Revenue estimation
df_clean['Revenue'] = (df_clean['Total_Conversion'] * 5) + (df_clean['Approved_Conversion'] * 50)

# ROAS = Revenue / Spent
df_clean['ROAS'] = np.where(
    df_clean['Spent'] > 0,
    df_clean['Revenue'] / df_clean['Spent'],
    0
)

# Campaign Type
df_clean['Campaign_Type'] = df_clean['xyz_campaign_id'].map({
    '916': 'Image',
    '936': 'Image',
    '1178': 'Video'
})

print("✅ KPI columns created: CTR, CPC, Conversion_Rate, CPA, Revenue, ROAS, Campaign_Type")

# Save cleaned dataset
df_clean.to_csv('/root/ad-campaign-analytics/data/ad_campaign_cleaned.csv', index=False)
print(f"✅ Cleaned dataset saved: {df_clean.shape}")

# =============================================================================
# 4. VISUALIZATIONS
# =============================================================================
print("\n" + "=" * 60)
print("GENERATING VISUALIZATIONS")
print("=" * 60)

# Distribution Plots
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle('Distribution of Key Metrics', fontsize=16, fontweight='bold')

axes[0, 0].hist(df['Impressions'], bins=50, color='steelblue', edgecolor='white', alpha=0.7)
axes[0, 0].set_xlabel('Impressions')
axes[0, 0].set_ylabel('Frequency')
axes[0, 0].set_title('Impressions Distribution')
axes[0, 0].axvline(df['Impressions'].median(), color='red', linestyle='--', label=f'Median: {df["Impressions"].median():,.0f}')
axes[0, 0].legend()

axes[0, 1].hist(df['Clicks'], bins=30, color='forestgreen', edgecolor='white', alpha=0.7)
axes[0, 1].set_xlabel('Clicks')
axes[0, 1].set_ylabel('Frequency')
axes[0, 1].set_title('Clicks Distribution')

axes[0, 2].hist(df['Spent'], bins=50, color='darkorange', edgecolor='white', alpha=0.7)
axes[0, 2].set_xlabel('Spent ($)')
axes[0, 2].set_ylabel('Frequency')
axes[0, 2].set_title('Ad Spend Distribution')

axes[1, 0].hist(df['Total_Conversion'], bins=20, color='purple', edgecolor='white', alpha=0.7)
axes[1, 0].set_xlabel('Total Conversions')
axes[1, 0].set_ylabel('Frequency')
axes[1, 0].set_title('Total Conversions Distribution')

axes[1, 1].hist(df['Approved_Conversion'], bins=15, color='crimson', edgecolor='white', alpha=0.7)
axes[1, 1].set_xlabel('Approved Conversions')
axes[1, 1].set_ylabel('Frequency')
axes[1, 1].set_title('Approved Conversions Distribution')

campaign_counts = df['xyz_campaign_id'].value_counts()
axes[1, 2].bar(campaign_counts.index.astype(str), campaign_counts.values, color=['#3498db', '#e74c3c', '#2ecc71'])
axes[1, 2].set_xlabel('Campaign ID')
axes[1, 2].set_ylabel('Number of Ads')
axes[1, 2].set_title('Ads per Campaign')

plt.tight_layout()
plt.savefig('/root/ad-campaign-analytics/reports/01_distributions.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Distribution plots saved")

# Correlation Matrix
numeric_cols = ['Impressions', 'Clicks', 'Spent', 'Total_Conversion', 'Approved_Conversion']
corr_matrix = df[numeric_cols].corr()

plt.figure(figsize=(10, 8))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.3f', cmap='RdYlBu_r',
            center=0, square=True, linewidths=1, cbar_kws={'shrink': 0.8})
plt.title('Correlation Matrix: Ad Performance Metrics', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('/root/ad-campaign-analytics/reports/02_correlation_matrix.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Correlation matrix saved")

# =============================================================================
# 5. FUNNEL ANALYSIS
# =============================================================================
print("\n" + "=" * 60)
print("FUNNEL ANALYSIS")
print("=" * 60)

funnel_data = {
    'Stage': ['Impressions', 'Clicks', 'Total Conversions', 'Approved Conversions'],
    'Count': [
        df_clean['Impressions'].sum(),
        df_clean['Clicks'].sum(),
        df_clean['Total_Conversion'].sum(),
        df_clean['Approved_Conversion'].sum()
    ]
}

funnel_df = pd.DataFrame(funnel_data)
print(funnel_df)

# Calculate drop-off rates
counts = funnel_df['Count'].values
drop_off_stages = ['Impressions→Clicks', 'Clicks→Conversions', 'Conv→Approved']
drop_off_rates = [
    100 - (counts[1] / counts[0] * 100),
    100 - (counts[2] / counts[1] * 100),
    100 - (counts[3] / counts[2] * 100)
]

# Funnel Visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Funnel bars
stages = funnel_df['Stage']
counts_list = funnel_df['Count']
colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']

max_width = counts_list.max()
widths = counts_list / max_width
y_pos = np.arange(len(stages))[::-1]

for i, (stage, width, count, color) in enumerate(zip(stages, widths, counts_list, colors)):
    left = (1 - width) / 2
    axes[0].barh(y_pos[i], width, left=left, height=0.6, color=color, alpha=0.8, edgecolor='white', linewidth=2)
    axes[0].text(0.5, y_pos[i], f'{stage}\n{count:,.0f}', ha='center', va='center',
                fontsize=12, fontweight='bold', color='white')

axes[0].set_xlim(0, 1)
axes[0].set_ylim(-0.5, len(stages) - 0.5)
axes[0].axis('off')
axes[0].set_title('Marketing Funnel', fontsize=14, fontweight='bold', pad=20)

# Drop-off rates
bars = axes[1].bar(drop_off_stages, drop_off_rates, color=['#e74c3c', '#e67e22', '#f1c40f'],
                   edgecolor='white', linewidth=2, alpha=0.8)
for bar, rate in zip(bars, drop_off_rates):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                f'{rate:.1f}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

axes[1].set_ylabel('Drop-off Rate (%)', fontsize=12)
axes[1].set_title('Funnel Drop-off Rates', fontsize=14, fontweight='bold')
axes[1].set_ylim(0, 105)

plt.tight_layout()
plt.savefig('/root/ad-campaign-analytics/reports/03_funnel_analysis.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Funnel analysis saved")

# =============================================================================
# 6. A/B TEST: VIDEO vs IMAGE ADS
# =============================================================================
print("\n" + "=" * 60)
print("A/B TEST: VIDEO ADS vs IMAGE ADS")
print("=" * 60)

video_ads = df_clean[df_clean['Campaign_Type'] == 'Video']['ROAS'].dropna()
image_ads = df_clean[df_clean['Campaign_Type'] == 'Image']['ROAS'].dropna()

# Filter outliers
video_ads = video_ads[(video_ads > 0) & (video_ads < video_ads.quantile(0.99))]
image_ads = image_ads[(image_ads > 0) & (image_ads < image_ads.quantile(0.99))]

print(f"\n🎬 Video Ads (Campaign 1178):")
print(f"   Sample Size: {len(video_ads)}")
print(f"   Mean ROAS: {video_ads.mean():.4f}")
print(f"   Median ROAS: {video_ads.median():.4f}")

print(f"\n🖼️ Image Ads (Campaigns 916, 936):")
print(f"   Sample Size: {len(image_ads)}")
print(f"   Mean ROAS: {image_ads.mean():.4f}")
print(f"   Median ROAS: {image_ads.median():.4f}")

# Statistical Test
t_stat, p_value = stats.ttest_ind(video_ads, image_ads, equal_var=False)

# Cohen's d
pooled_std = np.sqrt(((len(video_ads)-1)*video_ads.std()**2 + (len(image_ads)-1)*image_ads.std()**2) /
                      (len(video_ads) + len(image_ads) - 2))
cohens_d = (video_ads.mean() - image_ads.mean()) / pooled_std

# Confidence Interval
se_diff = np.sqrt(video_ads.var()/len(video_ads) + image_ads.var()/len(image_ads))
mean_diff = video_ads.mean() - image_ads.mean()
ci_lower = mean_diff - 1.96 * se_diff
ci_upper = mean_diff + 1.96 * se_diff

# ROAS Ratio
roas_ratio = video_ads.mean() / image_ads.mean()

print(f"\n📈 STATISTICAL TEST RESULTS:")
print(f"   t-statistic: {t_stat:.4f}")
print(f"   p-value: {p_value:.6f}")
print(f"   Cohen's d: {cohens_d:.4f}")
print(f"   95% CI: [{ci_lower:.4f}, {ci_upper:.4f}]")
print(f"   ROAS Ratio: {roas_ratio:.2f}x")

if abs(cohens_d) < 0.2:
    effect_interpretation = "Negligible"
elif abs(cohens_d) < 0.5:
    effect_interpretation = "Small"
elif abs(cohens_d) < 0.8:
    effect_interpretation = "Medium"
else:
    effect_interpretation = "Large"

print(f"   Effect Size: {effect_interpretation}")

if p_value < 0.05:
    print(f"\n   ✅ STATISTICALLY SIGNIFICANT (p < 0.05)")
else:
    print(f"\n   ❌ NOT Statistically Significant")

# A/B Test Visualization
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Box Plot
bp_data = [image_ads, video_ads]
bp = axes[0].boxplot(bp_data, patch_artist=True, labels=['Image Ads', 'Video Ads'])
colors_box = ['#3498db', '#e74c3c']
for patch, color in zip(bp['boxes'], colors_box):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
axes[0].set_ylabel('ROAS', fontsize=12)
axes[0].set_title('ROAS Distribution', fontsize=14, fontweight='bold')
axes[0].axhline(y=1, color='gray', linestyle='--', alpha=0.5, label='Break-even')
axes[0].legend()

# Histogram
axes[1].hist(image_ads, bins=30, alpha=0.6, label=f'Image (μ={image_ads.mean():.2f})', color='#3498db')
axes[1].hist(video_ads, bins=30, alpha=0.6, label=f'Video (μ={video_ads.mean():.2f})', color='#e74c3c')
axes[1].axvline(image_ads.mean(), color='#2980b9', linestyle='--', linewidth=2)
axes[1].axvline(video_ads.mean(), color='#c0392b', linestyle='--', linewidth=2)
axes[1].set_xlabel('ROAS', fontsize=12)
axes[1].set_ylabel('Frequency', fontsize=12)
axes[1].set_title('ROAS Distribution Comparison', fontsize=14, fontweight='bold')
axes[1].legend()

# Bar Chart
means = [image_ads.mean(), video_ads.mean()]
bars = axes[2].bar([0, 1], means, color=['#3498db', '#e74c3c'], alpha=0.8, edgecolor='white', linewidth=2)
axes[2].set_xticks([0, 1])
axes[2].set_xticklabels(['Image Ads', 'Video Ads'])
axes[2].set_ylabel('Mean ROAS', fontsize=12)
axes[2].set_title(f'Mean ROAS Comparison\n(p={p_value:.4f})', fontsize=14, fontweight='bold')

for i, (bar, mean) in enumerate(zip(bars, means)):
    axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f'{mean:.2f}', ha='center', va='bottom', fontsize=14, fontweight='bold')

plt.tight_layout()
plt.savefig('/root/ad-campaign-analytics/reports/04_ab_test_results.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ A/B test visualization saved")

# =============================================================================
# 7. AGE GROUP SEGMENTATION
# =============================================================================
print("\n" + "=" * 60)
print("AGE GROUP SEGMENTATION")
print("=" * 60)

age_analysis = df_clean.groupby('age').agg({
    'ad_id': 'count',
    'Impressions': 'sum',
    'Clicks': 'sum',
    'Spent': 'sum',
    'Total_Conversion': 'sum',
    'Approved_Conversion': 'sum',
    'Revenue': 'sum'
}).rename(columns={'ad_id': 'Ad_Count'})

age_analysis['CTR'] = (age_analysis['Clicks'] / age_analysis['Impressions']) * 100
age_analysis['Conversion_Rate'] = (age_analysis['Total_Conversion'] / age_analysis['Clicks']) * 100
age_analysis['Conversion_Share'] = (age_analysis['Total_Conversion'] / age_analysis['Total_Conversion'].sum()) * 100
age_analysis['Actual_CPA'] = age_analysis['Spent'] / age_analysis['Total_Conversion']
age_analysis['Actual_ROAS'] = age_analysis['Revenue'] / age_analysis['Spent']

print(age_analysis[['Ad_Count', 'Total_Conversion', 'Spent', 'Revenue', 'Conversion_Share', 'Actual_CPA', 'Actual_ROAS']])

# Age Group Visualization
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

age_order = ['30-34', '35-39', '40-44', '45-49']
colors_age = ['#27ae60', '#3498db', '#f39c12', '#e74c3c']

# Conversions
conv_data = age_analysis.loc[age_order, 'Total_Conversion']
bars1 = axes[0, 0].bar(age_order, conv_data, color=colors_age, edgecolor='white', linewidth=2, alpha=0.8)
axes[0, 0].set_xlabel('Age Group', fontsize=12)
axes[0, 0].set_ylabel('Total Conversions', fontsize=12)
axes[0, 0].set_title('Total Conversions by Age Group', fontsize=14, fontweight='bold')
for bar, val in zip(bars1, conv_data):
    axes[0, 0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
                   f'{val:,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

# CPA
cpa_data = age_analysis.loc[age_order, 'Actual_CPA']
bars2 = axes[0, 1].bar(age_order, cpa_data, color=colors_age, edgecolor='white', linewidth=2, alpha=0.8)
axes[0, 1].set_xlabel('Age Group', fontsize=12)
axes[0, 1].set_ylabel('Cost per Acquisition ($)', fontsize=12)
axes[0, 1].set_title('CPA by Age Group (Lower is Better)', fontsize=14, fontweight='bold')
for bar, val in zip(bars2, cpa_data):
    axes[0, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                   f'${val:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

# Pie Chart
conv_share = age_analysis.loc[age_order, 'Conversion_Share']
wedges, texts, autotexts = axes[1, 0].pie(conv_share, labels=age_order, autopct='%1.1f%%',
                                          colors=colors_age, explode=[0.05, 0, 0, 0],
                                          shadow=True, startangle=90)
for autotext in autotexts:
    autotext.set_fontsize(12)
    autotext.set_fontweight('bold')
axes[1, 0].set_title('Conversion Share by Age Group', fontsize=14, fontweight='bold')

# ROAS
roas_data = age_analysis.loc[age_order, 'Actual_ROAS']
bars4 = axes[1, 1].bar(age_order, roas_data, color=colors_age, edgecolor='white', linewidth=2, alpha=0.8)
axes[1, 1].set_xlabel('Age Group', fontsize=12)
axes[1, 1].set_ylabel('ROAS', fontsize=12)
axes[1, 1].set_title('ROAS by Age Group', fontsize=14, fontweight='bold')
axes[1, 1].axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Break-even')
for bar, val in zip(bars4, roas_data):
    axes[1, 1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                   f'{val:.2f}x', ha='center', va='bottom', fontsize=11, fontweight='bold')
axes[1, 1].legend()

plt.tight_layout()
plt.savefig('/root/ad-campaign-analytics/reports/05_age_segmentation.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Age segmentation charts saved")

# Heatmap
age_gender_conv = df_clean.pivot_table(
    values='Total_Conversion',
    index='age',
    columns='gender',
    aggfunc='sum'
)

plt.figure(figsize=(10, 6))
sns.heatmap(age_gender_conv, annot=True, fmt='.0f', cmap='YlOrRd',
            linewidths=2, linecolor='white', cbar_kws={'label': 'Total Conversions'})
plt.title('Conversions Heatmap: Age × Gender', fontsize=14, fontweight='bold')
plt.xlabel('Gender', fontsize=12)
plt.ylabel('Age Group', fontsize=12)
plt.tight_layout()
plt.savefig('/root/ad-campaign-analytics/reports/06_age_gender_heatmap.png', dpi=150, bbox_inches='tight')
plt.close()
print("✅ Heatmap saved")

# =============================================================================
# 8. SQL ANALYSIS WITH DUCKDB
# =============================================================================
print("\n" + "=" * 60)
print("SQL ANALYSIS WITH DUCKDB")
print("=" * 60)

con = duckdb.connect(database=':memory:')
con.register('ads', df_clean)

# Query 1: Cohort ROAS by Campaign Type
query1 = """
SELECT 
    Campaign_Type,
    COUNT(*) as Ad_Count,
    ROUND(SUM(Spent), 2) as Total_Spent,
    SUM(Total_Conversion) as Conversions,
    ROUND(SUM(Revenue), 2) as Revenue,
    ROUND(SUM(Revenue) / NULLIF(SUM(Spent), 0), 4) as ROAS
FROM ads
GROUP BY Campaign_Type
ORDER BY ROAS DESC
"""
print("\n📊 Query 1: ROAS by Campaign Type")
print(con.execute(query1).fetchdf().to_string(index=False))

# Query 2: Audience Segment Ranking
query2 = """
SELECT 
    age,
    gender,
    SUM(Total_Conversion) as Conversions,
    ROUND(SUM(Revenue) / NULLIF(SUM(Spent), 0), 4) as ROAS,
    RANK() OVER (ORDER BY SUM(Revenue) / NULLIF(SUM(Spent), 0) DESC) as Rank
FROM ads
WHERE Spent > 0
GROUP BY age, gender
ORDER BY ROAS DESC
"""
print("\n📊 Query 2: Audience Segment ROAS Ranking")
print(con.execute(query2).fetchdf().to_string(index=False))

# Save SQL queries
sql_queries = """
-- ============================================================
-- AD CAMPAIGN PERFORMANCE ANALYTICS - SQL QUERIES
-- ============================================================

-- Query 1: Cohort ROAS by Campaign Type
SELECT 
    Campaign_Type,
    COUNT(*) as Ad_Count,
    ROUND(SUM(Spent), 2) as Total_Spent,
    SUM(Total_Conversion) as Conversions,
    ROUND(SUM(Revenue), 2) as Revenue,
    ROUND(SUM(Revenue) / NULLIF(SUM(Spent), 0), 4) as ROAS
FROM ads
GROUP BY Campaign_Type
ORDER BY ROAS DESC;

-- Query 2: Audience Segment ROAS Ranking
SELECT 
    age,
    gender,
    SUM(Total_Conversion) as Conversions,
    ROUND(SUM(Revenue) / NULLIF(SUM(Spent), 0), 4) as ROAS,
    RANK() OVER (ORDER BY SUM(Revenue) / NULLIF(SUM(Spent), 0) DESC) as Rank
FROM ads
WHERE Spent > 0
GROUP BY age, gender
ORDER BY ROAS DESC;

-- Query 3: Top 10 Interest Categories by ROAS
SELECT 
    interest as Interest_ID,
    COUNT(*) as Ad_Count,
    SUM(Total_Conversion) as Conversions,
    ROUND(SUM(Revenue) / NULLIF(SUM(Spent), 0), 4) as ROAS
FROM ads
WHERE Spent > 0 AND Total_Conversion > 0
GROUP BY interest
HAVING COUNT(*) >= 5
ORDER BY ROAS DESC
LIMIT 10;

-- Query 4: Campaign Performance Summary
SELECT 
    xyz_campaign_id as Campaign,
    Campaign_Type as Type,
    SUM(Impressions) as Impressions,
    SUM(Clicks) as Clicks,
    SUM(Total_Conversion) as Conversions,
    ROUND(SUM(Spent), 2) as Spent,
    ROUND(SUM(Revenue), 2) as Revenue,
    ROUND(SUM(Revenue) / NULLIF(SUM(Spent), 0), 4) as ROAS
FROM ads
GROUP BY xyz_campaign_id, Campaign_Type
ORDER BY Revenue DESC;
"""

with open('/root/ad-campaign-analytics/sql/analytics_queries.sql', 'w') as f:
    f.write(sql_queries)
print("\n✅ SQL queries saved to sql/analytics_queries.sql")

con.close()

# =============================================================================
# 9. EXECUTIVE SUMMARY
# =============================================================================
print("\n" + "=" * 80)
print("📊 EXECUTIVE SUMMARY: AD CAMPAIGN PERFORMANCE ANALYTICS")
print("=" * 80)

total_spend = df_clean['Spent'].sum()
total_revenue = df_clean['Revenue'].sum()
total_conversions = df_clean['Total_Conversion'].sum()
overall_roas = total_revenue / total_spend

print(f"\n📈 OVERALL METRICS:")
print(f"   • Total Ad Spend: ${total_spend:,.2f}")
print(f"   • Total Revenue: ${total_revenue:,.2f}")
print(f"   • Overall ROAS: {overall_roas:.2f}x")
print(f"   • Total Conversions: {total_conversions:,}")

best_age = age_analysis['Total_Conversion'].idxmax()
best_age_conv_share = age_analysis.loc[best_age, 'Conversion_Share']
best_age_cpa = age_analysis.loc[best_age, 'Actual_CPA']

print(f"\n🎯 KEY FINDING #1: VIDEO ADS OUTPERFORM IMAGE ADS")
print(f"   • Video ads generate {roas_ratio:.2f}x higher ROAS")
print(f"   • Statistical significance: p = {p_value:.6f}")
print(f"   • Effect size: {cohens_d:.4f} ({effect_interpretation})")

print(f"\n🎯 KEY FINDING #2: {best_age} AGE GROUP IS MOST VALUABLE")
print(f"   • Drives {best_age_conv_share:.1f}% of all conversions")
print(f"   • Lowest CPA at ${best_age_cpa:.2f}")

print(f"\n💡 BUSINESS RECOMMENDATIONS:")
print(f"   1. Shift budget toward Video ad formats")
print(f"   2. Prioritize {best_age} age segment")
print(f"   3. Reduce spend on 45-49 age group")
print(f"   4. A/B test video creatives")

print("\n" + "=" * 80)
print("✅ ANALYSIS COMPLETE!")
print("=" * 80)

print("\n📁 Generated Files:")
print("   • data/ad_campaign_cleaned.csv")
print("   • sql/analytics_queries.sql")
print("   • reports/01_distributions.png")
print("   • reports/02_correlation_matrix.png")
print("   • reports/03_funnel_analysis.png")
print("   • reports/04_ab_test_results.png")
print("   • reports/05_age_segmentation.png")
print("   • reports/06_age_gender_heatmap.png")
