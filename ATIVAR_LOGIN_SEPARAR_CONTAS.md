# 🔐 Ativar Login e Separar Contas

## ✅ Por que ativar login?

Você está certo! Faz muito sentido ter login para:
- ✅ **Cada conta tem seu próprio System Prompt** (Portal Magra, outras empresas)
- ✅ **Cada conta tem suas próprias configurações** (IA, WhatsApp, etc.)
- ✅ **Cada conta tem seus próprios leads e conversas**
- ✅ **Cada conta tem seus próprios fluxos**
- ✅ **Mais profissional e escalável**

## 🚀 Como Ativar (Simples!)

### Passo 1: Ativar Autenticação

No arquivo `.env`, adicione:

```env
AUTH_REQUIRED=true
```

Ou edite `web/app.py` linha 98:

```python
AUTH_REQUIRED = os.getenv('AUTH_REQUIRED', 'true').lower() == 'true'  # Mude de 'false' para 'true'
```

### Passo 2: Criar Primeira Conta

1. Acesse: `http://localhost:5002/register`
2. Preencha:
   - **Nome:** Seu nome
   - **Email:** seu@email.com
   - **Senha:** sua senha
3. Clique em **"Criar Conta"**

### Passo 3: Fazer Login

1. Acesse: `http://localhost:5002/login`
2. Digite email e senha
3. Clique em **"Entrar"**

### Passo 4: Configurar System Prompt

1. No Dashboard, vá em **"Configurar IA"**
2. Cole o System Prompt da Portal Magra
3. Salve

**Pronto!** Cada conta terá seu próprio System Prompt.

---

## 📋 Como Funciona Agora

### Antes (Sem Login):
- ❌ Todos compartilham o mesmo System Prompt
- ❌ Não dá para ter múltiplas contas
- ❌ Configurações são globais

### Depois (Com Login):
- ✅ Cada usuário tem seu próprio System Prompt
- ✅ Cada usuário tem suas próprias configurações
- ✅ Cada usuário tem seus próprios leads/conversas
- ✅ Cada usuário tem seu próprio WhatsApp (1 por conta)
- ✅ Pode ter múltiplas contas (Portal Magra, outras empresas)

---

## 🎯 Estrutura por Conta

Cada conta terá:
- ✅ **System Prompt próprio** (salvo em `data/ai_config_user_{user_id}.json`)
- ✅ **WhatsApp próprio** (1 instância por usuário)
- ✅ **Leads próprios** (filtrados por `user_id`)
- ✅ **Conversas próprias** (filtradas por `user_id`)
- ✅ **Fluxos próprios** (filtrados por `user_id`)

---

## 🔧 Mudanças Necessárias

Vou fazer as seguintes atualizações:

1. ✅ Ativar autenticação por padrão
2. ✅ Salvar System Prompt por usuário (não global)
3. ✅ Garantir que cada usuário veja apenas seus dados
4. ✅ Atualizar instance_helper para usar user_id corretamente

---

## 📝 Próximos Passos

1. **Ativar login** (mudar AUTH_REQUIRED para true)
2. **Criar sua conta** (Portal Magra)
3. **Configurar System Prompt** da Portal Magra
4. **Criar outras contas** se precisar (outras empresas)

---

**Vou fazer essas mudanças agora!** 🚀

