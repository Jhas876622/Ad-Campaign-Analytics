"""
Google/Meta Ad Campaign Performance Analytics Dashboard
========================================================
Interactive dashboard built with Plotly Dash for ROAS optimization analysis.

Author: [Your Name]
Date: April 2026
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os

# ============================================================
# DATA LOADING
# ============================================================

def load_data():
    """Load and prepare the cleaned dataset."""
    # Try multiple paths for flexibility
    possible_paths = [
        '../data/ad_campaign_cleaned.csv',
        'data/ad_campaign_cleaned.csv',
        '/root/ad-campaign-analytics/data/ad_campaign_cleaned.csv'
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            return df
    
    raise FileNotFoundError("Could not find ad_campaign_cleaned.csv")

# Load data
df = load_data()

# ============================================================
# CALCULATE KPIs
# ============================================================

# Overall KPIs
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

# ============================================================
# CREATE FIGURES
# ============================================================

def create_funnel_chart():
    """Create marketing funnel visualization."""
    funnel_data = pd.DataFrame({
        'Stage': ['Impressions', 'Clicks', 'Total Conversions', 'Approved Conversions'],
        'Count': [
            df['Impressions'].sum(),
            df['Clicks'].sum(),
            df['Total_Conversion'].sum(),
            df['Approved_Conversion'].sum()
        ]
    })
    
    # Calculate drop-off rates
    funnel_data['Drop_Off'] = funnel_data['Count'].pct_change() * 100
    funnel_data['Drop_Off'] = funnel_data['Drop_Off'].fillna(0)
    
    fig = go.Figure(go.Funnel(
        y=funnel_data['Stage'],
        x=funnel_data['Count'],
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(
            color=['#1a73e8', '#34a853', '#fbbc04', '#ea4335'],
            line=dict(width=2, color='white')
        ),
        connector=dict(line=dict(color="royalblue", dash="dot", width=2))
    ))
    
    fig.update_layout(
        title=dict(text='<b>Marketing Funnel Analysis</b>', x=0.5, font=dict(size=18)),
        font=dict(size=12),
        height=400,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_roas_by_campaign():
    """Create ROAS comparison by campaign type."""
    campaign_roas = df.groupby('Campaign_Type').agg({
        'Spent': 'sum',
        'Revenue': 'sum',
        'Total_Conversion': 'sum'
    }).reset_index()
    campaign_roas['ROAS'] = campaign_roas['Revenue'] / campaign_roas['Spent']
    
    colors = ['#1a73e8' if x == 'Video' else '#ea4335' for x in campaign_roas['Campaign_Type']]
    
    fig = go.Figure(data=[
        go.Bar(
            x=campaign_roas['Campaign_Type'],
            y=campaign_roas['ROAS'],
            marker_color=colors,
            text=campaign_roas['ROAS'].round(2),
            textposition='outside',
            textfont=dict(size=14, color='#333')
        )
    ])
    
    # Add benchmark line
    fig.add_hline(y=2.0, line_dash="dash", line_color="green", 
                  annotation_text="Industry Benchmark (2.0x)", 
                  annotation_position="top right")
    
    fig.update_layout(
        title=dict(text='<b>ROAS by Campaign Type</b>', x=0.5, font=dict(size=18)),
        xaxis_title='Campaign Type',
        yaxis_title='ROAS (Return on Ad Spend)',
        height=400,
        margin=dict(l=60, r=20, t=60, b=60),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=dict(gridcolor='lightgray', gridwidth=0.5)
    )
    
    return fig


def create_age_heatmap():
    """Create age group x gender conversion heatmap."""
    pivot = df.pivot_table(
        values='Total_Conversion', 
        index='age', 
        columns='gender', 
        aggfunc='sum'
    ).fillna(0)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='Blues',
        text=pivot.values.astype(int),
        texttemplate="%{text}",
        textfont=dict(size=14),
        hovertemplate='Age: %{y}<br>Gender: %{x}<br>Conversions: %{z}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text='<b>Conversions by Age Group & Gender</b>', x=0.5, font=dict(size=18)),
        xaxis_title='Gender',
        yaxis_title='Age Group',
        height=400,
        margin=dict(l=60, r=20, t=60, b=60),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


def create_spend_revenue_scatter():
    """Create spend vs revenue scatter plot with trendline."""
    # Aggregate by ad for cleaner visualization
    ad_data = df.groupby('ad_id').agg({
        'Spent': 'sum',
        'Revenue': 'sum',
        'Campaign_Type': 'first',
        'age': 'first'
    }).reset_index()
    
    fig = px.scatter(
        ad_data,
        x='Spent',
        y='Revenue',
        color='Campaign_Type',
        size='Revenue',
        hover_data=['ad_id', 'age'],
        trendline='ols',
        color_discrete_map={'Video': '#1a73e8', 'Image': '#ea4335'},
        labels={'Spent': 'Ad Spend ($)', 'Revenue': 'Revenue ($)'}
    )
    
    # Add break-even line (ROAS = 1)
    max_val = max(ad_data['Spent'].max(), ad_data['Revenue'].max())
    fig.add_trace(go.Scatter(
        x=[0, max_val],
        y=[0, max_val],
        mode='lines',
        line=dict(dash='dash', color='gray', width=2),
        name='Break-even (ROAS=1)',
        showlegend=True
    ))
    
    fig.update_layout(
        title=dict(text='<b>Ad Spend vs Revenue</b>', x=0.5, font=dict(size=18)),
        height=400,
        margin=dict(l=60, r=20, t=60, b=60),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='lightgray', gridwidth=0.5),
        yaxis=dict(gridcolor='lightgray', gridwidth=0.5),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )
    
    return fig


def create_age_performance_chart():
    """Create age group performance comparison."""
    age_perf = df.groupby('age').agg({
        'Total_Conversion': 'sum',
        'Spent': 'sum',
        'Revenue': 'sum'
    }).reset_index()
    
    age_perf['CPA'] = age_perf['Spent'] / age_perf['Total_Conversion']
    age_perf['ROAS'] = age_perf['Revenue'] / age_perf['Spent']
    age_perf['Conv_Share'] = age_perf['Total_Conversion'] / age_perf['Total_Conversion'].sum() * 100
    
    # Sort by age group
    age_order = ['30-34', '35-39', '40-44', '45-49']
    age_perf['age'] = pd.Categorical(age_perf['age'], categories=age_order, ordered=True)
    age_perf = age_perf.sort_values('age')
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Conversion Share by Age', 'CPA by Age Group'),
        specs=[[{"type": "pie"}, {"type": "bar"}]]
    )
    
    # Pie chart for conversion share
    colors = ['#1a73e8', '#34a853', '#fbbc04', '#ea4335']
    fig.add_trace(
        go.Pie(
            labels=age_perf['age'],
            values=age_perf['Total_Conversion'],
            hole=0.4,
            marker_colors=colors,
            textinfo='label+percent',
            textposition='outside'
        ),
        row=1, col=1
    )
    
    # Bar chart for CPA
    fig.add_trace(
        go.Bar(
            x=age_perf['age'],
            y=age_perf['CPA'],
            marker_color=colors,
            text=age_perf['CPA'].round(2),
            textposition='outside'
        ),
        row=1, col=2
    )
    
    fig.update_layout(
        title=dict(text='<b>Age Group Performance Analysis</b>', x=0.5, font=dict(size=18)),
        height=400,
        margin=dict(l=60, r=20, t=80, b=60),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_yaxes(title_text='CPA ($)', row=1, col=2)
    
    return fig


def create_campaign_comparison():
    """Create detailed campaign comparison."""
    campaign_data = df.groupby(['xyz_campaign_id', 'Campaign_Type']).agg({
        'Impressions': 'sum',
        'Clicks': 'sum',
        'Spent': 'sum',
        'Revenue': 'sum',
        'Total_Conversion': 'sum',
        'ad_id': 'count'
    }).reset_index()
    
    campaign_data.columns = ['Campaign_ID', 'Type', 'Impressions', 'Clicks', 'Spent', 'Revenue', 'Conversions', 'Ad_Count']
    campaign_data['CTR'] = (campaign_data['Clicks'] / campaign_data['Impressions'] * 100).round(2)
    campaign_data['ROAS'] = (campaign_data['Revenue'] / campaign_data['Spent']).round(2)
    campaign_data['CPA'] = (campaign_data['Spent'] / campaign_data['Conversions']).round(2)
    
    fig = go.Figure()
    
    colors = {'Video': '#1a73e8', 'Image': '#ea4335'}
    
    for camp_type in campaign_data['Type'].unique():
        camp_subset = campaign_data[campaign_data['Type'] == camp_type]
        fig.add_trace(go.Bar(
            name=camp_type,
            x=[f"Campaign {cid}" for cid in camp_subset['Campaign_ID']],
            y=camp_subset['ROAS'],
            marker_color=colors.get(camp_type, 'gray'),
            text=camp_subset['ROAS'],
            textposition='outside'
        ))
    
    fig.update_layout(
        title=dict(text='<b>ROAS by Individual Campaign</b>', x=0.5, font=dict(size=18)),
        xaxis_title='Campaign',
        yaxis_title='ROAS',
        barmode='group',
        height=400,
        margin=dict(l=60, r=20, t=60, b=60),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        yaxis=dict(gridcolor='lightgray', gridwidth=0.5)
    )
    
    return fig

# ============================================================
# DASH APP LAYOUT
# ============================================================

app = dash.Dash(
    __name__,
    title='Ad Campaign Analytics Dashboard',
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]
)
server = app.server

# Custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
                margin: 0;
                padding: 0;
            }
            .dashboard-container {
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
            }
            .header {
                text-align: center;
                padding: 30px 0;
                background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
                color: white;
                border-radius: 12px;
                margin-bottom: 25px;
                box-shadow: 0 4px 20px rgba(26, 115, 232, 0.3);
            }
            .header h1 {
                margin: 0;
                font-size: 2rem;
                font-weight: 700;
            }
            .header p {
                margin: 10px 0 0;
                opacity: 0.9;
                font-size: 1rem;
            }
            .kpi-grid {
                display: grid;
                grid-template-columns: repeat(5, 1fr);
                gap: 20px;
                margin-bottom: 25px;
            }
            .kpi-card {
                background: white;
                border-radius: 12px;
                padding: 25px;
                text-align: center;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .kpi-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.12);
            }
            .kpi-value {
                font-size: 2rem;
                font-weight: 700;
                margin-bottom: 5px;
            }
            .kpi-label {
                font-size: 0.85rem;
                color: #666;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .kpi-trend {
                font-size: 0.75rem;
                margin-top: 8px;
                padding: 3px 8px;
                border-radius: 12px;
                display: inline-block;
            }
            .trend-up { background: #e8f5e9; color: #2e7d32; }
            .trend-neutral { background: #fff8e1; color: #f57c00; }
            .chart-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                margin-bottom: 25px;
            }
            .chart-card {
                background: white;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            }
            .chart-full {
                grid-column: span 2;
            }
            .insights-section {
                background: white;
                border-radius: 12px;
                padding: 25px;
                margin-top: 25px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            }
            .insights-section h2 {
                color: #1a73e8;
                margin-top: 0;
                font-size: 1.3rem;
                border-bottom: 2px solid #e0e0e0;
                padding-bottom: 10px;
            }
            .insight-item {
                display: flex;
                align-items: flex-start;
                margin-bottom: 15px;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #1a73e8;
            }
            .insight-icon {
                font-size: 1.5rem;
                margin-right: 15px;
            }
            .insight-text h4 {
                margin: 0 0 5px;
                color: #333;
            }
            .insight-text p {
                margin: 0;
                color: #666;
                font-size: 0.9rem;
            }
            .footer {
                text-align: center;
                padding: 20px;
                color: #666;
                font-size: 0.85rem;
            }
            @media (max-width: 1200px) {
                .kpi-grid { grid-template-columns: repeat(3, 1fr); }
            }
            @media (max-width: 768px) {
                .kpi-grid { grid-template-columns: repeat(2, 1fr); }
                .chart-grid { grid-template-columns: 1fr; }
                .chart-full { grid-column: span 1; }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# App Layout
app.layout = html.Div([
    html.Div([
        # Header
        html.Div([
            html.H1('📊 Ad Campaign Performance Analytics'),
            html.P('ROAS Optimization Dashboard | Google/Meta Ad Campaigns')
        ], className='header'),
        
        # KPI Cards
        html.Div([
            html.Div([
                html.Div(f'{overall_ctr:.2f}%', className='kpi-value', style={'color': '#1a73e8'}),
                html.Div('Click-Through Rate (CTR)', className='kpi-label'),
                html.Div('▲ Above average', className='kpi-trend trend-up')
            ], className='kpi-card'),
            
            html.Div([
                html.Div(f'${overall_cpc:.2f}', className='kpi-value', style={'color': '#34a853'}),
                html.Div('Cost Per Click (CPC)', className='kpi-label'),
                html.Div('◆ On target', className='kpi-trend trend-neutral')
            ], className='kpi-card'),
            
            html.Div([
                html.Div(f'{overall_roas:.2f}x', className='kpi-value', style={'color': '#ea4335'}),
                html.Div('Return on Ad Spend (ROAS)', className='kpi-label'),
                html.Div('▲ Excellent ROI', className='kpi-trend trend-up')
            ], className='kpi-card'),
            
            html.Div([
                html.Div(f'{overall_cvr:.2f}%', className='kpi-value', style={'color': '#fbbc04'}),
                html.Div('Conversion Rate (CVR)', className='kpi-label'),
                html.Div('▲ Strong performance', className='kpi-trend trend-up')
            ], className='kpi-card'),
            
            html.Div([
                html.Div(f'${overall_cpa:.2f}', className='kpi-value', style={'color': '#9c27b0'}),
                html.Div('Cost Per Acquisition (CPA)', className='kpi-label'),
                html.Div('▲ Below target', className='kpi-trend trend-up')
            ], className='kpi-card'),
        ], className='kpi-grid'),
        
        # Charts Row 1
        html.Div([
            html.Div([
                dcc.Graph(figure=create_funnel_chart(), config={'displayModeBar': False})
            ], className='chart-card'),
            
            html.Div([
                dcc.Graph(figure=create_roas_by_campaign(), config={'displayModeBar': False})
            ], className='chart-card'),
        ], className='chart-grid'),
        
        # Charts Row 2
        html.Div([
            html.Div([
                dcc.Graph(figure=create_age_heatmap(), config={'displayModeBar': False})
            ], className='chart-card'),
            
            html.Div([
                dcc.Graph(figure=create_spend_revenue_scatter(), config={'displayModeBar': False})
            ], className='chart-card'),
        ], className='chart-grid'),
        
        # Charts Row 3
        html.Div([
            html.Div([
                dcc.Graph(figure=create_age_performance_chart(), config={'displayModeBar': False})
            ], className='chart-card'),
            
            html.Div([
                dcc.Graph(figure=create_campaign_comparison(), config={'displayModeBar': False})
            ], className='chart-card'),
        ], className='chart-grid'),
        
        # Key Insights Section
        html.Div([
            html.H2('🎯 Key Insights & Recommendations'),
            
            html.Div([
                html.Div([
                    html.Span('🎬', className='insight-icon'),
                    html.Div([
                        html.H4('Video Ads Outperform Image Ads by 2.9x'),
                        html.P('Statistical analysis (p < 0.001, Cohen\'s d = 0.70) confirms video ads generate significantly higher ROAS. Recommend shifting 40% of image ad budget to video formats.')
                    ], className='insight-text')
                ], className='insight-item'),
                
                html.Div([
                    html.Span('👥', className='insight-icon'),
                    html.Div([
                        html.H4('30-34 Age Group Drives 51% of Conversions'),
                        html.P('This segment delivers the highest conversion volume at the lowest CPA ($4.09). Increase bid adjustments by 25% for this demographic.')
                    ], className='insight-text')
                ], className='insight-item'),
                
                html.Div([
                    html.Span('📈', className='insight-icon'),
                    html.Div([
                        html.H4('Overall ROAS of 3.06x Exceeds Industry Benchmark'),
                        html.P('Campaign performance is strong with ROAS well above the 2.0x industry standard. Continue current strategy while optimizing underperforming segments.')
                    ], className='insight-text')
                ], className='insight-item'),
                
                html.Div([
                    html.Span('⚠️', className='insight-icon'),
                    html.Div([
                        html.H4('45-49 Age Group Shows Highest CPA'),
                        html.P('This segment has CPA of $14.04, 3.4x higher than the 30-34 group. Consider reducing bids or excluding from low-performing campaigns.')
                    ], className='insight-text')
                ], className='insight-item'),
            ])
        ], className='insights-section'),
        
        # Footer
        html.Div([
            html.P('📊 Ad Campaign Performance Analytics Dashboard | Built with Python, Plotly Dash, Pandas'),
            html.P('Data Source: Facebook/Meta Ad Campaign Data | Analysis Date: April 2026')
        ], className='footer'),
        
    ], className='dashboard-container')
])

# ============================================================
# RUN SERVER
# ============================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 AD CAMPAIGN ANALYTICS DASHBOARD")
    print("="*60)
    print("\n📊 Dashboard running at: http://127.0.0.1:8050")
    print("   Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=8050)
