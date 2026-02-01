# Guia Completo - Google Cloud Console

Passo a passo para configurar Google Sheets API e obter credenciais.

## 📋 O que vamos fazer

1. Criar um projeto no Google Cloud
2. Ativar a API do Google Sheets
3. Criar uma Service Account (conta de serviço)
4. Baixar credenciais JSON
5. Compartilhar planilha com a service account

---

## Passo 1: Acessar Google Cloud Console

1. Acesse: **https://console.cloud.google.com/**
2. Faça login com sua conta Google
3. Aceite os termos de serviço se aparecer

---

## Passo 2: Criar Novo Projeto

1. No topo da página, clique no **seletor de projeto** (ao lado de "Google Cloud")

2. Na janela que abrir, clique em **"NOVO PROJETO"** (canto superior direito)

3. Preencha:
   - **Nome do projeto**: `ads-dashboard` (ou outro nome)
   - **Organização**: Deixe "Sem organização" (padrão)
   - **Local**: Deixe como está

4. Clique em **"CRIAR"**

5. Aguarde alguns segundos. Uma notificação aparecerá quando o projeto for criado

6. **IMPORTANTE**: Clique na notificação ou no seletor de projeto e escolha o projeto que acabou de criar

---

## Passo 3: Ativar Google Sheets API

1. No menu lateral esquerdo (☰), vá em:
   ```
   APIs e serviços > Biblioteca
   ```

2. Na barra de busca, digite: **"Google Sheets API"**

3. Clique no resultado **"Google Sheets API"**

4. Clique no botão azul **"ATIVAR"**

5. Aguarde a ativação (5-10 segundos)

6. Você será redirecionado para a página da API

---

## Passo 4: Ativar Google Drive API (Opcional mas Recomendado)

Repita o processo para a Google Drive API:

1. Volte para **APIs e serviços > Biblioteca**
2. Busque: **"Google Drive API"**
3. Clique e depois em **"ATIVAR"**

---

## Passo 5: Criar Service Account (Conta de Serviço)

1. No menu lateral, vá em:
   ```
   APIs e serviços > Credenciais
   ```

2. No topo, clique em **"+ CRIAR CREDENCIAIS"**

3. Selecione: **"Conta de serviço"**

4. Preencha os dados:
   - **Nome da conta de serviço**: `ads-dashboard-service`
   - **ID da conta de serviço**: (será preenchido automaticamente)
   - **Descrição**: "Service account para dashboard de ads"

5. Clique em **"CRIAR E CONTINUAR"**

6. **Conceder acesso ao projeto** (Etapa 2):
   - Em "Papel", selecione: **"Editor"**
   - (Você pode buscar por "Editor" na caixa de busca)
   - Clique em **"CONTINUAR"**

7. **Conceder acesso aos usuários** (Etapa 3):
   - Deixe em branco
   - Clique em **"CONCLUIR"**

---

## Passo 6: Baixar Credenciais JSON

1. Você verá a lista de Service Accounts criadas

2. Clique no **email da service account** que você acabou de criar
   - Será algo como: `ads-dashboard-service@seu-projeto.iam.gserviceaccount.com`

3. Vá na aba **"CHAVES"** (Keys)

4. Clique em **"ADICIONAR CHAVE"** > **"Criar nova chave"**

5. Escolha o tipo: **JSON**

6. Clique em **"CRIAR"**

7. Um arquivo JSON será baixado automaticamente para seu computador
   - Nome será algo como: `seu-projeto-abc123.json`

8. **IMPORTANTE**: Guarde este arquivo com segurança!

---

## Passo 7: Mover Credenciais para o Projeto

Agora vamos colocar o arquivo JSON no lugar certo:

1. Abra o Finder/Explorer onde o arquivo foi baixado (geralmente pasta Downloads)

2. **Renomeie** o arquivo para algo mais simples:
   ```
   google-service-account.json
   ```

3. Mova o arquivo para a pasta do projeto:
   ```bash
   # No terminal:
   cd ~/ads-dashboard
   mv ~/Downloads/google-service-account.json credentials/
   ```

   Ou arraste manualmente para:
   ```
   ads-dashboard/credentials/google-service-account.json
   ```

---

## Passo 8: Configurar .env

Edite o arquivo `.env` e adicione:

```env
GOOGLE_SHEETS_CREDENTIALS_FILE=credentials/google-service-account.json
```

---

## Passo 9: Criar e Compartilhar Planilha do Google

### Criar a Planilha:

1. Acesse: **https://sheets.google.com/**

2. Clique em **"+ Em branco"** para criar nova planilha

3. Dê um nome à planilha: `Dashboard Ads Analytics`

4. Copie o **ID da planilha** da URL:
   ```
   https://docs.google.com/spreadsheets/d/ESTE_É_O_ID/edit
   ```

5. Cole o ID no `.env`:
   ```env
   GOOGLE_SHEETS_SPREADSHEET_ID=ESTE_É_O_ID
   ```

### Compartilhar com Service Account:

1. Na planilha, clique em **"Compartilhar"** (canto superior direito)

2. **COPIE o email da service account** que você criou:
   - Vá em Google Cloud Console > IAM e administrador > Contas de serviço
   - Copie o email (algo como `ads-dashboard-service@seu-projeto.iam.gserviceaccount.com`)

3. **Cole o email** no campo "Adicionar pessoas e grupos"

4. Defina a permissão como: **"Editor"**

5. **DESMARQUE** a opção "Notificar pessoas"

6. Clique em **"Compartilhar"** ou **"Enviar"**

---

## Passo 10: Testar a Conexão

No terminal, execute:

```bash
cd ~/ads-dashboard
source venv/bin/activate  # Se ainda não ativou
python src/google_sheets/client.py
```

Se tudo estiver correto, você verá:
```
✅ Conectado ao Google Sheets: Dashboard Ads Analytics
```

---

## 🎉 Pronto!

Agora o Google Sheets está configurado e funcionando!

---

## 🔒 Segurança

**NUNCA compartilhe ou commite:**
- ❌ O arquivo JSON de credenciais
- ❌ O email da service account em lugares públicos
- ❌ O ID da planilha (se contiver dados sensíveis)

**O `.gitignore` já está configurado para proteger:**
- ✅ `credentials/*.json`
- ✅ `.env`

---

## ❓ Problemas Comuns

### "Arquivo de credenciais não encontrado"
- Verifique se o arquivo JSON está em `ads-dashboard/credentials/`
- Verifique se o caminho no `.env` está correto

### "Permission denied" ao acessar planilha
- Verifique se compartilhou a planilha com o email da service account
- Verifique se deu permissão de "Editor"

### "API not enabled"
- Volte ao Google Cloud Console
- Certifique-se de que ativou a Google Sheets API
- Aguarde alguns minutos para propagar

### "Invalid credentials"
- Certifique-se de baixar o JSON da service account correta
- Verifique se o arquivo JSON não está corrompido

---

## 📚 Recursos Úteis

- Console Google Cloud: https://console.cloud.google.com/
- Documentação Google Sheets API: https://developers.google.com/sheets/api
- Guia de Service Accounts: https://cloud.google.com/iam/docs/service-accounts

---

## 🆘 Precisa de Ajuda?

Se encontrar algum erro:

1. Verifique os logs em `logs/`
2. Execute: `python config/settings.py` para validar configurações
3. Tente testar: `python src/google_sheets/client.py`
