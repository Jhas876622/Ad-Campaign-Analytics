"""
Generate realistic Facebook/Meta Ad Campaign data matching the Kaggle dataset schema.
Dataset: Sales Conversion Optimization (KAG_conversion_data.csv)
Source: https://www.kaggle.com/datasets/loveall/clicks-conversion-tracking

This script generates data that mirrors the real dataset structure with realistic patterns:
- 3 campaigns (916, 936, 1178) with different performance profiles
- Age groups: 30-34, 35-39, 40-44, 45-49
- Gender: M, F
- Interest codes: Various numeric codes
- Realistic correlations between impressions, clicks, spend, and conversions
"""

import numpy as np
import pandas as pd

np.random.seed(42)

# Configuration matching the real dataset
n_records = 1143
campaigns = [916, 936, 1178]
age_groups = ['30-34', '35-39', '40-44', '45-49']
genders = ['M', 'F']
interests = list(range(2, 115))  # Interest codes 2-114

# Campaign characteristics (different performance profiles)
# Campaign 1178 = Video-like (higher ROAS), 916 and 936 = Image-like (lower ROAS)
campaign_profiles = {
    916: {'base_impressions': 5000, 'ctr_mult': 0.8, 'conv_mult': 0.7, 'type': 'Image'},
    936: {'base_impressions': 8000, 'ctr_mult': 0.9, 'conv_mult': 0.8, 'type': 'Image'},
    1178: {'base_impressions': 15000, 'ctr_mult': 1.5, 'conv_mult': 1.8, 'type': 'Video'}  # Higher performance
}

# Age group characteristics (30-34 performs best)
age_profiles = {
    '30-34': {'conv_mult': 1.4, 'cpa_mult': 0.7},   # Best: highest conversion, lowest CPA
    '35-39': {'conv_mult': 1.1, 'cpa_mult': 0.9},
    '40-44': {'conv_mult': 0.9, 'cpa_mult': 1.1},
    '45-49': {'conv_mult': 0.8, 'cpa_mult': 1.3}    # Worst: lowest conversion, highest CPA
}

data = []

for i in range(n_records):
    # Random selections
    campaign_id = np.random.choice(campaigns, p=[0.35, 0.25, 0.40])  # 1178 most common
    age = np.random.choice(age_groups, p=[0.37, 0.22, 0.18, 0.23])  # 30-34 most common
    gender = np.random.choice(genders, p=[0.48, 0.52])
    interest = np.random.choice(interests)
    
    # Generate fb_campaign_id (unique per ad)
    fb_campaign_id = 103000 + i + np.random.randint(0, 1000)
    
    # Generate ad_id
    ad_id = 708000 + i + np.random.randint(0, 500)
    
    # Get profiles
    camp_profile = campaign_profiles[campaign_id]
    age_profile = age_profiles[age]
    
    # Generate impressions (log-normal distribution for realistic heavy tail)
    base_imp = camp_profile['base_impressions']
    impressions = int(np.random.lognormal(np.log(base_imp), 1.2))
    impressions = max(100, min(impressions, 2000000))  # Cap extremes
    
    # Generate clicks based on impressions and CTR
    base_ctr = 0.00015 * camp_profile['ctr_mult']  # Base CTR around 0.015%
    expected_clicks = impressions * base_ctr * np.random.uniform(0.5, 2.0)
    clicks = int(np.random.poisson(max(0.1, expected_clicks)))
    clicks = min(clicks, int(impressions * 0.01))  # Cap at 1% CTR max
    
    # Generate spend based on clicks (CPC model)
    if clicks > 0:
        cpc = np.random.uniform(1.0, 2.5) * age_profile['cpa_mult']
        spent = round(clicks * cpc + np.random.uniform(0, 0.5), 2)
    else:
        spent = 0.0
    
    # Generate conversions
    if clicks > 0:
        conv_rate = 0.15 * camp_profile['conv_mult'] * age_profile['conv_mult']
        conv_rate *= np.random.uniform(0.3, 1.5)
        total_conversion = int(np.random.poisson(max(0.1, clicks * conv_rate)))
        total_conversion = min(total_conversion, clicks)  # Can't exceed clicks
    else:
        total_conversion = 0
    
    # Approved conversion (subset of total conversion)
    if total_conversion > 0:
        approval_rate = np.random.uniform(0.3, 0.8)
        approved_conversion = int(total_conversion * approval_rate)
    else:
        approved_conversion = 0
    
    data.append({
        'ad_id': ad_id,
        'xyz_campaign_id': campaign_id,
        'fb_campaign_id': fb_campaign_id,
        'age': age,
        'gender': gender,
        'interest': interest,
        'Impressions': impressions,
        'Clicks': clicks,
        'Spent': spent,
        'Total_Conversion': total_conversion,
        'Approved_Conversion': approved_conversion
    })

# Create DataFrame
df = pd.DataFrame(data)

# Sort by ad_id for consistency
df = df.sort_values('ad_id').reset_index(drop=True)

# Save to CSV
df.to_csv('/root/ad-campaign-analytics/data/KAG_conversion_data.csv', index=False)

print("Dataset generated successfully!")
print(f"Shape: {df.shape}")
print(f"\nColumn dtypes:\n{df.dtypes}")
print(f"\nFirst 5 rows:\n{df.head()}")
print(f"\nCampaign distribution:\n{df['xyz_campaign_id'].value_counts()}")
print(f"\nAge distribution:\n{df['age'].value_counts()}")
