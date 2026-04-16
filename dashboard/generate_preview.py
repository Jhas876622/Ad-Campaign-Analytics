"""
Generate static dashboard preview for GitHub README.
Creates an HTML file that can be viewed without running the server.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Load data
df = pd.read_csv('/root/ad-campaign-analytics/data/ad_campaign_cleaned.csv')

# Calculate KPIs
total_impressions = df['Impressions'].sum()
total_clicks = df['Clicks'].sum()
total_spent = df['Spent'].sum()
total_revenue = df['Revenue'].sum()
total_conversions = df['Total_Conversion'].sum()

overall_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
overall_cpc = (total_spent / total_clicks) if total_clicks > 0 else 0
overall_roas = (total_revenue / total_spent) if total_spent > 0 else 0
overall_cvr = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0
overall_cpa = (total_spent / total_conversions) if total_conversions > 0 else 0

# Create combined dashboard figure
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=(
        'Marketing Funnel', 'ROAS by Campaign Type',
        'Conversions by Age & Gender', 'Spend vs Revenue',
        'Conversion Share by Age', 'Campaign Performance'
    ),
    specs=[
        [{"type": "funnel"}, {"type": "bar"}],
        [{"type": "heatmap"}, {"type": "scatter"}],
        [{"type": "pie"}, {"type": "bar"}]
    ],
    vertical_spacing=0.12,
    horizontal_spacing=0.1
)

# 1. Funnel Chart
funnel_data = {
    'Stage': ['Impressions', 'Clicks', 'Conversions', 'Approved'],
    'Count': [total_impressions, total_clicks, total_conversions, df['Approved_Conversion'].sum()]
}
fig.add_trace(
    go.Funnel(
        y=funnel_data['Stage'],
        x=funnel_data['Count'],
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(color=['#1a73e8', '#34a853', '#fbbc04', '#ea4335'])
    ),
    row=1, col=1
)

# 2. ROAS by Campaign Type
campaign_roas = df.groupby('Campaign_Type').agg({'Spent': 'sum', 'Revenue': 'sum'}).reset_index()
campaign_roas['ROAS'] = campaign_roas['Revenue'] / campaign_roas['Spent']
fig.add_trace(
    go.Bar(
        x=campaign_roas['Campaign_Type'],
        y=campaign_roas['ROAS'],
        marker_color=['#ea4335', '#1a73e8'],
        text=campaign_roas['ROAS'].round(2),
        textposition='outside'
    ),
    row=1, col=2
)

# 3. Heatmap
pivot = df.pivot_table(values='Total_Conversion', index='age', columns='gender', aggfunc='sum').fillna(0)
fig.add_trace(
    go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale='Blues',
        text=pivot.values.astype(int),
        texttemplate="%{text}",
        showscale=False
    ),
    row=2, col=1
)

# 4. Scatter Plot
ad_agg = df.groupby('ad_id').agg({
    'Spent': 'sum', 'Revenue': 'sum', 'Campaign_Type': 'first'
}).reset_index()
colors = ['#1a73e8' if t == 'Video' else '#ea4335' for t in ad_agg['Campaign_Type']]
fig.add_trace(
    go.Scatter(
        x=ad_agg['Spent'],
        y=ad_agg['Revenue'],
        mode='markers',
        marker=dict(color=colors, size=8, opacity=0.6),
        showlegend=False
    ),
    row=2, col=2
)

# 5. Pie Chart
age_conv = df.groupby('age')['Total_Conversion'].sum().reset_index()
fig.add_trace(
    go.Pie(
        labels=age_conv['age'],
        values=age_conv['Total_Conversion'],
        marker_colors=['#1a73e8', '#34a853', '#fbbc04', '#ea4335'],
        textinfo='label+percent',
        showlegend=False
    ),
    row=3, col=1
)

# 6. Campaign Performance
camp_perf = df.groupby(['xyz_campaign_id', 'Campaign_Type']).agg({
    'Spent': 'sum', 'Revenue': 'sum'
}).reset_index()
camp_perf['ROAS'] = camp_perf['Revenue'] / camp_perf['Spent']
colors = ['#1a73e8' if t == 'Video' else '#ea4335' for t in camp_perf['Campaign_Type']]
fig.add_trace(
    go.Bar(
        x=[f"Camp {c}" for c in camp_perf['xyz_campaign_id']],
        y=camp_perf['ROAS'],
        marker_color=colors,
        text=camp_perf['ROAS'].round(2),
        textposition='outside',
        showlegend=False
    ),
    row=3, col=2
)

# Update layout
fig.update_layout(
    title=dict(
        text='<b>📊 Ad Campaign Performance Analytics Dashboard</b><br><sup>ROAS Optimization | Google/Meta Ad Campaigns</sup>',
        x=0.5,
        font=dict(size=20)
    ),
    height=1200,
    width=1200,
    showlegend=False,
    paper_bgcolor='#f5f7fa',
    font=dict(family='Arial, sans-serif')
)

# Add KPI annotations
kpi_text = f"""
<b>KEY METRICS</b><br>
CTR: {overall_ctr:.2f}% | CPC: ${overall_cpc:.2f} | ROAS: {overall_roas:.2f}x | CVR: {overall_cvr:.2f}% | CPA: ${overall_cpa:.2f}
"""
fig.add_annotation(
    text=kpi_text,
    xref="paper", yref="paper",
    x=0.5, y=1.02,
    showarrow=False,
    font=dict(size=12),
    align="center"
)

# Save as HTML
output_path = '/root/ad-campaign-analytics/reports/dashboard_preview.html'
fig.write_html(output_path, include_plotlyjs='cdn')
print(f"✅ Dashboard preview saved to: {output_path}")

# Also save as image
try:
    fig.write_image('/root/ad-campaign-analytics/reports/dashboard_screenshot.png', scale=2)
    print("✅ Dashboard screenshot saved")
except Exception as e:
    print(f"⚠️ Could not save PNG (requires kaleido): {e}")

print("\n📊 Dashboard Summary:")
print(f"   Total Spend: ${total_spent:,.2f}")
print(f"   Total Revenue: ${total_revenue:,.2f}")
print(f"   Overall ROAS: {overall_roas:.2f}x")
print(f"   Total Conversions: {total_conversions:,}")
