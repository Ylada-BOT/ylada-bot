# 🚀 Passo a Passo Completo: Railway + Deploy

## 🎯 Objetivo

Configurar seu bot no Railway, fazer deploy e obter todas as chaves/configurações necessárias.

---

## 📋 PRÉ-REQUISITOS

Antes de começar, você precisa ter:

- ✅ Conta no GitHub (seu código já está lá)
- ✅ Conta no Supabase (banco de dados)
- ✅ Conta na OpenAI (para IA - opcional por enquanto)
- ✅ Email para criar conta no Railway

---

## 🚂 PASSO 1: Criar Conta no Railway

### **1.1 Acessar Railway**

1. Acesse: **https://railway.app**
2. Clique em **"Start a New Project"** ou **"Login"**
3. Escolha **"Login with GitHub"**
4. Autorize o Railway a acessar seu GitHub

### **1.2 Verificar Conta**

- ✅ Você será redirecionado para o dashboard do Railway
- ✅ Sua conta está criada!

**Custo:** R$ 0 (plano grátis com $5 créditos/mês)

---

## 📦 PASSO 2: Criar Projeto no Railway

### **2.1 Criar Novo Projeto**

1. No dashboard, clique em **"New Project"**
2. Escolha **"Deploy from GitHub repo"**
3. Selecione seu repositório: `ylada-bot` (ou o nome do seu repo)
4. Clique em **"Deploy Now"**

### **2.2 Railway Detecta Automaticamente**

O Railway vai:
- ✅ Detectar que é um projeto Python
- ✅ Tentar fazer deploy automaticamente
- ⚠️ Pode dar erro inicial (normal, vamos configurar)

---

## ⚙️ PASSO 3: Configurar Serviço Python (Flask)

### **3.1 Ajustar Configurações do Serviço**

1. No projeto criado, você verá um serviço
2. Clique no serviço para abrir configurações
3. Vá em **"Settings"** → **"Deploy"**

### **3.2 Configurar Build e Start**

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
python3 web/app.py
```

**Root Directory:**
```
/
```

### **3.3 Configurar Porta**

1. Vá em **"Settings"** → **"Networking"**
2. Adicione variável de ambiente:
   - **Nome:** `PORT`
   - **Valor:** `5002`

---

## 🔑 PASSO 4: Configurar Variáveis de Ambiente

### **4.1 Acessar Variáveis de Ambiente**

1. No serviço, clique em **"Variables"**
2. Clique em **"New Variable"**

### **4.2 Adicionar Variáveis Essenciais**

Adicione uma por uma:

#### **A) Configuração Básica**

```bash
# Porta do Flask
PORT=5002

# Ambiente
NODE_ENV=production
PYTHON_ENV=production

# Secret Key (GERE UMA NOVA!)
SECRET_KEY=seu-secret-key-super-seguro-aqui-123456789
```

**Como gerar SECRET_KEY:**
```bash
# No terminal local, execute:
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```
Copie o resultado e use como `SECRET_KEY`.

#### **B) Banco de Dados (Supabase)**

```bash
# URL do Supabase (você já tem)
DATABASE_URL=postgresql://postgres:[SENHA]@[HOST]:5432/postgres
```

**Como obter DATABASE_URL:**
1. Acesse: https://supabase.com
2. Vá no seu projeto
3. **Settings** → **Database**
4. Role até **"Connection string"**
5. Copie a string (substitua `[YOUR-PASSWORD]` pela senha real)
6. Cole no Railway

#### **C) JWT (Autenticação)**

```bash
# JWT Secret (GERE UMA NOVA!)
JWT_SECRET_KEY=jwt-secret-key-super-seguro-aqui-123456789
```

**Como gerar JWT_SECRET_KEY:**
```bash
# No terminal local, execute:
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### **D) WhatsApp (Configuração)**

```bash
# URL do servidor WhatsApp (vamos configurar depois)
WHATSAPP_SERVER_URL=http://localhost:5001
WHATSAPP_SERVER_PORT=5001
```

#### **E) IA (OpenAI - Opcional por enquanto)**

```bash
# OpenAI (opcional - configure depois se quiser)
AI_PROVIDER=openai
AI_API_KEY=sk-... (seu token da OpenAI)
AI_MODEL=gpt-4o-mini
```

**Como obter AI_API_KEY:**
1. Acesse: https://platform.openai.com/api-keys
2. Crie uma nova chave
3. Copie e cole no Railway

#### **F) URL da Aplicação**

```bash
# URL do seu app no Railway (vamos obter depois)
APP_URL=https://seu-projeto.up.railway.app
```

**⚠️ IMPORTANTE:** Deixe `APP_URL` vazio por enquanto. Vamos obter depois do deploy.

---

## 🚀 PASSO 5: Fazer Deploy

### **5.1 Trigger Deploy**

1. Após adicionar todas as variáveis
2. Vá em **"Deployments"**
3. Clique em **"Redeploy"** ou aguarde deploy automático

### **5.2 Verificar Logs**

1. Clique em **"Deployments"** → Último deploy
2. Veja os logs em tempo real
3. Aguarde até ver: `Running on http://0.0.0.0:5002`

### **5.3 Obter URL do App**

1. Vá em **"Settings"** → **"Networking"**
2. Clique em **"Generate Domain"**
3. Copie a URL gerada (ex: `seu-projeto.up.railway.app`)
4. Volte em **"Variables"** e atualize:
   ```bash
   APP_URL=https://seu-projeto.up.railway.app
   ```

---

## 📱 PASSO 6: Configurar Serviço Node.js (WhatsApp)

### **6.1 Criar Novo Serviço**

1. No mesmo projeto Railway
2. Clique em **"New"** → **"Empty Service"**
3. Nome: `whatsapp-server`

### **6.2 Configurar Serviço Node.js**

1. Clique no serviço `whatsapp-server`
2. Vá em **"Settings"** → **"Deploy"**

**Build Command:**
```bash
npm install
```

**Start Command:**
```bash
node whatsapp_server.js
```

**Root Directory:**
```
/
```

### **6.3 Configurar Variáveis do Node.js**

1. No serviço `whatsapp-server`, vá em **"Variables"**
2. Adicione:

```bash
# Porta do servidor WhatsApp
PORT=5001

# Ambiente
NODE_ENV=production
```

### **6.4 Configurar Networking**

1. Vá em **"Settings"** → **"Networking"**
2. Adicione variável:
   - **Nome:** `PORT`
   - **Valor:** `5001`

### **6.5 Atualizar URL no Serviço Python**

1. Volte no serviço Python (Flask)
2. Vá em **"Variables"**
3. Obtenha a URL do serviço Node.js:
   - No serviço `whatsapp-server`
   - **Settings** → **Networking** → **Generate Domain**
   - Copie a URL (ex: `whatsapp-server.up.railway.app`)
4. Atualize no serviço Python:
   ```bash
   WHATSAPP_SERVER_URL=https://whatsapp-server.up.railway.app
   ```

---

## 🔗 PASSO 7: Conectar Serviços

### **7.1 Verificar Comunicação**

Os dois serviços precisam se comunicar:

**Opção A: Mesmo Projeto (Recomendado)**
- Railway permite comunicação interna
- Use: `http://whatsapp-server:5001` (nome do serviço)

**Opção B: URLs Públicas**
- Use as URLs geradas pelo Railway
- Ex: `https://whatsapp-server.up.railway.app`

### **7.2 Atualizar Variável no Python**

No serviço Python, atualize:

```bash
# Se serviços no mesmo projeto:
WHATSAPP_SERVER_URL=http://whatsapp-server:5001

# OU se usar URLs públicas:
WHATSAPP_SERVER_URL=https://whatsapp-server.up.railway.app
```

---

## ✅ PASSO 8: Verificar se Está Funcionando

### **8.1 Verificar Logs**

1. No serviço Python, veja os logs
2. Deve aparecer: `Running on http://0.0.0.0:5002`
3. Sem erros de conexão

### **8.2 Testar URL**

1. Acesse: `https://seu-projeto.up.railway.app`
2. Deve carregar a página de login
3. Se não carregar, verifique logs

### **8.3 Testar API**

1. Acesse: `https://seu-projeto.up.railway.app/api/health`
2. Deve retornar JSON com status

---

## 📊 PASSO 9: Obter Todas as Chaves/Configurações

### **9.1 Resumo de Todas as URLs e Chaves**

Crie um documento com:

```markdown
# Configurações Railway - YLADA BOT

## URLs
- App Principal: https://seu-projeto.up.railway.app
- WhatsApp Server: https://whatsapp-server.up.railway.app
- (ou interno: http://whatsapp-server:5001)

## Variáveis de Ambiente (já configuradas no Railway)
- PORT=5002
- SECRET_KEY=*** (gerado)
- JWT_SECRET_KEY=*** (gerado)
- DATABASE_URL=*** (Supabase)
- WHATSAPP_SERVER_URL=*** (configurado)
- APP_URL=https://seu-projeto.up.railway.app

## Supabase
- URL: https://seu-projeto.supabase.co
- DATABASE_URL: postgresql://...

## OpenAI (se configurado)
- API Key: sk-*** (já no Railway)
```

---

## 🔧 PASSO 10: Configurações Adicionais (Opcional)

### **10.1 Domínio Customizado (Opcional)**

1. Vá em **"Settings"** → **"Networking"**
2. Clique em **"Custom Domain"**
3. Adicione seu domínio (ex: `yladabot.com`)
4. Configure DNS conforme instruções

### **10.2 Monitoramento (Opcional)**

1. Railway tem logs integrados
2. Veja em **"Deployments"** → **Logs**
3. Pode integrar com serviços externos se quiser

---

## ⚠️ TROUBLESHOOTING

### **Erro: "Module not found"**

**Solução:**
1. Verifique se `requirements.txt` está completo
2. Veja logs do build
3. Adicione dependências faltantes

### **Erro: "Port already in use"**

**Solução:**
1. Verifique variável `PORT` está configurada
2. Railway usa porta automática se não especificar
3. Use variável `PORT` sempre

### **Erro: "Database connection failed"**

**Solução:**
1. Verifique `DATABASE_URL` está correto
2. Verifique se Supabase permite conexões externas
3. Verifique senha está correta

### **Erro: "WhatsApp server not responding"**

**Solução:**
1. Verifique serviço Node.js está rodando
2. Verifique `WHATSAPP_SERVER_URL` está correto
3. Verifique logs do serviço Node.js

---

## 📝 CHECKLIST FINAL

Antes de considerar completo, verifique:

- [ ] Conta Railway criada
- [ ] Projeto criado e conectado ao GitHub
- [ ] Serviço Python (Flask) configurado
- [ ] Serviço Node.js (WhatsApp) configurado
- [ ] Todas as variáveis de ambiente adicionadas
- [ ] Deploy realizado com sucesso
- [ ] URLs obtidas e configuradas
- [ ] App acessível via URL
- [ ] Logs sem erros críticos
- [ ] Banco de dados conectado
- [ ] WhatsApp server acessível

---

## 🎯 PRÓXIMOS PASSOS

Após configurar tudo:

1. **Testar Login/Registro**
   - Acesse: `https://seu-projeto.up.railway.app/register`
   - Crie primeiro usuário
   - Faça login

2. **Conectar WhatsApp**
   - Acesse: `https://seu-projeto.up.railway.app/qr`
   - Escaneie QR Code
   - Verifique conexão

3. **Configurar IA (se quiser)**
   - Adicione `AI_API_KEY` no Railway
   - Teste respostas automáticas

4. **Monitorar Uso**
   - Veja créditos no Railway
   - Monitore custos

---

## 💰 CUSTOS ESPERADOS

**Primeiros dias (Grátis):**
- $5 créditos grátis/mês
- Dura ~4 dias se rodar 24/7

**Depois:**
- Railway: ~R$ 25-50/mês (1-2 serviços)
- Supabase: R$ 0-125/mês (depende do uso)
- OpenAI: R$ 0-200/mês (depende do uso)

**Total estimado:** R$ 25-375/mês

---

## 📞 SUPORTE

Se tiver problemas:

1. **Logs do Railway:** Veja em "Deployments" → "Logs"
2. **Documentação:** https://docs.railway.app
3. **Comunidade:** Discord do Railway

---

**Última atualização:** 27/01/2025


