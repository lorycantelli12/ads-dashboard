"""
Cliente para integração com Meta Ads API (Facebook/Instagram)
"""
import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime, timedelta
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adsinsights import AdsInsights

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from config.settings import META_ADS_CONFIG, LOGS_DIR


class MetaAdsClient:
    """Cliente para coletar dados do Meta Ads (Facebook/Instagram)"""

    def __init__(self):
        self.access_token = META_ADS_CONFIG['access_token']
        self.ad_account_id = META_ADS_CONFIG['ad_account_id']
        self.campaign_ids = META_ADS_CONFIG['campaign_ids']

        if not self.access_token:
            raise ValueError("META_ACCESS_TOKEN não configurado. Verifique o arquivo .env")

        if not self.ad_account_id:
            raise ValueError("META_AD_ACCOUNT_ID não configurado. Verifique o arquivo .env")

        # Inicializar API
        try:
            FacebookAdsApi.init(access_token=self.access_token)
            self.ad_account = AdAccount(self.ad_account_id)
            print(f"✅ Meta Ads API inicializada")
        except Exception as e:
            raise Exception(f"Erro ao inicializar Meta Ads API: {e}")

    def get_account_info(self):
        """Obtém informações da conta de anúncios"""
        try:
            account = self.ad_account.api_get(fields=[
                'name',
                'account_id',
                'currency',
                'account_status',
                'business_name'
            ])

            return {
                'success': True,
                'data': account,
                'message': 'Conta válida'
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_campaigns(self):
        """Lista todas as campanhas da conta"""
        try:
            campaigns = self.ad_account.get_campaigns(fields=[
                Campaign.Field.id,
                Campaign.Field.name,
                Campaign.Field.status,
                Campaign.Field.objective,
                Campaign.Field.created_time,
                Campaign.Field.updated_time
            ])

            campaign_list = []
            for campaign in campaigns:
                campaign_list.append({
                    'id': campaign.get('id'),
                    'name': campaign.get('name'),
                    'status': campaign.get('status'),
                    'objective': campaign.get('objective'),
                    'created_time': campaign.get('created_time'),
                })

            return {
                'success': True,
                'campaigns': campaign_list,
                'total': len(campaign_list)
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_insights(self, date_from=None, date_to=None, level='campaign'):
        """
        Obtém insights/métricas das campanhas

        Args:
            date_from (str): Data inicial no formato 'YYYY-MM-DD'
            date_to (str): Data final no formato 'YYYY-MM-DD'
            level (str): Nível dos dados ('account', 'campaign', 'adset', 'ad')

        Returns:
            dict: Dados de performance
        """
        # Definir período padrão (últimos 30 dias)
        if not date_from:
            date_from = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not date_to:
            date_to = datetime.now().strftime('%Y-%m-%d')

        params = {
            'time_range': {
                'since': date_from,
                'until': date_to
            },
            'level': level,
            'breakdowns': ['impression_device'],
            'time_increment': 1,  # Dados diários
        }

        # Campos (métricas) que queremos
        fields = [
            AdsInsights.Field.campaign_id,
            AdsInsights.Field.campaign_name,
            AdsInsights.Field.date_start,
            AdsInsights.Field.date_stop,
            AdsInsights.Field.impressions,
            AdsInsights.Field.clicks,
            AdsInsights.Field.spend,
            AdsInsights.Field.reach,
            AdsInsights.Field.frequency,
            AdsInsights.Field.cpc,
            AdsInsights.Field.cpm,
            AdsInsights.Field.cpp,
            AdsInsights.Field.ctr,
            AdsInsights.Field.actions,  # Conversões
            AdsInsights.Field.action_values,
            AdsInsights.Field.cost_per_action_type,
        ]

        try:
            insights = self.ad_account.get_insights(
                fields=fields,
                params=params
            )

            results = []

            for insight in insights:
                # Processar ações (conversões, leads, etc)
                actions = insight.get('actions', [])
                conversions = 0
                leads = 0

                for action in actions:
                    action_type = action.get('action_type', '')
                    value = int(action.get('value', 0))

                    if 'lead' in action_type.lower():
                        leads += value
                    elif 'conversion' in action_type.lower() or 'purchase' in action_type.lower():
                        conversions += value

                # Dados estruturados
                data = {
                    'date': insight.get('date_start'),
                    'campaign_id': insight.get('campaign_id'),
                    'campaign_name': insight.get('campaign_name'),
                    'impressions': int(insight.get('impressions', 0)),
                    'clicks': int(insight.get('clicks', 0)),
                    'spend': float(insight.get('spend', 0)),
                    'reach': int(insight.get('reach', 0)),
                    'frequency': float(insight.get('frequency', 0)),
                    'cpc': float(insight.get('cpc', 0)),
                    'cpm': float(insight.get('cpm', 0)),
                    'ctr': float(insight.get('ctr', 0)),
                    'conversions': conversions,
                    'leads': leads,
                    'platform': 'Meta Ads'
                }

                # Calcular CPL (custo por lead)
                if leads > 0:
                    data['cpl'] = round(data['spend'] / leads, 2)
                else:
                    data['cpl'] = 0

                # Calcular taxa de conversão
                if data['clicks'] > 0:
                    data['conversion_rate'] = round((conversions / data['clicks']) * 100, 2)
                else:
                    data['conversion_rate'] = 0

                results.append(data)

            print(f"✅ {len(results)} registros coletados de {date_from} a {date_to}")

            return {
                'success': True,
                'data': results,
                'total_records': len(results),
                'date_range': {'from': date_from, 'to': date_to}
            }

        except Exception as e:
            print(f"❌ Erro ao coletar insights: {e}")
            return {
                'success': False,
                'error': str(e)
            }

    def get_daily_summary(self, date_from=None, date_to=None):
        """
        Obtém resumo diário agregado de todas as campanhas

        Returns:
            dict: Resumo com totais por dia
        """
        insights_result = self.get_insights(date_from, date_to, level='account')

        if not insights_result['success']:
            return insights_result

        # Agrupar por data
        daily_data = {}

        for record in insights_result['data']:
            date = record['date']

            if date not in daily_data:
                daily_data[date] = {
                    'date': date,
                    'impressions': 0,
                    'clicks': 0,
                    'spend': 0,
                    'reach': 0,
                    'conversions': 0,
                    'leads': 0,
                    'platform': 'Meta Ads'
                }

            daily_data[date]['impressions'] += record['impressions']
            daily_data[date]['clicks'] += record['clicks']
            daily_data[date]['spend'] += record['spend']
            daily_data[date]['reach'] += record['reach']
            daily_data[date]['conversions'] += record['conversions']
            daily_data[date]['leads'] += record['leads']

        # Calcular métricas derivadas
        for date, data in daily_data.items():
            if data['clicks'] > 0:
                data['cpc'] = round(data['spend'] / data['clicks'], 2)
                data['conversion_rate'] = round((data['conversions'] / data['clicks']) * 100, 2)
            else:
                data['cpc'] = 0
                data['conversion_rate'] = 0

            if data['impressions'] > 0:
                data['ctr'] = round((data['clicks'] / data['impressions']) * 100, 2)
                data['cpm'] = round((data['spend'] / data['impressions']) * 1000, 2)
            else:
                data['ctr'] = 0
                data['cpm'] = 0

            if data['leads'] > 0:
                data['cpl'] = round(data['spend'] / data['leads'], 2)
            else:
                data['cpl'] = 0

        return {
            'success': True,
            'data': list(daily_data.values()),
            'total_days': len(daily_data)
        }

    def _log_error(self, error_data):
        """Registra erro no log"""
        log_file = LOGS_DIR / f"meta_ads_errors_{datetime.now().strftime('%Y-%m')}.log"

        error_data['timestamp'] = datetime.now().isoformat()

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(error_data, ensure_ascii=False) + '\n')


def main():
    """Teste do cliente Meta Ads"""
    print("📘 Testando Cliente Meta Ads\n")

    try:
        client = MetaAdsClient()

        # Informações da conta
        print("📋 Informações da Conta:")
        account = client.get_account_info()

        if account['success']:
            data = account['data']
            print(f"  ✅ Conectado!")
            print(f"  Nome: {data.get('name', 'N/A')}")
            print(f"  ID: {data.get('account_id', 'N/A')}")
            print(f"  Moeda: {data.get('currency', 'N/A')}")
            print(f"  Status: {data.get('account_status', 'N/A')}")
            if data.get('business_name'):
                print(f"  Empresa: {data.get('business_name')}")
        else:
            print(f"  ❌ Erro: {account['error']}")
            return

        # Listar campanhas
        print("\n📊 Campanhas:")
        campaigns = client.get_campaigns()

        if campaigns['success']:
            print(f"  Total de campanhas: {campaigns['total']}")
            for camp in campaigns['campaigns'][:5]:  # Mostrar primeiras 5
                print(f"  • {camp['name']} ({camp['status']})")
        else:
            print(f"  ❌ Erro: {campaigns['error']}")

        # Coletar insights dos últimos 7 dias
        print("\n📈 Coletando insights dos últimos 7 dias...")
        date_from = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        date_to = datetime.now().strftime('%Y-%m-%d')

        summary = client.get_daily_summary(date_from, date_to)

        if summary['success']:
            print(f"  ✅ {summary['total_days']} dias de dados coletados")

            # Mostrar totais
            total_spend = sum(d['spend'] for d in summary['data'])
            total_impressions = sum(d['impressions'] for d in summary['data'])
            total_clicks = sum(d['clicks'] for d in summary['data'])
            total_leads = sum(d['leads'] for d in summary['data'])

            print(f"\n  📊 Totais do período:")
            print(f"     Gasto: R$ {total_spend:,.2f}")
            print(f"     Impressões: {total_impressions:,}")
            print(f"     Cliques: {total_clicks:,}")
            print(f"     Leads: {total_leads:,}")

            if total_leads > 0:
                avg_cpl = total_spend / total_leads
                print(f"     CPL médio: R$ {avg_cpl:.2f}")

        else:
            print(f"  ❌ Erro: {summary['error']}")

        print("\n✅ Testes concluídos!")

    except ValueError as e:
        print(f"\n❌ Erro de configuração: {e}")
        print("💡 Configure META_ACCESS_TOKEN e META_AD_ACCOUNT_ID no arquivo .env")
    except Exception as e:
        print(f"\n❌ Erro: {e}")


if __name__ == '__main__':
    main()
