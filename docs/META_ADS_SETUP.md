# Guia Completo - Meta Ads API (Facebook/Instagram)

Passo a passo para configurar a API do Meta Ads e coletar dados de campanhas.

## 📋 Pré-requisitos

✅ Conta no **Facebook Business Manager** (Meta Business Suite)
✅ Conta de anúncios ativa (Facebook Ads Manager)
✅ Campanhas rodando ou já executadas
✅ Permissão de **Administrador** na conta de anúncios

---

## Passo 1: Acessar Meta for Developers

1. Acesse: **https://developers.facebook.com/**
2. Faça login com sua conta Facebook (de preferência a mesma do Business Manager)
3. No canto superior direito, clique em **"Meus Aplicativos"**

---

## Passo 2: Criar um Aplicativo

1. Clique em **"Criar Aplicativo"**

2. Escolha o tipo: **"Empresa"** (Business)

3. Preencha os dados:
   - **Nome do aplicativo**: `Ads Dashboard Analytics`
   - **Email de contato**: seu email
   - **Conta comercial do aplicativo**: Selecione sua conta Business (ou crie uma)

4. Clique em **"Criar aplicativo"**

5. Você pode precisar fazer verificação de segurança (CAPTCHA ou código SMS)

---

## Passo 3: Adicionar o Produto "Marketing API"

1. No dashboard do seu app, procure **"Adicionar produtos"**

2. Encontre **"Marketing API"** e clique em **"Configurar"**

3. A API será adicionada ao seu aplicativo

---

## Passo 4: Obter Access Token

### Opção A: Usando Graph API Explorer (Mais Rápido)

1. Acesse: **https://developers.facebook.com/tools/explorer/**

2. No topo da página:
   - Em **"Meta App"**: Selecione o app que você criou (`Ads Dashboard Analytics`)
   - Clique em **"Generate Access Token"** (Gerar Token de Acesso)

3. Uma janela vai abrir pedindo permissões. Marque:
   - ✅ `ads_read` - Ler dados de anúncios
   - ✅ `ads_management` - Gerenciar anúncios
   - ✅ `business_management` - Gerenciar negócios

4. Clique em **"Gerar Token"** ou **"Generate Token"**

5. **COPIE O TOKEN** que aparece (começa com `EAA...`)
   - ⚠️ **IMPORTANTE**: Este token expira em **1 hora**
   - Vamos converter para token de longa duração no Passo 6

### Opção B: No App Dashboard

1. No dashboard do app, vá em **"Ferramentas"** → **"Graph API Explorer"**
2. Siga os mesmos passos da Opção A

---

## Passo 5: Obter o Ad Account ID

1. Acesse: **https://business.facebook.com/settings/ad-accounts**

2. Você verá uma lista das suas contas de anúncios

3. Clique na conta que você quer usar

4. Na URL ou nas informações da conta, copie o **ID da conta de anúncios**
   - Formato: `act_1234567890123456` ou apenas `1234567890123456`
   - Se não tiver o prefixo `act_`, adicione: `act_1234567890123456`

5. Guarde esse ID!

---

## Passo 6: Converter para Token de Longa Duração

O token que você gerou expira em 1 hora. Vamos converter para **60 dias**:

### Pegar App ID e App Secret:

1. No dashboard do app, vá em **"Configurações"** → **"Básico"**

2. Copie:
   - **ID do Aplicativo** (App ID): Ex: `123456789012345`
   - **Chave Secreta do Aplicativo** (App Secret): Clique em "Mostrar" e copie

### Converter o Token:

Execute este comando no **terminal** (ou use um navegador):

```bash
curl -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=SEU_APP_ID&client_secret=SEU_APP_SECRET&fb_exchange_token=SEU_TOKEN_CURTO"
```

**Substitua:**
- `SEU_APP_ID` → ID do aplicativo
- `SEU_APP_SECRET` → Secret do aplicativo
- `SEU_TOKEN_CURTO` → Token de 1 hora que você gerou

**Exemplo:**
```bash
curl -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=123456789012345&client_secret=abc123def456&fb_exchange_token=EAAabc123..."
```

**Resposta:**
```json
{
  "access_token": "EAAxyz789...",
  "token_type": "bearer",
  "expires_in": 5183944
}
```

O novo `access_token` dura **60 dias**! 🎉

---

## Passo 7: Configurar no .env

Edite o arquivo `.env` do projeto:

```env
# META ADS
META_ACCESS_TOKEN=EAAxyz789...
META_AD_ACCOUNT_ID=act_1234567890123456
META_CAMPAIGN_IDS=
```

---

## Passo 8: Testar a Conexão

Execute no terminal:

```bash
cd ~/ads-dashboard
source venv/bin/activate
python src/meta_ads/client.py
```

Se tudo estiver correto, você verá:
```
✅ Conectado ao Meta Ads!
Conta: Nome da Conta
ID: act_1234567890123456
```

---

## 📊 Permissões Necessárias

Para o dashboard funcionar, o token precisa ter estas permissões:

| Permissão | Descrição |
|-----------|-----------|
| `ads_read` | Ler insights de campanhas |
| `ads_management` | Gerenciar anúncios |
| `business_management` | Acessar Business Manager |

---

## 🔄 Renovar Token (A cada 60 dias)

O token expira em 60 dias. Para renovar:

1. Repita o **Passo 4** para gerar um novo token curto
2. Repita o **Passo 6** para converter para longa duração
3. Atualize o `.env` com o novo token

---

## 🔒 Segurança

**NUNCA compartilhe:**
- ❌ Access Token
- ❌ App Secret
- ❌ Arquivo `.env`

**Sempre:**
- ✅ Use `.gitignore` (já configurado)
- ✅ Rotacione tokens periodicamente
- ✅ Use contas de serviço em produção

---

## ❓ Troubleshooting

### Erro: "Invalid OAuth access token"
- Token expirou → Gere um novo
- Token sem permissões → Regere com permissões corretas

### Erro: "Unsupported get request"
- Account ID está errado → Verifique o formato `act_123...`
- Token não tem acesso à conta → Verifique permissões no Business Manager

### Erro: "Rate limit exceeded"
- Muitas requisições → Aguarde 1 hora ou reduza frequência de coleta

### Erro: "Permission denied"
- Sua conta não tem acesso a essa conta de anúncios
- Peça ao administrador para adicionar seu usuário

---

## 📚 Recursos Adicionais

- Meta for Developers: https://developers.facebook.com/
- Marketing API Docs: https://developers.facebook.com/docs/marketing-apis
- Graph API Explorer: https://developers.facebook.com/tools/explorer/
- Business Manager: https://business.facebook.com/

---

## 🎯 Próximos Passos

Depois de configurar:
1. ✅ Teste a conexão
2. ✅ Execute a coleta de dados
3. ✅ Visualize no dashboard
4. ✅ Configure coleta automática

---

Pronto para coletar dados! 🚀
