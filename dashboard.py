"""
Dashboard de Analytics de Ads
Visualização unificada de métricas de Meta Ads, LinkedIn Ads e Google Ads
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.append(str(Path(__file__).resolve().parent))

from src.google_sheets.client import GoogleSheetsClient
from config.settings import GOOGLE_SHEETS_CONFIG

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Ads Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)


# Função para gerar dados de exemplo
@st.cache_data
def generate_sample_data():
    """Gera dados de exemplo para demonstração"""
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')

    data = []
    platforms = ['Meta Ads', 'Google Ads', 'LinkedIn Ads']

    for platform in platforms:
        for date in dates:
            # Gerar métricas aleatórias mas realistas
            base_multiplier = {
                'Meta Ads': 1.0,
                'Google Ads': 0.8,
                'LinkedIn Ads': 0.6
            }[platform]

            impressions = int(np.random.normal(10000, 2000) * base_multiplier)
            clicks = int(impressions * np.random.uniform(0.02, 0.05))
            spend = round(np.random.uniform(200, 500) * base_multiplier, 2)
            conversions = int(clicks * np.random.uniform(0.05, 0.15))

            data.append({
                'data': date,
                'plataforma': platform,
                'impressoes': impressions,
                'cliques': clicks,
                'gasto': spend,
                'conversoes': conversions,
                'cpc': round(spend / clicks if clicks > 0 else 0, 2),
                'ctr': round((clicks / impressions * 100) if impressions > 0 else 0, 2),
                'taxa_conversao': round((conversions / clicks * 100) if clicks > 0 else 0, 2),
                'cpa': round(spend / conversions if conversions > 0 else 0, 2),
            })

    return pd.DataFrame(data)


def load_data():
    """Carrega dados do Google Sheets ou usa dados de exemplo"""
    try:
        if GOOGLE_SHEETS_CONFIG['spreadsheet_id']:
            sheets_client = GoogleSheetsClient()
            data = sheets_client.read_all_data()

            if data:
                df = pd.DataFrame(data)
                if 'data' in df.columns:
                    df['data'] = pd.to_datetime(df['data'])
                st.sidebar.success("✅ Dados carregados do Google Sheets")
                return df
    except Exception as e:
        st.sidebar.warning(f"⚠️ Usando dados de exemplo: {str(e)}")

    return generate_sample_data()


def calculate_kpis(df):
    """Calcula KPIs principais"""
    total_impressions = df['impressoes'].sum()
    total_clicks = df['cliques'].sum()
    total_spend = df['gasto'].sum()
    total_conversions = df['conversoes'].sum()

    avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    avg_cpc = total_spend / total_clicks if total_clicks > 0 else 0
    avg_cpa = total_spend / total_conversions if total_conversions > 0 else 0
    conversion_rate = (total_conversions / total_clicks * 100) if total_clicks > 0 else 0

    return {
        'total_impressions': int(total_impressions),
        'total_clicks': int(total_clicks),
        'total_spend': round(total_spend, 2),
        'total_conversions': int(total_conversions),
        'avg_ctr': round(avg_ctr, 2),
        'avg_cpc': round(avg_cpc, 2),
        'avg_cpa': round(avg_cpa, 2),
        'conversion_rate': round(conversion_rate, 2),
    }


def main():
    """Função principal do dashboard"""

    # Header
    st.markdown('<h1 class="main-header">📊 Dashboard de Ads Analytics</h1>', unsafe_allow_html=True)
    st.markdown("---")

    # Carregar dados
    df = load_data()

    # Sidebar - Filtros
    st.sidebar.header("🔍 Filtros")

    # Filtro de data
    date_range = st.sidebar.selectbox(
        "Período",
        ["Últimos 7 dias", "Últimos 30 dias", "Últimos 90 dias", "Personalizado"]
    )

    if date_range == "Últimos 7 dias":
        start_date = datetime.now() - timedelta(days=7)
    elif date_range == "Últimos 30 dias":
        start_date = datetime.now() - timedelta(days=30)
    elif date_range == "Últimos 90 dias":
        start_date = datetime.now() - timedelta(days=90)
    else:
        col1, col2 = st.sidebar.columns(2)
        with col1:
            start_date = st.date_input("De", datetime.now() - timedelta(days=30))
        with col2:
            end_date = st.date_input("Até", datetime.now())

    # Filtro de plataforma
    platforms = ['Todas'] + list(df['plataforma'].unique())
    selected_platform = st.sidebar.selectbox("Plataforma", platforms)

    # Aplicar filtros
    df_filtered = df[df['data'] >= pd.Timestamp(start_date)]
    if selected_platform != 'Todas':
        df_filtered = df_filtered[df_filtered['plataforma'] == selected_platform]

    # Calcular KPIs
    kpis = calculate_kpis(df_filtered)

    # Exibir KPIs principais
    st.subheader("📈 KPIs Principais")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="💰 Gasto Total",
            value=f"R$ {kpis['total_spend']:,.2f}",
            delta=None
        )

    with col2:
        st.metric(
            label="👁️ Impressões",
            value=f"{kpis['total_impressions']:,}",
            delta=None
        )

    with col3:
        st.metric(
            label="🖱️ Cliques",
            value=f"{kpis['total_clicks']:,}",
            delta=f"{kpis['avg_ctr']}% CTR"
        )

    with col4:
        st.metric(
            label="✅ Conversões",
            value=f"{kpis['total_conversions']:,}",
            delta=f"{kpis['conversion_rate']}% Taxa"
        )

    # Segunda linha de KPIs
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric(
            label="CPC Médio",
            value=f"R$ {kpis['avg_cpc']:.2f}",
            delta=None
        )

    with col6:
        st.metric(
            label="CPA Médio",
            value=f"R$ {kpis['avg_cpa']:.2f}",
            delta=None
        )

    with col7:
        st.metric(
            label="CTR Médio",
            value=f"{kpis['avg_ctr']:.2f}%",
            delta=None
        )

    with col8:
        st.metric(
            label="Taxa de Conversão",
            value=f"{kpis['conversion_rate']:.2f}%",
            delta=None
        )

    st.markdown("---")

    # Gráficos
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "📈 Tendências", "🎯 Comparação", "📋 Dados Detalhados"])

    with tab1:
        st.subheader("Visão Geral de Performance")

        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de Gasto por Plataforma
            spend_by_platform = df_filtered.groupby('plataforma')['gasto'].sum().reset_index()
            fig_spend = px.pie(
                spend_by_platform,
                values='gasto',
                names='plataforma',
                title='💰 Distribuição de Gasto por Plataforma',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig_spend.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_spend, use_container_width=True)

        with col2:
            # Gráfico de Conversões por Plataforma
            conv_by_platform = df_filtered.groupby('plataforma')['conversoes'].sum().reset_index()
            fig_conv = px.bar(
                conv_by_platform,
                x='plataforma',
                y='conversoes',
                title='✅ Conversões por Plataforma',
                color='plataforma',
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_conv.update_layout(showlegend=False)
            st.plotly_chart(fig_conv, use_container_width=True)

    with tab2:
        st.subheader("Tendências Temporais")

        # Métricas ao longo do tempo
        metric_choice = st.selectbox(
            "Selecione a métrica",
            ["gasto", "impressoes", "cliques", "conversoes", "ctr", "cpc"]
        )

        metric_labels = {
            "gasto": "Gasto (R$)",
            "impressoes": "Impressões",
            "cliques": "Cliques",
            "conversoes": "Conversões",
            "ctr": "CTR (%)",
            "cpc": "CPC (R$)"
        }

        trend_data = df_filtered.groupby(['data', 'plataforma'])[metric_choice].sum().reset_index()

        fig_trend = px.line(
            trend_data,
            x='data',
            y=metric_choice,
            color='plataforma',
            title=f'📈 Evolução de {metric_labels[metric_choice]} ao Longo do Tempo',
            markers=True
        )
        fig_trend.update_xaxis(title="Data")
        fig_trend.update_yaxis(title=metric_labels[metric_choice])
        st.plotly_chart(fig_trend, use_container_width=True)

    with tab3:
        st.subheader("Comparação entre Plataformas")

        col1, col2 = st.columns(2)

        with col1:
            # Comparação de CTR
            ctr_comparison = df_filtered.groupby('plataforma')['ctr'].mean().reset_index()
            fig_ctr = px.bar(
                ctr_comparison,
                x='plataforma',
                y='ctr',
                title='🎯 CTR Médio por Plataforma',
                color='ctr',
                color_continuous_scale='Blues'
            )
            fig_ctr.update_yaxis(title="CTR Médio (%)")
            st.plotly_chart(fig_ctr, use_container_width=True)

        with col2:
            # Comparação de CPC
            cpc_comparison = df_filtered.groupby('plataforma')['cpc'].mean().reset_index()
            fig_cpc = px.bar(
                cpc_comparison,
                x='plataforma',
                y='cpc',
                title='💵 CPC Médio por Plataforma',
                color='cpc',
                color_continuous_scale='Greens'
            )
            fig_cpc.update_yaxis(title="CPC Médio (R$)")
            st.plotly_chart(fig_cpc, use_container_width=True)

    with tab4:
        st.subheader("Dados Detalhados")

        # Tabela de dados
        df_display = df_filtered.copy()
        df_display['data'] = df_display['data'].dt.strftime('%Y-%m-%d')
        df_display = df_display.sort_values('data', ascending=False)

        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )

        # Botão de download
        csv = df_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"ads_analytics_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 1rem;'>
            Dashboard de Ads Analytics | Atualizado automaticamente |
            Dados de: Meta Ads, Google Ads, LinkedIn Ads
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
