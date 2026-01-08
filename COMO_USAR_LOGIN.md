# 🔐 Como Usar o Sistema com Login

## ✅ Login Ativado!

O sistema agora está configurado para usar login e separar contas.

## 🚀 Primeiro Acesso

### 1. Criar Primeira Conta

1. Acesse: `http://localhost:5002/register`
2. Preencha:
   - **Nome:** Seu nome (ex: "Portal Magra")
   - **Email:** seu@email.com
   - **Senha:** sua senha
3. Clique em **"Criar Conta"**

### 2. Fazer Login

1. Acesse: `http://localhost:5002/login`
2. Digite email e senha
3. Clique em **"Entrar"**

### 3. Configurar System Prompt

1. No Dashboard, vá em **"Configurar IA"**
2. Cole o System Prompt da Portal Magra (do arquivo `system_prompt_sequencia_vendas.txt`)
3. Clique em **"Salvar Configuração"**

**Pronto!** Sua conta está configurada.

---

## 📋 Como Funciona Agora

### Cada Conta Tem:
- ✅ **System Prompt próprio** (salvo em `data/ai_config_user_{user_id}.json`)
- ✅ **WhatsApp próprio** (1 instância por usuário)
- ✅ **Leads próprios** (filtrados por usuário)
- ✅ **Conversas próprias** (filtradas por usuário)
- ✅ **Fluxos próprios** (filtrados por usuário)

### API Key:
- ✅ **Compartilhada** do `.env` (todos usam a mesma chave)
- ✅ **System Prompt** é individual por conta

---

## 🎯 Criar Múltiplas Contas

### Conta 1: Portal Magra
1. Crie conta: `portalmagra@email.com`
2. Configure System Prompt da Portal Magra
3. Conecte WhatsApp

### Conta 2: Outra Empresa
1. Crie conta: `outraempresa@email.com`
2. Configure System Prompt diferente
3. Conecte WhatsApp (porta diferente)

**Cada conta é totalmente independente!**

---

## 🔧 Desabilitar Login (Apenas Desenvolvimento)

Se quiser desabilitar temporariamente:

No arquivo `.env`:
```env
AUTH_REQUIRED=false
```

Ou edite `web/app.py` linha 98:
```python
AUTH_REQUIRED = os.getenv('AUTH_REQUIRED', 'false').lower() == 'true'
```

---

## 📝 Estrutura de Arquivos

```
data/
├── ai_config_user_1.json    # Config da conta 1
├── ai_config_user_2.json    # Config da conta 2
├── user_instances.json      # Instâncias WhatsApp por usuário
└── sessions/
    ├── user_1/              # Sessão WhatsApp do usuário 1
    └── user_2/              # Sessão WhatsApp do usuário 2
```

---

## ✅ Vantagens

1. ✅ **Separação total** entre contas
2. ✅ **System Prompt personalizado** por conta
3. ✅ **Dados isolados** (leads, conversas, fluxos)
4. ✅ **Mais profissional**
5. ✅ **Escalável** (pode ter quantas contas quiser)

---

**Agora você pode ter múltiplas contas, cada uma com seu próprio System Prompt!** 🎉








