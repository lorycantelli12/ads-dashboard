"""
Cliente para integração com Google Sheets
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# Adicionar o diretório raiz ao path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from config.settings import GOOGLE_SHEETS_CONFIG, LOGS_DIR


class GoogleSheetsClient:
    """Cliente para ler e escrever dados no Google Sheets"""

    # Scopes necessários
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    def __init__(self):
        self.spreadsheet_id = GOOGLE_SHEETS_CONFIG['spreadsheet_id']
        self.config_tab = GOOGLE_SHEETS_CONFIG['config_tab']
        self.data_tab = GOOGLE_SHEETS_CONFIG['data_tab']
        self.credentials_file = GOOGLE_SHEETS_CONFIG['credentials_file']

        if not self.spreadsheet_id:
            raise ValueError("GOOGLE_SHEETS_SPREADSHEET_ID não configurado")

        if not self.credentials_file:
            raise ValueError("GOOGLE_SHEETS_CREDENTIALS_FILE não configurado")

        self.client = None
        self.spreadsheet = None
        self._authenticate()

    def _authenticate(self):
        """Autentica com Google Sheets usando service account"""
        try:
            credentials = Credentials.from_service_account_file(
                self.credentials_file,
                scopes=self.SCOPES
            )

            self.client = gspread.authorize(credentials)
            self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)

            print(f"✅ Conectado ao Google Sheets: {self.spreadsheet.title}")

        except FileNotFoundError:
            raise FileNotFoundError(
                f"Arquivo de credenciais não encontrado: {self.credentials_file}\n"
                "Baixe o JSON de credenciais do Google Cloud Console"
            )
        except Exception as e:
            raise Exception(f"Erro ao autenticar com Google Sheets: {e}")

    def read_config(self):
        """
        Lê configurações da aba de Config

        Returns:
            list: Lista de dicionários com configurações por plataforma
        """
        try:
            worksheet = self.spreadsheet.worksheet(self.config_tab)
            records = worksheet.get_all_records()

            print(f"📖 {len(records)} configurações lidas da aba '{self.config_tab}'")
            return records

        except gspread.exceptions.WorksheetNotFound:
            print(f"⚠️  Aba '{self.config_tab}' não encontrada. Criando...")
            return self._create_config_tab()
        except Exception as e:
            print(f"❌ Erro ao ler configurações: {e}")
            return []

    def _create_config_tab(self):
        """Cria aba de configuração se não existir"""
        try:
            worksheet = self.spreadsheet.add_worksheet(
                title=self.config_tab,
                rows=100,
                cols=10
            )

            # Cabeçalhos
            headers = [
                'Plataforma',
                'Account ID',
                'Campaign IDs',
                'Status',
                'Notas'
            ]

            # Dados de exemplo
            example_data = [
                ['Meta', 'act_123456789', '', 'Ativo', 'Facebook/Instagram Ads'],
                ['LinkedIn', '123456789', '', 'Ativo', 'LinkedIn Ads'],
                ['Google', '1234567890', '', 'Ativo', 'Google Ads'],
            ]

            # Escrever cabeçalhos e dados
            worksheet.update('A1:E1', [headers])
            worksheet.update('A2:E4', example_data)

            # Formatar cabeçalho
            worksheet.format('A1:E1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 0.9}
            })

            print(f"✅ Aba '{self.config_tab}' criada com dados de exemplo")
            return []

        except Exception as e:
            print(f"❌ Erro ao criar aba de config: {e}")
            return []

    def write_metrics(self, data):
        """
        Escreve métricas na aba de Dados

        Args:
            data (list): Lista de dicionários com métricas
                Exemplo: [
                    {
                        'data': '2024-01-01',
                        'plataforma': 'Meta',
                        'campanha': 'Campanha 1',
                        'impressoes': 1000,
                        'cliques': 50,
                        'gasto': 100.00,
                        ...
                    }
                ]

        Returns:
            bool: True se sucesso, False caso contrário
        """
        if not data:
            print("⚠️  Nenhum dado para escrever")
            return False

        try:
            worksheet = self._get_or_create_data_tab()

            # Obter cabeçalhos existentes ou criar novos
            existing_headers = worksheet.row_values(1)

            if not existing_headers:
                # Primeira vez - criar cabeçalhos baseado nos dados
                headers = list(data[0].keys())
                worksheet.update('A1', [headers])
                worksheet.format('A1:Z1', {
                    'textFormat': {'bold': True},
                    'backgroundColor': {'red': 0.9, 'green': 0.6, 'blue': 0.2}
                })
                existing_headers = headers

            # Preparar linhas para inserir
            rows_to_insert = []
            for item in data:
                row = [item.get(header, '') for header in existing_headers]
                rows_to_insert.append(row)

            # Adicionar no final da planilha
            worksheet.append_rows(rows_to_insert)

            print(f"✅ {len(rows_to_insert)} linhas adicionadas à aba '{self.data_tab}'")
            return True

        except Exception as e:
            print(f"❌ Erro ao escrever métricas: {e}")
            self._log_error({'error': str(e), 'data_count': len(data)})
            return False

    def _get_or_create_data_tab(self):
        """Obtém ou cria a aba de dados"""
        try:
            return self.spreadsheet.worksheet(self.data_tab)
        except gspread.exceptions.WorksheetNotFound:
            print(f"📝 Criando aba '{self.data_tab}'...")
            return self.spreadsheet.add_worksheet(
                title=self.data_tab,
                rows=1000,
                cols=20
            )

    def read_all_data(self):
        """
        Lê todos os dados da aba de Dados

        Returns:
            list: Lista de dicionários com todos os dados
        """
        try:
            worksheet = self.spreadsheet.worksheet(self.data_tab)
            records = worksheet.get_all_records()

            print(f"📖 {len(records)} registros lidos da aba '{self.data_tab}'")
            return records

        except gspread.exceptions.WorksheetNotFound:
            print(f"⚠️  Aba '{self.data_tab}' não encontrada")
            return []
        except Exception as e:
            print(f"❌ Erro ao ler dados: {e}")
            return []

    def clear_data_tab(self):
        """Limpa todos os dados da aba (mantém cabeçalhos)"""
        try:
            worksheet = self.spreadsheet.worksheet(self.data_tab)
            worksheet.clear()
            print(f"🗑️  Aba '{self.data_tab}' limpa")
            return True
        except Exception as e:
            print(f"❌ Erro ao limpar aba: {e}")
            return False

    def get_sheet_info(self):
        """Retorna informações sobre a planilha"""
        try:
            return {
                'success': True,
                'title': self.spreadsheet.title,
                'url': self.spreadsheet.url,
                'worksheets': [ws.title for ws in self.spreadsheet.worksheets()],
                'sheet_id': self.spreadsheet.id
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _log_error(self, error_data):
        """Registra erro no log"""
        log_file = LOGS_DIR / f"google_sheets_errors_{datetime.now().strftime('%Y-%m')}.log"

        error_data['timestamp'] = datetime.now().isoformat()

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(error_data, ensure_ascii=False) + '\n')


def main():
    """Teste do cliente Google Sheets"""
    print("📊 Testando Cliente Google Sheets\n")

    try:
        client = GoogleSheetsClient()

        # Informações da planilha
        print("\n📋 Informações da Planilha:")
        info = client.get_sheet_info()

        if info['success']:
            print(f"  Título: {info['title']}")
            print(f"  URL: {info['url']}")
            print(f"  Abas: {', '.join(info['worksheets'])}")
        else:
            print(f"  Erro: {info['error']}")
            return

        # Ler configurações
        print("\n⚙️  Lendo Configurações:")
        config = client.read_config()
        for item in config:
            print(f"  • {item.get('Plataforma')}: {item.get('Status')}")

        # Teste de escrita (descomente para testar)
        # print("\n💾 Testando escrita de dados...")
        # test_data = [
        #     {
        #         'data': datetime.now().strftime('%Y-%m-%d'),
        #         'plataforma': 'Teste',
        #         'campanha': 'Campanha Teste',
        #         'impressoes': 1000,
        #         'cliques': 50,
        #         'gasto': 100.00
        #     }
        # ]
        # client.write_metrics(test_data)

        print("\n✅ Testes concluídos!")

    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        print("\n💡 Passos para resolver:")
        print("  1. Acesse https://console.cloud.google.com/")
        print("  2. Crie um projeto")
        print("  3. Ative a API do Google Sheets")
        print("  4. Crie uma Service Account")
        print("  5. Baixe o JSON de credenciais")
        print("  6. Configure o caminho no .env")
    except ValueError as e:
        print(f"\n❌ {e}")
        print("💡 Configure o .env com GOOGLE_SHEETS_SPREADSHEET_ID")
    except Exception as e:
        print(f"\n❌ Erro: {e}")


if __name__ == '__main__':
    main()
