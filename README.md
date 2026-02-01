# 📊 Dashboard Meta Ads - Fabrício

Dashboard de análise de campanhas do Meta Ads (Facebook/Instagram) com dados em tempo real.

## 🎯 Funcionalidades

- ✅ **Dashboard Web Interativo** (Streamlit)
  - Visão consolidada de todas as plataformas
  - Gráficos de performance em tempo real
  - Comparação entre plataformas
  - Filtros por período, campanha e métricas

- ✅ **Integração Google Sheets**
  - Leitura de configurações da planilha
  - Salvamento automático de métricas
  - Atualização periódica

- ✅ **Coleta Automática de Dados**
  - Agendamento de coleta periódica
  - Logs detalhados
  - Tratamento de erros

- ✅ **Métricas Principais**
  - Impressões e alcance
  - Cliques e CTR (taxa de cliques)
  - Conversões e taxa de conversão
  - CPC (custo por clique)
  - CPM (custo por mil impressões)
  - ROAS (retorno sobre gasto em anúncios)
  - Gasto total

## 🚀 Deploy no Streamlit Cloud (RECOMENDADO)

### Passo 1: Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. Nome do repositório: `ads-dashboard`
3. Deixe como **Público** (necessário para Streamlit Cloud gratuito)
4. **NÃO** marque "Add README" (já temos um)
5. Clique em **"Create repository"**

### Passo 2: Subir o Código

Execute no terminal:

```bash
cd ~/ads-dashboard
git add .
git commit -m "Initial commit - Meta Ads Dashboard"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/ads-dashboard.git
git push -u origin main
```

(Substitua `SEU_USUARIO` pelo seu username do GitHub)

### Passo 3: Deploy no Streamlit Cloud

1. Acesse: **https://share.streamlit.io/**
2. Faça login com sua conta GitHub
3. Clique em **"New app"**
4. Selecione:
   - **Repository**: `SEU_USUARIO/ads-dashboard`
   - **Branch**: `main`
   - **Main file path**: `dashboard_meta_real.py`
5. Clique em **"Advanced settings"**
6. Em **"Secrets"**, cole:

```toml
META_ACCESS_TOKEN = "EAANNVTMzRiUBQm56PXOwEZAJfNxR6MAGFOY6KhEvAMzPzbEpIe4jfqz6XaXEQIW2rr0wuqL45pZCAj1SGSzGlDQ9oZADBsXZBbff69OY92W5BztEZAGTnJ5mQf6Dn8yGXVRvOABrIAz7YDfyV9wzVovAAn4SI9mRgJe5IX1DjdY2SlIs9ixRZBfmbQ2bd6oUel"
META_AD_ACCOUNT_ID = "act_188938172932947"
```

7. Clique em **"Deploy!"**
8. Aguarde 2-3 minutos... 🚀
9. Seu dashboard estará no ar! 🎉

## 🖥️ Instalação Local (Opcional)

### 1. Instalar Dependências

```bash
cd ~/ads-dashboard
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar .env

```bash
cp .env.example .env
```

Edite o `.env` com suas credenciais.

### 3. Executar Dashboard

```bash
streamlit run dashboard_meta_real.py
```

Acesse: `http://localhost:8501`

## 📋 Configuração de APIs

Cada plataforma requer configuração específica:

1. **Google Sheets**: [docs/GOOGLE_SHEETS_SETUP.md](docs/GOOGLE_SHEETS_SETUP.md)
2. **Meta Ads**: [docs/META_ADS_SETUP.md](docs/META_ADS_SETUP.md)
3. **LinkedIn Ads**: [docs/LINKEDIN_ADS_SETUP.md](docs/LINKEDIN_ADS_SETUP.md)
4. **Google Ads**: [docs/GOOGLE_ADS_SETUP.md](docs/GOOGLE_ADS_SETUP.md)

## 📂 Estrutura do Projeto

```
ads-dashboard/
├── dashboard.py              # Dashboard principal (Streamlit)
├── collector.py              # Script de coleta automática
├── requirements.txt          # Dependências
├── .env.example             # Template de configuração
│
├── config/
│   └── settings.py          # Configurações centralizadas
│
├── src/
│   ├── google_sheets/       # Integração Google Sheets
│   ├── meta_ads/            # Integração Meta Ads
│   ├── linkedin_ads/        # Integração LinkedIn Ads
│   ├── google_ads/          # Integração Google Ads
│   └── collector/           # Sistema de coleta
│
├── credentials/             # Credenciais das APIs (não commitar!)
├── data/                    # Dados coletados (CSV/cache)
├── logs/                    # Logs do sistema
└── docs/                    # Documentação
```

## 🎨 Dashboard

### Visão Geral

O dashboard mostra:

- **KPIs principais**: Cards com métricas resumidas
- **Gráficos temporais**: Evolução de métricas ao longo do tempo
- **Comparação de plataformas**: Performance lado a lado
- **Tabela detalhada**: Dados completos de cada campanha
- **Exportação**: Download de relatórios em CSV/Excel

### Filtros Disponíveis

- Período (últimos 7, 30, 90 dias ou customizado)
- Plataforma (Meta, LinkedIn, Google ou todas)
- Campanha específica
- Métricas a visualizar

## 🔄 Coleta Automática

Configure coleta periódica de dados:

```bash
# Executar coleta única
python collector.py --once

# Executar coleta agendada
python collector.py --schedule
```

Configure a frequência no `.env`:

```env
COLLECTION_FREQUENCY_HOURS=24
COLLECTION_TIME=08:00
```

## 📊 Google Sheets

### Estrutura da Planilha

O sistema espera duas abas:

**1. Aba "Config"** (Configurações)
| Plataforma | Account ID | Campaign IDs | Status |
|------------|------------|--------------|--------|
| Meta | act_123... | | Ativo |
| LinkedIn | 456... | | Ativo |
| Google | 789... | | Ativo |

**2. Aba "Dados"** (Métricas coletadas)
| Data | Plataforma | Campanha | Impressões | Cliques | Gasto | ... |
|------|------------|----------|------------|---------|-------|-----|
| ... | ... | ... | ... | ... | ... | ... |

## 💰 Custos das APIs

- **Meta Ads API**: Gratuita (limite: 200 chamadas/hora)
- **LinkedIn Ads API**: Gratuita (limite: 100 chamadas/dia)
- **Google Ads API**: Gratuita (limite: 15.000 operações/dia)
- **Google Sheets API**: Gratuita (limite: 300 requisições/minuto)

## 🔒 Segurança

- ⚠️ Nunca commite o arquivo `.env`
- ⚠️ Nunca commite arquivos de credenciais (`.json`)
- ✅ Use `.gitignore` (já configurado)
- ✅ Rotacione tokens periodicamente

## 🐛 Troubleshooting

### "Erro ao conectar com Google Sheets"
- Verifique se o arquivo de credenciais está no local correto
- Certifique-se de que compartilhou a planilha com o service account

### "Invalid access token - Meta"
- Tokens do Meta expiram em 60 dias
- Renove o token seguindo o guia

### "Rate limit exceeded"
- Reduza a frequência de coleta
- Aguarde o reset do limite (geralmente 1 hora)

## 📚 Documentação Completa

- [Guia de Início Rápido](docs/QUICKSTART.md)
- [Configuração Google Sheets](docs/GOOGLE_SHEETS_SETUP.md)
- [Configuração Meta Ads](docs/META_ADS_SETUP.md)
- [Configuração LinkedIn Ads](docs/LINKEDIN_ADS_SETUP.md)
- [Configuração Google Ads](docs/GOOGLE_ADS_SETUP.md)

## 🆘 Suporte

Para dúvidas e problemas:
1. Verifique os logs em `logs/`
2. Consulte a documentação em `docs/`
3. Valide configurações: `python config/settings.py`

---

Desenvolvido para centralizar e simplificar a análise de campanhas de ads 🚀
