# 📝 Como Atualizar o .env.local

## ✅ Arquivo Completo Criado

Criei o arquivo **`.env.local.completo`** com TODAS as variáveis necessárias.

## 🔄 Como Atualizar

### Opção 1: Copiar o arquivo completo

```bash
# No terminal, na raiz do projeto:
cp .env.local.completo .env.local
```

### Opção 2: Manualmente

1. Abra `.env.local.completo`
2. Copie TODO o conteúdo
3. Cole no seu `.env.local` atual (substituindo tudo)

## 📋 O que está no arquivo completo

### ✅ Já preenchido (suas credenciais):
- ✅ DATABASE_URL (Supabase)
- ✅ DB_HOST, DB_USER, DB_PASSWORD
- ✅ SUPABASE_URL, SUPABASE_KEY, SUPABASE_SERVICE_KEY
- ✅ SECRET_KEY, JWT_SECRET_KEY
- ✅ Configurações de WhatsApp
- ✅ GITHUB_TOKEN
- ✅ Configurações básicas da aplicação

### ⬅️ Para preencher depois:
- ⬅️ **AI_API_KEY** - Cole sua chave da OpenAI aqui
- ⬅️ **STRIPE_SECRET_KEY** - Quando configurar pagamento
- ⬅️ **STRIPE_PUBLIC_KEY** - Quando configurar pagamento
- ⬅️ **NOTIFICATION_WHATSAPP_NUMBER** - Quando configurar notificações
- ⬅️ **SMTP_*** - Se quiser enviar emails

## 🎯 Variáveis Importantes Agora

### 1. IA (Para funcionar respostas automáticas):
```env
AI_API_KEY=sk-sua-chave-aqui
```

### 2. Notificações (Opcional):
```env
NOTIFICATION_WHATSAPP_NUMBER=5511999999999
```

### 3. Pagamento (Quando implementar):
```env
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLIC_KEY=pk_live_...
```

## ✅ Após Atualizar

1. **Salve o arquivo** `.env.local`
2. **Reinicie o servidor** se estiver rodando
3. **Teste**: `python3 scripts/init_db.py` (deve conectar no Supabase)

---

**O arquivo `.env.local.completo` tem TODAS as variáveis necessárias para o sistema funcionar completamente!**
