"""
Dashboard Meta Ads - APENAS DADOS REAIS
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))
from src.meta_ads.client import MetaAdsClient

# Configuração
st.set_page_config(
    page_title="Meta Ads Dashboard - Fabrício",
    page_icon="📘",
    layout="wide"
)

# CSS Tema Dark
st.markdown("""
    <style>
    /* Fundo preto */
    .stApp {
        background-color: #000000;
    }

    /* Texto branco */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #FFFFFF !important;
    }

    /* Métricas com fundo branco */
    [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-size: 2rem !important;
        font-weight: bold !important;
    }

    [data-testid="stMetricLabel"] {
        color: #666666 !important;
        font-size: 0.9rem !important;
    }

    /* Container das métricas */
    [data-testid="metric-container"] {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(255,255,255,0.1);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #FFFFFF !important;
    }

    /* Selectbox na sidebar */
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: #2d2d2d;
    }

    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #2d2d2d;
        color: #FFFFFF !important;
    }

    /* Dropdown do selectbox */
    [data-baseweb="popover"] {
        background-color: #2d2d2d !important;
    }

    [data-baseweb="popover"] ul {
        background-color: #2d2d2d !important;
    }

    [data-baseweb="popover"] li {
        background-color: #2d2d2d !important;
        color: #FFFFFF !important;
    }

    [data-baseweb="popover"] li:hover {
        background-color: #FFD700 !important;
        color: #000000 !important;
    }

    /* Texto dentro do menu dropdown */
    [role="option"] {
        color: #FFFFFF !important;
    }

    /* Botões */
    .stButton button {
        background-color: #FFD700;
        color: #000000;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=600)
def load_data(days):
    """Carrega dados REAIS do Meta"""
    try:
        client = MetaAdsClient()
        date_from = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        date_to = datetime.now().strftime('%Y-%m-%d')

        result = client.get_daily_summary(date_from, date_to)

        if result['success']:
            return pd.DataFrame(result['data']), None
        return None, result.get('error')
    except Exception as e:
        return None, str(e)


def main():
    # Header
    st.markdown("""
        <div style='background:#000; padding:1.5rem; border-radius:10px; margin-bottom:2rem; border: 2px solid #FFD700;'>
            <h1 style='margin:0; color:#FFF !important;'>
                Fabr<span style='color:#FFD700;'>ício</span>
                <span style='font-size:1.2rem; margin-left:2rem; font-weight:normal;'>Meta Ads - Dashboard</span>
            </h1>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.header("🔍 Filtros")
    days = st.sidebar.selectbox("Período", [7, 15, 30], index=0, format_func=lambda x: f"Últimos {x} dias")

    if st.sidebar.button("🔄 Atualizar Dados"):
        st.cache_data.clear()
        st.rerun()

    # Carregar dados
    with st.spinner('📥 Carregando dados do Meta Ads...'):
        df, error = load_data(days)

    if error:
        st.error(f"❌ Erro ao carregar dados: {error}")
        st.stop()

    if df is None or len(df) == 0:
        st.warning("⚠️ Nenhum dado encontrado para este período")
        st.stop()

    st.success(f"✅ {len(df)} dias carregados")

    # Calcular totais
    total_spend = df['spend'].sum()
    total_leads = int(df['leads'].sum())
    total_impressions = int(df['impressions'].sum())
    total_clicks = int(df['clicks'].sum())
    total_conversions = int(df['conversions'].sum())

    avg_cpl = total_spend / total_leads if total_leads > 0 else 0
    avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    avg_cpc = total_spend / total_clicks if total_clicks > 0 else 0
    avg_cpm = df['cpm'].mean()

    # Métricas Principais
    st.markdown("## 📊 Principais Indicadores")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="💰 Investimento Total",
            value=f"R$ {total_spend:,.2f}"
        )

    with col2:
        st.metric(
            label="📋 Total de Leads",
            value=f"{total_leads:,}"
        )

    with col3:
        st.metric(
            label="💵 CPL Médio",
            value=f"R$ {avg_cpl:.2f}"
        )

    with col4:
        st.metric(
            label="📈 CTR Médio",
            value=f"{avg_ctr:.2f}%"
        )

    # Segunda linha de métricas
    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.metric(
            label="👁️ Impressões",
            value=f"{total_impressions:,}"
        )

    with col6:
        st.metric(
            label="🖱️ Cliques",
            value=f"{total_clicks:,}"
        )

    with col7:
        st.metric(
            label="💲 CPC Médio",
            value=f"R$ {avg_cpc:.2f}"
        )

    with col8:
        st.metric(
            label="📊 CPM Médio",
            value=f"R$ {avg_cpm:.2f}"
        )

    st.markdown("---")

    # Gráficos
    st.markdown("## 📈 Gráficos")

    # Leads e CPL por dia
    fig1 = go.Figure()

    fig1.add_trace(go.Bar(
        x=df['date'],
        y=df['leads'],
        name='Leads',
        marker_color='#FFD700',
        yaxis='y'
    ))

    fig1.add_trace(go.Scatter(
        x=df['date'],
        y=df['cpl'],
        name='CPL (R$)',
        mode='lines+markers',
        line=dict(color='#FFFFFF', width=3),
        marker=dict(size=8, color='#FF5722'),
        yaxis='y2'
    ))

    fig1.update_layout(
        title="Leads e CPL por Dia",
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font=dict(color='#FFFFFF', size=12),
        xaxis=dict(
            showgrid=True,
            gridcolor='#333333',
            title="Data"
        ),
        yaxis=dict(
            title="Leads",
            showgrid=True,
            gridcolor='#333333',
            side='left'
        ),
        yaxis2=dict(
            title="CPL (R$)",
            overlaying='y',
            side='right',
            showgrid=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=450,
        hovermode='x unified'
    )

    st.plotly_chart(fig1, use_container_width=True)

    # Gasto por dia
    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        x=df['date'],
        y=df['spend'],
        fill='tozeroy',
        fillcolor='rgba(33, 150, 243, 0.7)',
        line=dict(color='#2196F3', width=3),
        name='Gasto (R$)'
    ))

    fig2.update_layout(
        title="Gasto por Dia",
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font=dict(color='#FFFFFF', size=12),
        xaxis=dict(
            showgrid=True,
            gridcolor='#333333',
            title="Data"
        ),
        yaxis=dict(
            title="Gasto (R$)",
            showgrid=True,
            gridcolor='#333333'
        ),
        showlegend=False,
        height=400,
        hovermode='x unified'
    )

    st.plotly_chart(fig2, use_container_width=True)

    # Métricas em 3 colunas
    st.markdown("### Evolução de Métricas")

    col1, col2, col3 = st.columns(3)

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['cpm'],
            mode='lines+markers',
            line=dict(color='#2196F3', width=2),
            marker=dict(size=6),
            name='CPM'
        ))
        fig.update_layout(
            title="CPM (Custo por Mil)",
            plot_bgcolor='#000000',
            paper_bgcolor='#000000',
            font=dict(color='#FFFFFF'),
            xaxis=dict(showgrid=True, gridcolor='#333333'),
            yaxis=dict(showgrid=True, gridcolor='#333333', title="R$"),
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['cpc'],
            mode='lines+markers',
            line=dict(color='#FF5722', width=2),
            marker=dict(size=6),
            name='CPC'
        ))
        fig.update_layout(
            title="CPC (Custo por Clique)",
            plot_bgcolor='#000000',
            paper_bgcolor='#000000',
            font=dict(color='#FFFFFF'),
            xaxis=dict(showgrid=True, gridcolor='#333333'),
            yaxis=dict(showgrid=True, gridcolor='#333333', title="R$"),
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['ctr'],
            mode='lines+markers',
            line=dict(color='#4CAF50', width=2),
            marker=dict(size=6),
            name='CTR'
        ))
        fig.update_layout(
            title="CTR (Taxa de Cliques)",
            plot_bgcolor='#000000',
            paper_bgcolor='#000000',
            font=dict(color='#FFFFFF'),
            xaxis=dict(showgrid=True, gridcolor='#333333'),
            yaxis=dict(showgrid=True, gridcolor='#333333', title="%"),
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Tabela
    st.markdown("## 📋 Dados Diários Detalhados")

    display_df = df.copy()
    display_df['date'] = pd.to_datetime(display_df['date']).dt.strftime('%d/%m/%Y')
    display_df = display_df.sort_values('date', ascending=False)

    # Formatar valores
    display_df['spend'] = display_df['spend'].apply(lambda x: f"R$ {x:,.2f}")
    display_df['cpl'] = display_df['cpl'].apply(lambda x: f"R$ {x:.2f}")
    display_df['cpc'] = display_df['cpc'].apply(lambda x: f"R$ {x:.2f}")
    display_df['cpm'] = display_df['cpm'].apply(lambda x: f"R$ {x:.2f}")
    display_df['ctr'] = display_df['ctr'].apply(lambda x: f"{x:.2f}%")
    display_df['conversion_rate'] = display_df['conversion_rate'].apply(lambda x: f"{x:.2f}%")

    # Selecionar e renomear colunas
    display_df = display_df[['date', 'spend', 'impressions', 'clicks', 'leads', 'conversions', 'cpl', 'cpc', 'cpm', 'ctr', 'conversion_rate']]
    display_df.columns = ['Data', 'Gasto', 'Impressões', 'Cliques', 'Leads', 'Conversões', 'CPL', 'CPC', 'CPM', 'CTR', 'Taxa Conversão']

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=400
    )

    # Info no sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Resumo")
    st.sidebar.markdown(f"""
    <div style='background-color:#2d2d2d; padding:1rem; border-radius:8px; border-left:4px solid #FFD700;'>
        <p style='color:#FFF; margin:0.3rem 0;'><strong>Período:</strong> {days} dias</p>
        <p style='color:#FFF; margin:0.3rem 0;'><strong>Total gasto:</strong> R$ {total_spend:,.2f}</p>
        <p style='color:#FFF; margin:0.3rem 0;'><strong>Total leads:</strong> {total_leads}</p>
        <p style='color:#FFF; margin:0.3rem 0;'><strong>Total conversões:</strong> {total_conversions}</p>
        <p style='color:#FFD700; margin:0.3rem 0;'><strong>Atualizado:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)

    # Download CSV
    st.sidebar.markdown("---")
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"meta_ads_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )


if __name__ == "__main__":
    main()
