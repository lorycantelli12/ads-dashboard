"""
Dashboard de Ads Analytics - Estilo Full Cycle
Dashboard profissional com tema dark
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Dashboard Ads Analytics - Full Cycle Style",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado - Tema Full Cycle Dark
st.markdown("""
    <style>
    /* Fundo preto total */
    .stApp {
        background-color: #000000;
    }

    /* Header */
    .main-header {
        background-color: #000000;
        color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }

    .logo-text {
        font-size: 2rem;
        font-weight: bold;
        color: #FFFFFF;
    }

    .logo-yellow {
        color: #FFD700;
    }

    /* Cards de métricas principais */
    .metric-card-white {
        background-color: #FFFFFF;
        color: #000000;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(255,255,255,0.1);
        margin: 0.5rem;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #666;
        font-weight: 500;
    }

    /* Cards de qualificação coloridos */
    .qual-card {
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.3rem;
        border: 2px solid rgba(255,255,255,0.1);
    }

    .qual-percentage {
        font-size: 1.8rem;
        font-weight: bold;
        color: #FFFFFF;
    }

    .qual-value {
        font-size: 1.3rem;
        font-weight: 600;
        color: #FFFFFF;
        margin: 0.5rem 0;
    }

    .qual-count {
        font-size: 1.5rem;
        font-weight: bold;
        color: #FFFFFF;
    }

    .qual-label {
        font-size: 0.8rem;
        color: rgba(255,255,255,0.8);
    }

    /* Cores das qualificações */
    .qual-0 { background-color: #E57373; }
    .qual-1 { background-color: #FFAB91; }
    .qual-2 { background-color: #FFD54F; }
    .qual-3 { background-color: #DCE775; }
    .qual-4 { background-color: #81C784; }
    .qual-5 { background-color: #4FC3F7; }

    /* Texto branco */
    h1, h2, h3, h4, h5, p, span, div {
        color: #FFFFFF !important;
    }

    /* Remover padding padrão */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0;
    }
    </style>
""", unsafe_allow_html=True)


def generate_sample_data():
    """Gera dados de exemplo no estilo Full Cycle"""
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')

    data = []

    for date in dates:
        # Meta Ads (Facebook)
        fb_impressions = int(np.random.normal(80000, 10000))
        fb_clicks = int(fb_impressions * np.random.uniform(0.005, 0.008))
        fb_leads = int(fb_clicks * np.random.uniform(0.20, 0.30))
        fb_spend = round(np.random.uniform(1500, 2500), 2)

        data.append({
            'data': date,
            'plataforma': 'Meta',
            'impressoes': fb_impressions,
            'cliques': fb_clicks,
            'leads': fb_leads,
            'gasto': fb_spend,
            'cpl': round(fb_spend / fb_leads if fb_leads > 0 else 0, 2),
            'cpc': round(fb_spend / fb_clicks if fb_clicks > 0 else 0, 2),
            'ctr': round((fb_clicks / fb_impressions * 100) if fb_impressions > 0 else 0, 3),
            'cpm': round((fb_spend / fb_impressions * 1000) if fb_impressions > 0 else 0, 2),
        })

        # Google Ads
        gg_impressions = int(np.random.normal(30000, 5000))
        gg_clicks = int(gg_impressions * np.random.uniform(0.004, 0.007))
        gg_leads = int(gg_clicks * np.random.uniform(0.15, 0.25))
        gg_spend = round(np.random.uniform(800, 1500), 2)

        data.append({
            'data': date,
            'plataforma': 'Google',
            'impressoes': gg_impressions,
            'cliques': gg_clicks,
            'leads': gg_leads,
            'gasto': gg_spend,
            'cpl': round(gg_spend / gg_leads if gg_leads > 0 else 0, 2),
            'cpc': round(gg_spend / gg_clicks if gg_clicks > 0 else 0, 2),
            'ctr': round((gg_clicks / gg_impressions * 100) if gg_impressions > 0 else 0, 3),
            'cpm': round((gg_spend / gg_impressions * 1000) if gg_impressions > 0 else 0, 2),
        })

    df = pd.DataFrame(data)

    # Adicionar qualificação de leads
    df['cpl_0'] = (df['leads'] * np.random.uniform(0.20, 0.30)).astype(int)
    df['cpl_1'] = (df['leads'] * np.random.uniform(0.04, 0.06)).astype(int)
    df['cpl_2'] = (df['leads'] * np.random.uniform(0.12, 0.15)).astype(int)
    df['cpl_3'] = (df['leads'] * np.random.uniform(0.18, 0.22)).astype(int)
    df['cpl_4'] = (df['leads'] * np.random.uniform(0.13, 0.17)).astype(int)
    df['cpl_5'] = (df['leads'] * np.random.uniform(0.20, 0.25)).astype(int)

    return df


def create_header():
    """Cria header estilo Full Cycle"""
    st.markdown("""
        <div class="main-header">
            <span class="logo-text">Full<span class="logo-yellow">Cycle</span></span>
            <span style="margin-left: 2rem; font-size: 1.2rem;">Dashboard de Ads - Lançamento</span>
            <span style="float: right; font-size: 1rem;">📊 Meta Ads | Google Ads | LinkedIn Ads</span>
        </div>
    """, unsafe_allow_html=True)


def create_qualification_cards(df):
    """Cria cards de qualificação coloridos"""
    st.markdown("### Qualificação")

    # Calcular totais por CPL
    total_leads = df['leads'].sum()

    cpl_data = []
    for i in range(6):
        count = df[f'cpl_{i}'].sum()
        percentage = (count / total_leads * 100) if total_leads > 0 else 0
        avg_value = df['gasto'].sum() * (percentage / 100) / count if count > 0 else 0

        cpl_data.append({
            'cpl': i,
            'percentage': percentage,
            'value': avg_value,
            'count': count
        })

    # Criar 6 colunas
    cols = st.columns(6)

    colors = ['qual-0', 'qual-1', 'qual-2', 'qual-3', 'qual-4', 'qual-5']

    for idx, (col, data) in enumerate(zip(cols, cpl_data)):
        with col:
            st.markdown(f"""
                <div class="qual-card {colors[idx]}">
                    <div class="qual-label">% {idx}</div>
                    <div class="qual-percentage">{data['percentage']:.2f}%</div>
                    <div class="qual-label">CPL {idx}</div>
                    <div class="qual-value">R$ {data['value']:.2f}</div>
                    <div class="qual-label">{idx}</div>
                    <div class="qual-count">{int(data['count'])}</div>
                </div>
            """, unsafe_allow_html=True)


def create_main_metrics(df):
    """Cria métricas principais em cards brancos"""
    st.markdown("### Principais Indicadores")

    total_invest = df['gasto'].sum()
    total_leads = df['leads'].sum()
    avg_cpl = total_invest / total_leads if total_leads > 0 else 0
    fb_leads = df[df['plataforma'] == 'Meta']['leads'].sum()
    gg_leads = df[df['plataforma'] == 'Google']['leads'].sum()

    cols = st.columns(6)

    metrics = [
        ("Investimento", f"R$ {total_invest:,.2f}"),
        ("CPL (Pago)", f"R$ {avg_cpl:.2f}"),
        ("Leads (Total)", f"{int(total_leads):,}"),
        ("Leads Facebook", f"{int(fb_leads):,}"),
        ("Leads Google", f"{int(gg_leads):,}"),
        ("% Confiabilidade", "99,50%"),
    ]

    for col, (label, value) in zip(cols, metrics):
        with col:
            st.markdown(f"""
                <div class="metric-card-white">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
            """, unsafe_allow_html=True)


def create_cpl_leads_chart(df):
    """Gráfico CPL/Leads por Dia"""
    daily_data = df.groupby(['data', 'plataforma']).agg({
        'leads': 'sum',
        'cpl': 'mean',
        'gasto': 'sum'
    }).reset_index()

    fig = go.Figure()

    # Barras de leads por plataforma
    for platform in ['Meta', 'Google']:
        platform_data = daily_data[daily_data['plataforma'] == platform]
        color = '#FFD700' if platform == 'Meta' else '#FF7043'

        fig.add_trace(go.Bar(
            x=platform_data['data'],
            y=platform_data['leads'],
            name=f'Leads {platform}',
            marker_color=color,
            yaxis='y'
        ))

    # Linha de CPL
    fig.add_trace(go.Scatter(
        x=daily_data['data'],
        y=daily_data['cpl'],
        name='CPL',
        mode='lines+markers',
        line=dict(color='#FFFFFF', width=2),
        marker=dict(size=6),
        yaxis='y2'
    ))

    fig.update_layout(
        title="CPL (Pago) / Leads x Dia",
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font=dict(color='#FFFFFF'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#333333',
            title="Data"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#333333',
            title="Leads",
            side='left'
        ),
        yaxis2=dict(
            showgrid=False,
            title="CPL (R$)",
            side='right',
            overlaying='y'
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(0,0,0,0.5)'
        ),
        height=400,
        shapes=[{
            'type': 'rect',
            'xref': 'paper',
            'yref': 'paper',
            'x0': 0,
            'y0': 0,
            'x1': 1,
            'y1': 1,
            'line': {
                'color': '#FFD700',
                'width': 2,
                'dash': 'dash'
            }
        }]
    )

    return fig


def create_spend_chart(df):
    """Gráfico de Gasto x Dia (área)"""
    daily_spend = df.groupby('data')['gasto'].sum().reset_index()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=daily_spend['data'],
        y=daily_spend['gasto'],
        fill='tozeroy',
        fillcolor='rgba(33, 150, 243, 0.7)',
        line=dict(color='#2196F3', width=2),
        name='Gasto'
    ))

    fig.update_layout(
        title="Gasto x Dia",
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font=dict(color='#FFFFFF'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#333333',
            title="Data"
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#333333',
            title="Gasto (R$)"
        ),
        height=350,
        showlegend=False,
        shapes=[{
            'type': 'rect',
            'xref': 'paper',
            'yref': 'paper',
            'x0': 0,
            'y0': 0,
            'x1': 1,
            'y1': 1,
            'line': {
                'color': '#FFD700',
                'width': 2,
                'dash': 'dash'
            }
        }]
    )

    return fig


def create_metrics_charts(df):
    """Gráficos de métricas (CPM, CPC, CTR)"""
    daily_metrics = df.groupby(['data', 'plataforma']).agg({
        'cpm': 'mean',
        'cpc': 'mean',
        'ctr': 'mean'
    }).reset_index()

    charts = []
    metrics = [
        ('cpm', 'CPM'),
        ('cpc', 'CPC'),
        ('ctr', 'CTR')
    ]

    for metric_col, metric_name in metrics:
        fig = go.Figure()

        colors = {'Meta': '#2196F3', 'Google': '#FF5722'}

        for platform in ['Meta', 'Google']:
            platform_data = daily_metrics[daily_metrics['plataforma'] == platform]

            fig.add_trace(go.Scatter(
                x=platform_data['data'],
                y=platform_data[metric_col],
                name=f'{metric_name} {platform}',
                mode='lines+markers',
                line=dict(color=colors[platform], width=2),
                marker=dict(size=5)
            ))

        fig.update_layout(
            title=metric_name,
            plot_bgcolor='#000000',
            paper_bgcolor='#000000',
            font=dict(color='#FFFFFF'),
            xaxis=dict(
                showgrid=True,
                gridcolor='#333333',
                title=""
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#333333',
                title=metric_name
            ),
            height=300,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.2,
                xanchor="center",
                x=0.5,
                bgcolor='rgba(0,0,0,0.5)'
            ),
            margin=dict(l=50, r=50, t=50, b=50),
            shapes=[{
                'type': 'rect',
                'xref': 'paper',
                'yref': 'paper',
                'x0': 0,
                'y0': 0,
                'x1': 1,
                'y1': 1,
                'line': {
                    'color': '#FFD700',
                    'width': 2,
                    'dash': 'dash'
                }
            }]
        )

        charts.append(fig)

    return charts


def main():
    """Função principal"""

    # Header
    create_header()

    # Carregar dados
    df = generate_sample_data()

    # Métricas principais
    create_main_metrics(df)

    st.markdown("<br>", unsafe_allow_html=True)

    # Cards de qualificação
    create_qualification_cards(df)

    st.markdown("<br>", unsafe_allow_html=True)

    # Gráfico CPL/Leads
    st.plotly_chart(create_cpl_leads_chart(df), use_container_width=True)

    # Gráfico de Gasto
    st.plotly_chart(create_spend_chart(df), use_container_width=True)

    st.markdown("### Métricas Gerais")

    # Gráficos de métricas em 3 colunas
    charts = create_metrics_charts(df)
    cols = st.columns(3)

    for col, chart in zip(cols, charts):
        with col:
            st.plotly_chart(chart, use_container_width=True)

    # Tabela de resumo
    st.markdown("### Resumo Diário")

    daily_summary = df.groupby('data').agg({
        'gasto': 'sum',
        'leads': 'sum',
        'cpl': 'mean',
        'cpl_0': 'sum',
        'cpl_1': 'sum',
        'cpl_2': 'sum',
        'cpl_3': 'sum',
        'cpl_4': 'sum',
        'cpl_5': 'sum',
    }).reset_index()

    daily_summary['data'] = daily_summary['data'].dt.strftime('%d/%m')
    daily_summary = daily_summary.sort_values('data', ascending=False)

    st.dataframe(
        daily_summary,
        use_container_width=True,
        hide_index=True,
        height=400
    )


if __name__ == "__main__":
    main()
