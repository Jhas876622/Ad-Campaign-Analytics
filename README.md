# 📊 Google/Meta Ad Campaign Performance Analytics

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-green.svg?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Dash-purple.svg?logo=plotly&logoColor=white)](https://plotly.com/)
[![DuckDB](https://img.shields.io/badge/DuckDB-SQL-orange.svg)](https://duckdb.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete-brightgreen.svg)]()

**An end-to-end data analytics project analyzing Facebook/Meta ad campaign performance to optimize ROAS (Return on Ad Spend) through statistical analysis, SQL queries, and interactive dashboards.**

---

## 🎯 Business Problem

A digital marketing team needs to optimize their ad spend across multiple campaigns. Key business questions:

1. **Which ad format (Video vs Image) delivers higher ROI?**
2. **Which audience segments drive the most conversions at the lowest cost?**
3. **Where should we reallocate budget to maximize ROAS?**

This project provides **data-driven answers** using statistical analysis and visualization.

---

## 📈 Key Findings

### 🎬 Video Ads Outperform Image Ads by 2.9x
| Metric | Video Ads | Image Ads | Difference |
|--------|-----------|-----------|------------|
| **Mean ROAS** | 4.49x | 1.54x | +192% |
| **Sample Size** | 257 ads | 86 ads | — |
| **Statistical Significance** | p < 0.001 | — | **Confirmed** |
| **Effect Size (Cohen's d)** | 0.70 | — | Medium-Large |

**Recommendation:** Shift 40% of image ad budget to video formats for estimated +$8,500 revenue increase.

### 👥 30-34 Age Group is the Top Performer
| Age Group | Conversion Share | CPA | ROAS |
|-----------|-----------------|-----|------|
| **30-34** | **51.2%** | **$4.09** | **5.82x** |
| 35-39 | 17.7% | $9.69 | 2.16x |
| 40-44 | 11.7% | $10.40 | 2.36x |
| 45-49 | 19.5% | $14.04 | 1.83x |

**Recommendation:** Increase bid adjustments by 25% for the 30-34 demographic; reduce bids for 45-49.

### 💰 Overall Campaign Performance
- **Total Ad Spend:** $9,050.19
- **Total Revenue Generated:** $27,735.00
- **Overall ROAS:** 3.06x (53% above industry benchmark of 2.0x)
- **Total Conversions:** 1,167

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Languages** | Python 3.9+, SQL |
| **Data Analysis** | Pandas, NumPy, SciPy |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **Dashboard** | Plotly Dash |
| **Database** | DuckDB (in-process SQL) |
| **Statistical Tests** | Welch's t-test, Cohen's d, 95% CI |
| **IDE** | Jupyter Notebook |
| **Version Control** | Git, GitHub |

---

## 📁 Project Structure

```
ad-campaign-analytics/
├── 📂 data/
│   ├── KAG_conversion_data.csv      # Raw dataset
│   └── ad_campaign_cleaned.csv      # Processed dataset with KPIs
│
├── 📂 notebooks/
│   └── 01_ad_campaign_analysis.ipynb # Complete EDA & analysis
│
├── 📂 sql/
│   └── analytics_queries.sql         # DuckDB SQL queries
│
├── 📂 reports/
│   ├── 01_distributions.png          # Distribution plots
│   ├── 02_correlation_matrix.png     # Correlation heatmap
│   ├── 03_funnel_analysis.png        # Marketing funnel
│   ├── 04_ab_test_results.png        # A/B test visualization
│   ├── 05_age_segmentation.png       # Age group analysis
│   ├── 06_age_gender_heatmap.png     # Demographic heatmap
│   ├── dashboard_preview.html        # Interactive dashboard
│   └── analysis_report.pdf           # Executive summary
│
├── 📂 dashboard/
│   ├── app.py                        # Plotly Dash application
│   └── generate_preview.py           # Dashboard preview generator
│
├── 📂 src/
│   ├── generate_data.py              # Data generation script
│   └── run_analysis.py               # Complete analysis pipeline
│
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

---

## 📊 Dataset Information

| Attribute | Description |
|-----------|-------------|
| **Source** | [Kaggle: Sales Conversion Optimization](https://www.kaggle.com/datasets/loveall/clicks-conversion-tracking) |
| **Records** | 1,143 ad-level observations |
| **Features** | 11 original + 7 engineered |
| **Campaigns** | 3 (Campaign 1178 = Video, 916/936 = Image) |
| **Time Period** | Single campaign cycle |

### Feature Descriptions

| Column | Type | Description |
|--------|------|-------------|
| `ad_id` | int | Unique ad identifier |
| `xyz_campaign_id` | int | Campaign grouping (916, 936, 1178) |
| `fb_campaign_id` | int | Facebook campaign ID |
| `age` | str | Target age bracket (30-34, 35-39, 40-44, 45-49) |
| `gender` | str | Target gender (M/F) |
| `interest` | int | Interest category code |
| `Impressions` | int | Number of ad views |
| `Clicks` | int | Number of clicks |
| `Spent` | float | Ad spend in USD |
| `Total_Conversion` | int | Total conversions |
| `Approved_Conversion` | int | Approved/verified conversions |

### Engineered KPIs

| KPI | Formula | Description |
|-----|---------|-------------|
| **CTR** | Clicks / Impressions × 100 | Click-Through Rate |
| **CPC** | Spent / Clicks | Cost Per Click |
| **ROAS** | Revenue / Spent | Return on Ad Spend |
| **CVR** | Conversions / Clicks × 100 | Conversion Rate |
| **CPA** | Spent / Conversions | Cost Per Acquisition |
| **Revenue** | (Total × $5) + (Approved × $50) | Estimated revenue |

---

## 🔬 Methodology

### 1. Exploratory Data Analysis (EDA)
- Distribution analysis of all numerical features
- Correlation matrix for feature relationships
- Categorical variable analysis (campaigns, demographics)

### 2. Data Cleaning & Feature Engineering
- Handled division-by-zero in KPI calculations
- Created campaign type mapping (Video/Image)
- Computed revenue using conversion value model

### 3. Funnel Analysis
```
Impressions: 21,957,412 (100%)
     ↓ Drop-off: 99.98%
Clicks: 5,239 (0.02%)
     ↓ Drop-off: 77.72%
Conversions: 1,167 (0.005%)
     ↓ Drop-off: 62.47%
Approved: 438 (0.002%)
```

### 4. A/B Testing (Video vs Image)
- **Test:** Welch's Two-Sample t-test (unequal variances)
- **Hypothesis:** H₀: μ_video = μ_image vs H₁: μ_video ≠ μ_image
- **Results:**
  - t-statistic: 8.88
  - p-value: < 0.001
  - Cohen's d: 0.70 (medium-large effect)
  - 95% CI: [2.30, 3.61]

### 5. SQL Analytics (DuckDB)
- Cohort ROAS by campaign type
- Audience segment ranking
- Top interest categories
- Campaign performance summary

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.9+
pip (package manager)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/ad-campaign-analytics.git
cd ad-campaign-analytics
```

2. **Create virtual environment (recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the analysis**
```bash
python src/run_analysis.py
```

5. **Launch the dashboard**
```bash
python dashboard/app.py
# Open http://127.0.0.1:8050 in your browser
```

6. **Explore the Jupyter notebook**
```bash
jupyter notebook notebooks/01_ad_campaign_analysis.ipynb
```

---

## 📸 Dashboard Features

The interactive dashboard includes:
- **KPI Cards:** Real-time metrics (CTR, CPC, ROAS, CVR, CPA)
- **Marketing Funnel:** Impressions → Clicks → Conversions flow
- **ROAS Comparison:** Video vs Image performance bar chart
- **Demographic Heatmap:** Age × Gender conversion matrix
- **Scatter Plot:** Spend vs Revenue with trendline
- **Age Analysis:** Conversion share and CPA by age group

> 🔗 View the interactive dashboard: Open `reports/dashboard_preview.html` in your browser

---

## 📋 SQL Queries

Sample query from `sql/analytics_queries.sql`:

```sql
-- ROAS by Campaign Type with Statistical Summary
SELECT 
    Campaign_Type,
    COUNT(*) as Ad_Count,
    ROUND(SUM(Spent), 2) as Total_Spent,
    SUM(Total_Conversion) as Conversions,
    ROUND(SUM(Revenue), 2) as Total_Revenue,
    ROUND(SUM(Revenue) / NULLIF(SUM(Spent), 0), 2) as ROAS
FROM ad_data
WHERE Spent > 0
GROUP BY Campaign_Type
ORDER BY ROAS DESC;
```

---

## 📊 Business Recommendations

| Priority | Recommendation | Expected Impact |
|----------|---------------|-----------------|
| 🔴 High | Shift 40% of image budget to video | +$8,500 revenue |
| 🔴 High | Increase bids 25% for ages 30-34 | +15% conversions |
| 🟡 Medium | Reduce bids 20% for ages 45-49 | -$640 wasted spend |
| 🟡 Medium | A/B test video creatives | Data for optimization |
| 🟢 Low | Explore new interest categories | Expand reach |

---

## 📄 Files & Outputs

| File | Description |
|------|-------------|
| `reports/analysis_report.pdf` | Executive summary with all findings |
| `reports/dashboard_preview.html` | Interactive Plotly dashboard |
| `notebooks/01_ad_campaign_analysis.ipynb` | Complete analysis notebook |
| `sql/analytics_queries.sql` | All SQL queries used |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Satyam Kumar Jha**
- LinkedIn: [https://linkedin.com/in/satyam-kumar-jha-27545a288]
- GitHub: [https://github.com/Jhas876622]
- Email: jha876622@gmail.com

---

## 🙏 Acknowledgments

- [Kaggle](https://www.kaggle.com/) for the dataset
- [Plotly](https://plotly.com/) for visualization libraries
- [DuckDB](https://duckdb.org/) for in-process SQL engine

---

<p align="center">
  <b>⭐ Star this repository if you found it helpful!</b>
</p>
