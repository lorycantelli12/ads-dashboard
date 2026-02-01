"""
Configurações centralizadas do Dashboard de Ads
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Carregar variáveis de ambiente
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# Detectar se está rodando no Streamlit Cloud
try:
    import streamlit as st
    # Se st.secrets existe, estamos no Streamlit Cloud
    _USE_STREAMLIT_SECRETS = hasattr(st, 'secrets') and len(st.secrets) > 0
except:
    _USE_STREAMLIT_SECRETS = False

def get_env(key, default=''):
    """Pega variável do Streamlit secrets ou do .env"""
    if _USE_STREAMLIT_SECRETS:
        try:
            import streamlit as st
            return st.secrets.get(key, default)
        except:
            pass
    return os.getenv(key, default)

# Configurações Gerais
DEBUG = get_env('DEBUG', 'False').lower() == 'true'
TIMEZONE = get_env('TIMEZONE', 'America/Sao_Paulo')

# Diretórios
CREDENTIALS_DIR = BASE_DIR / 'credentials'
DATA_DIR = BASE_DIR / 'data'
LOGS_DIR = BASE_DIR / 'logs'

# Criar diretórios se não existirem
for directory in [CREDENTIALS_DIR, DATA_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)

# ===========================
# GOOGLE SHEETS
# ===========================
GOOGLE_SHEETS_CONFIG = {
    'credentials_file': get_env('GOOGLE_SHEETS_CREDENTIALS_FILE'),
    'spreadsheet_id': get_env('GOOGLE_SHEETS_SPREADSHEET_ID'),
    'config_tab': get_env('GOOGLE_SHEETS_CONFIG_TAB', 'Config'),
    'data_tab': get_env('GOOGLE_SHEETS_DATA_TAB', 'Dados'),
}

# ===========================
# META ADS
# ===========================
META_ADS_CONFIG = {
    'access_token': get_env('META_ACCESS_TOKEN'),
    'ad_account_id': get_env('META_AD_ACCOUNT_ID'),
    'campaign_ids': [
        cid.strip()
        for cid in get_env('META_CAMPAIGN_IDS', '').split(',')
        if cid.strip()
    ],
}

# ===========================
# LINKEDIN ADS
# ===========================
LINKEDIN_ADS_CONFIG = {
    'access_token': get_env('LINKEDIN_ACCESS_TOKEN'),
    'ad_account_id': get_env('LINKEDIN_AD_ACCOUNT_ID'),
    'campaign_ids': [
        cid.strip()
        for cid in get_env('LINKEDIN_CAMPAIGN_IDS', '').split(',')
        if cid.strip()
    ],
}

# ===========================
# GOOGLE ADS
# ===========================
GOOGLE_ADS_CONFIG = {
    'developer_token': get_env('GOOGLE_ADS_DEVELOPER_TOKEN'),
    'client_id': get_env('GOOGLE_ADS_CLIENT_ID'),
    'client_secret': get_env('GOOGLE_ADS_CLIENT_SECRET'),
    'refresh_token': get_env('GOOGLE_ADS_REFRESH_TOKEN'),
    'customer_id': get_env('GOOGLE_ADS_CUSTOMER_ID'),
    'login_customer_id': get_env('GOOGLE_ADS_LOGIN_CUSTOMER_ID'),
}

# ===========================
# COLETA AUTOMÁTICA
# ===========================
COLLECTION_CONFIG = {
    'frequency_hours': int(get_env('COLLECTION_FREQUENCY_HOURS', '24')),
    'collection_time': get_env('COLLECTION_TIME', '08:00'),
}

# ===========================
# DASHBOARD
# ===========================
DASHBOARD_CONFIG = {
    'port': int(get_env('STREAMLIT_PORT', '8501')),
    'theme': get_env('DASHBOARD_THEME', 'light'),
}

# ===========================
# MÉTRICAS PADRÃO
# ===========================
DEFAULT_METRICS = [
    'impressions',      # Impressões
    'clicks',           # Cliques
    'spend',            # Gasto
    'conversions',      # Conversões
    'cpc',              # Custo por clique
    'ctr',              # Taxa de cliques
    'cpm',              # Custo por mil impressões
    'conversion_rate',  # Taxa de conversão
    'roas',             # Retorno sobre gasto em anúncios
]

# Validação básica
def validate_config():
    """Valida se as configurações essenciais estão presentes"""
    errors = []

    # Google Sheets
    if not GOOGLE_SHEETS_CONFIG['spreadsheet_id']:
        errors.append("GOOGLE_SHEETS_SPREADSHEET_ID não configurado")

    if not GOOGLE_SHEETS_CONFIG['credentials_file']:
        errors.append("GOOGLE_SHEETS_CREDENTIALS_FILE não configurado")

    # Pelo menos uma plataforma de ads deve estar configurada
    platforms_configured = 0

    if META_ADS_CONFIG['access_token'] and META_ADS_CONFIG['ad_account_id']:
        platforms_configured += 1

    if LINKEDIN_ADS_CONFIG['access_token'] and LINKEDIN_ADS_CONFIG['ad_account_id']:
        platforms_configured += 1

    if all([
        GOOGLE_ADS_CONFIG['developer_token'],
        GOOGLE_ADS_CONFIG['client_id'],
        GOOGLE_ADS_CONFIG['refresh_token'],
        GOOGLE_ADS_CONFIG['customer_id']
    ]):
        platforms_configured += 1

    if platforms_configured == 0:
        errors.append("Nenhuma plataforma de ads configurada (Meta, LinkedIn ou Google)")

    return errors


if __name__ == '__main__':
    print("🔍 Validando configurações...\n")
    errors = validate_config()

    if errors:
        print("❌ Erros encontrados:")
        for error in errors:
            print(f"  • {error}")
        print("\n💡 Configure o arquivo .env antes de continuar")
    else:
        print("✅ Todas as configurações estão OK!")

        print("\n📊 Plataformas configuradas:")
        if META_ADS_CONFIG['access_token']:
            print("  ✓ Meta Ads (Facebook/Instagram)")
        if LINKEDIN_ADS_CONFIG['access_token']:
            print("  ✓ LinkedIn Ads")
        if GOOGLE_ADS_CONFIG['developer_token']:
            print("  ✓ Google Ads")

        print(f"\n📁 Diretórios:")
        print(f"  • Credenciais: {CREDENTIALS_DIR}")
        print(f"  • Dados: {DATA_DIR}")
        print(f"  • Logs: {LOGS_DIR}")
