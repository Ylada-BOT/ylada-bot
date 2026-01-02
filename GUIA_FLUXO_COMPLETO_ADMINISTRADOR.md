# 📖 Guia Completo: Como Funciona o Sistema (Administrador)

## 🎯 VISÃO GERAL

Este guia explica **passo a passo** como você, como administrador, vai usar o sistema para criar e gerenciar seus 11 robôs.

---

## 📋 ESTRUTURA DO SISTEMA

```
👤 VOCÊ (Administrador)
│
└── 🏢 SUA ORGANIZAÇÃO
    │
    ├── 🤖 ROBÔ 1 (WhatsApp 1)
    ├── 🤖 ROBÔ 2 (WhatsApp 2)
    ├── 🤖 ROBÔ 3 (WhatsApp 3)
    ├── ... (até 11 robôs)
    └── 🤖 ROBÔ 11 (WhatsApp 11)
```

---

## 🚀 PASSO A PASSO COMPLETO

### **PASSO 1: Criar Sua Conta (Login)**

#### **Opção A: Via Interface Web**

1. Acesse: `http://localhost:5002/register`
2. Preencha:
   - **Nome:** Seu nome completo
   - **Email:** seu@email.com
   - **Senha:** Sua senha segura
3. Clique em "Criar Conta"
4. Você será redirecionado para fazer login

#### **Opção B: Via API (Terminal)**

```bash
curl -X POST http://localhost:5002/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "seu@email.com",
    "password": "sua-senha",
    "name": "Seu Nome"
  }'
```

**Resultado:**
- ✅ Sua conta é criada
- ✅ Você recebe um token de acesso
- ✅ Você pode fazer login

---

### **PASSO 2: Fazer Login**

1. Acesse: `http://localhost:5002/login`
2. Digite:
   - **Email:** seu@email.com
   - **Senha:** sua-senha
3. Clique em "Entrar"

**O que acontece:**
- ✅ Você é autenticado
- ✅ É redirecionado para o dashboard
- ✅ Sua sessão é criada

---

### **PASSO 3: Criar Sua Organização**

**O que é uma Organização?**
- É como uma "empresa" ou "projeto" no sistema
- Você pode ter várias organizações
- Cada organização pode ter vários robôs

#### **Como Criar:**

1. No dashboard, vá em **"Organizações"** (ou `/admin/organizations`)
2. Clique em **"+ Criar Organização"**
3. Preencha:
   - **Nome:** "Minha Empresa" (ou o nome que quiser)
4. Clique em "Criar"

**Resultado:**
- ✅ Organização criada
- ✅ Você é o dono dessa organização
- ✅ Agora pode criar robôs dentro dela

---

### **PASSO 4: Criar Seus 11 Robôs (Instâncias)**

**O que é um Robô (Instance)?**
- É um WhatsApp conectado ao sistema
- Cada robô tem seu próprio número de WhatsApp
- Cada robô funciona de forma independente

#### **Como Criar Cada Robô:**

**Método 1: Via Interface Web**

1. Vá em **"Instâncias"** (ou `/admin/instances`)
2. Clique em **"+ Criar Instância"**
3. Preencha:
   - **Nome:** "Robô 1", "Robô 2", etc.
   - **Organização:** Selecione sua organização
4. Clique em "Criar"
5. **Repita isso 11 vezes** (um para cada robô)

**Método 2: Via API (Mais Rápido para 11 robôs)**

```bash
# Criar Robô 1
curl -X POST http://localhost:5002/api/instances \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Robô 1",
    "tenant_id": 1
  }'

# Criar Robô 2
curl -X POST http://localhost:5002/api/instances \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Robô 2",
    "tenant_id": 1
  }'

# ... (repita para os outros 9 robôs)
```

**Resultado:**
- ✅ Você terá 11 robôs criados
- ✅ Cada um terá uma porta diferente (5001, 5002, 5003, etc.)
- ✅ Cada um está pronto para conectar um WhatsApp

---

### **PASSO 5: Conectar WhatsApp em Cada Robô**

Para cada um dos 11 robôs:

1. Vá em **"Instâncias"** no dashboard
2. Clique no robô que quer conectar (ex: "Robô 1")
3. Clique em **"Conectar WhatsApp"** ou **"Ver QR Code"**
4. Escaneie o QR Code com seu WhatsApp
5. Aguarde a conexão (status muda para "Conectado")
6. **Repita para os outros 10 robôs**

**Importante:**
- Cada robô precisa de um WhatsApp diferente
- Você pode usar:
  - 11 números de celular diferentes
  - Ou criar 11 contas WhatsApp Business diferentes

---

### **PASSO 6: Configurar Agentes (Opcional, mas Recomendado)**

**O que é um Agente?**
- É a "personalidade" do robô
- Define como ele responde quando não há fluxo ativo
- Cada robô pode ter seu próprio agente

#### **Como Criar um Agente:**

1. Vá em **"Agentes"** (ou `/admin/agents`)
2. Clique em **"+ Criar Agente"**
3. Preencha:
   - **Nome:** "Agente Vendas", "Agente Suporte", etc.
   - **Provider:** OpenAI ou Anthropic
   - **Model:** gpt-4o-mini, claude-3-haiku, etc.
   - **System Prompt:** "Você é um vendedor amigável..."
   - **Temperatura:** 0.7 (padrão)
4. Clique em "Criar"

#### **Associar Agente a um Robô:**

1. Vá em **"Instâncias"**
2. Clique no robô
3. Clique em **"Editar"**
4. Selecione o **Agente** desejado
5. Salve

**Resultado:**
- ✅ Cada robô pode ter seu próprio comportamento
- ✅ Respostas personalizadas por robô

---

### **PASSO 7: Criar Fluxos (Automações)**

**O que é um Fluxo?**
- É uma automação que responde automaticamente
- Exemplo: quando alguém manda "oi" → responde "Olá! Como posso ajudar?"

#### **Tipos de Fluxos:**

**A) Fluxos Compartilhados** (todos os robôs usam):
- Útil para: "Boas-vindas", "Promoções", etc.
- `instance_id` = NULL

**B) Fluxos Específicos** (só um robô usa):
- Útil para: "Cardápio do Robô 1", "Horário do Robô 2", etc.
- `instance_id` = ID do robô

#### **Como Criar um Fluxo:**

1. Vá em **"Fluxos"** (ou `/flows`)
2. Clique em **"+ Criar Fluxo"**
3. Configure:
   - **Nome:** "Boas-vindas"
   - **Trigger:** Palavra-chave "oi", "olá"
   - **Ações:** Enviar mensagem "Olá! Bem-vindo!"
4. Se quiser específico de um robô, selecione o **Robô**
5. Clique em "Salvar"

**Exemplo de Fluxo Compartilhado:**
```json
{
  "name": "Boas-vindas",
  "trigger": {
    "type": "keyword",
    "keywords": ["oi", "olá", "bom dia"]
  },
  "steps": [
    {
      "type": "send_message",
      "message": "Olá! Bem-vindo! Como posso ajudar?"
    }
  ]
}
```

---

## 📊 RESUMO DO FLUXO COMPLETO

```
1. Criar Conta (Register)
   ↓
2. Fazer Login
   ↓
3. Criar Organização
   ↓
4. Criar 11 Robôs (Instâncias)
   ↓
5. Conectar WhatsApp em cada robô
   ↓
6. (Opcional) Configurar Agentes
   ↓
7. Criar Fluxos (Automações)
   ↓
8. PRONTO! Seus 11 robôs estão funcionando!
```

---

## 🎯 ÁREAS DO SISTEMA

### **Área do Usuário** (`/`)
- Dashboard principal
- Ver seus robôs
- Ver conversas
- Gerenciar fluxos
- Configurar IA

### **Área Administrativa** (`/admin`)
- Gerenciar usuários
- Gerenciar organizações
- Gerenciar instâncias (robôs)
- Ver logs
- Analytics

---

## ❓ PERGUNTAS FREQUENTES

### **1. Preciso criar 11 organizações para 11 robôs?**
❌ **NÃO!** Você pode ter todos os 11 robôs em **UMA organização**.

### **2. Cada robô precisa de um WhatsApp diferente?**
✅ **SIM!** Cada robô conecta um WhatsApp diferente.

### **3. Posso usar o mesmo número em vários robôs?**
❌ **NÃO!** Cada robô precisa de um número único.

### **4. Como faço login depois?**
1. Acesse `/login`
2. Digite email e senha
3. Pronto!

### **5. Posso criar usuários para outras pessoas?**
✅ **SIM!** Como administrador, você pode:
- Criar usuários na área `/admin/users`
- Cada usuário pode ter suas próprias organizações
- Ou você pode dar acesso à sua organização

### **6. Os fluxos são compartilhados entre robôs?**
✅ **SIM e NÃO:**
- Fluxos **compartilhados** (`instance_id = NULL`) → todos os robôs usam
- Fluxos **específicos** (`instance_id = X`) → só aquele robô usa

---

## 🔐 SEGURANÇA E AUTENTICAÇÃO

### **Como Funciona o Login:**

1. **Registro:**
   - Você cria uma conta com email e senha
   - Senha é criptografada (hash)
   - Conta é salva no banco de dados

2. **Login:**
   - Você digita email e senha
   - Sistema verifica se está correto
   - Cria uma sessão (cookie)
   - Você fica logado

3. **Sessão:**
   - Enquanto você está logado, pode acessar tudo
   - Se fechar o navegador, pode precisar fazer login novamente
   - (Depende da configuração)

### **Roles (Papéis):**

- **ADMIN:** Você (pode tudo)
- **USER:** Usuário comum (só vê suas coisas)
- **RESELLER:** Revendedor (pode criar organizações para clientes)

---

## 📝 EXEMPLO PRÁTICO COMPLETO

### **Cenário: Você quer 11 robôs para vender produtos**

```
1. Criar Conta
   Email: vendedor@empresa.com
   Senha: ********
   ↓
2. Login
   Acessa o sistema
   ↓
3. Criar Organização
   Nome: "Minha Loja"
   ↓
4. Criar 11 Robôs
   - Robô 1: "Vendas Loja 1"
   - Robô 2: "Vendas Loja 2"
   - ... (até Robô 11)
   ↓
5. Conectar WhatsApp
   Cada robô conecta um número diferente
   ↓
6. Criar Agente
   Nome: "Vendedor Amigável"
   Prompt: "Você é um vendedor..."
   ↓
7. Associar Agente aos Robôs
   Todos os 11 robôs usam o mesmo agente
   ↓
8. Criar Fluxos
   - "Boas-vindas" (compartilhado)
   - "Cardápio" (compartilhado)
   - "Promoção" (compartilhado)
   ↓
9. PRONTO!
   Seus 11 robôs estão respondendo automaticamente!
```

---

## 🎉 CONCLUSÃO

**Resumo rápido:**

1. ✅ Crie sua conta (register)
2. ✅ Faça login
3. ✅ Crie uma organização
4. ✅ Crie 11 robôs (instâncias)
5. ✅ Conecte WhatsApp em cada um
6. ✅ Configure agentes (opcional)
7. ✅ Crie fluxos (automações)
8. ✅ **PRONTO! Seus robôs estão funcionando!**

**Tempo estimado:** 30-60 minutos para configurar tudo.

---

**Última atualização:** 2024-12-23


