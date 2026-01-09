# 🔌 Como Funcionam as Portas no Sistema

## 📋 VISÃO GERAL

O sistema usa **múltiplas portas** para separar diferentes serviços:

1. **Porta 5002** → Servidor Flask (aplicação web principal)
2. **Porta 5001, 5003, 5004...** → Servidores WhatsApp (um para cada conta)

---

## 🏗️ ARQUITETURA COMPLETA

### **1. Porta 5002 - Servidor Flask (Principal)**

**O que é:**
- Aplicação web principal (Python/Flask)
- Dashboard, login, configurações
- API REST
- Interface web completa

**O que faz:**
- ✅ Gerencia usuários e autenticação
- ✅ Dashboard e interface web
- ✅ API para frontend
- ✅ Gerencia instâncias WhatsApp
- ✅ Conecta com banco de dados (Supabase)
- ✅ Processa fluxos e mensagens

**Como funciona:**
```bash
# Localmente
python3 web/app.py
# Roda na porta 5002

# Em produção (Railway)
# Railway define PORT automaticamente (pode ser 5002, 3000, etc.)
# O código lê: port = int(os.getenv('PORT', 5002))
```

**URLs:**
- Local: `http://localhost:5002`
- Produção: `https://seu-projeto.railway.app`

---

### **2. Portas 5001, 5003, 5004... - Servidores WhatsApp**

**O que são:**
- Servidores Node.js separados
- Cada um gerencia **UMA conta WhatsApp**
- Cada porta = uma instância/conta diferente

**Por que múltiplas portas?**
- ✅ Cada conta WhatsApp precisa de sua própria sessão
- ✅ Cada conta tem seu próprio QR Code
- ✅ Cada conta tem seu próprio cache e autenticação
- ✅ Permite múltiplos usuários conectarem WhatsApp simultaneamente

**Como funciona:**
```bash
# Porta 5001 - Primeira conta
PORT=5001 node whatsapp_server.js

# Porta 5002 - Segunda conta (não confundir com Flask!)
PORT=5002 node whatsapp_server.js

# Porta 5003 - Terceira conta
PORT=5003 node whatsapp_server.js
```

**Mapeamento:**
- Usuário 1 → Porta 5001
- Usuário 2 → Porta 5002 (WhatsApp, não Flask!)
- Usuário 3 → Porta 5003
- Usuário 4 → Porta 5004
- etc.

---

## 🔄 COMO FUNCIONA EM PRODUÇÃO (Railway)

### **Estrutura no Railway:**

```
Projeto Railway
├── Serviço 1: Flask (Python)
│   ├── Porta: Definida pelo Railway (ex: 5002)
│   ├── URL: https://seu-projeto.railway.app
│   └── Variáveis: DATABASE_URL, SECRET_KEY, etc.
│
└── Serviço 2: WhatsApp Server (Node.js)
    ├── Porta: Definida pelo Railway (ex: 5001)
    ├── URL: https://whatsapp-server.railway.app
    └── Variáveis: PORT=5001
```

### **Como o Flask se conecta com WhatsApp:**

1. **Flask (porta 5002)** recebe requisição: "Conectar WhatsApp"
2. **Flask** verifica qual porta usar (5001, 5002, 5003...)
3. **Flask** faz requisição HTTP para: `http://whatsapp-server:5001/qr`
4. **WhatsApp Server** retorna o QR Code
5. **Flask** exibe o QR Code para o usuário

**Variável importante:**
```bash
# No Flask (Railway)
WHATSAPP_SERVER_URL=https://whatsapp-server.railway.app
# ou
WHATSAPP_SERVER_URL=http://whatsapp-server:5001  # Se estiver no mesmo projeto
```

---

## 🏠 COMO FUNCIONA LOCALMENTE

### **Estrutura Local:**

```
Seu Computador
├── Terminal 1: Flask
│   └── python3 web/app.py (porta 5002)
│
└── Terminal 2, 3, 4...: WhatsApp Servers
    ├── PORT=5001 node whatsapp_server.js
    ├── PORT=5002 node whatsapp_server.js
    └── PORT=5003 node whatsapp_server.js
```

### **Inicialização Automática:**

O sistema pode iniciar servidores WhatsApp automaticamente:

1. Usuário acessa: `http://localhost:5002/connect`
2. Flask detecta: "Preciso de servidor na porta 5001"
3. Flask verifica: "Servidor está rodando?"
4. Se não estiver, Flask inicia: `PORT=5001 node whatsapp_server.js`
5. Flask busca QR Code: `http://localhost:5001/qr`

---

## 🔑 VARIÁVEIS DE AMBIENTE IMPORTANTES

### **No Flask (.env.local ou Railway):**

```bash
# Porta do Flask (Railway define automaticamente)
PORT=5002

# URL do servidor WhatsApp
WHATSAPP_SERVER_URL=http://localhost:5001  # Local
# ou
WHATSAPP_SERVER_URL=https://whatsapp-server.railway.app  # Produção

# Banco de dados
DATABASE_URL=postgresql://postgres.tbbjqvvtsotjqgfygaaj:senha@aws-0-us-west-2.pooler.supabase.com:5432/postgres
```

### **No WhatsApp Server:**

```bash
# Porta do servidor WhatsApp
PORT=5001  # ou 5002, 5003, etc.
```

---

## 📊 FLUXO COMPLETO DE UMA MENSAGEM

### **1. Usuário envia mensagem no WhatsApp**

```
WhatsApp → Servidor WhatsApp (porta 5001)
```

### **2. Servidor WhatsApp processa**

```
Servidor WhatsApp → Verifica se tem fluxo ativo
                 → Se sim, executa fluxo
                 → Se não, envia para IA
```

### **3. Servidor WhatsApp envia para Flask**

```
Servidor WhatsApp → POST http://localhost:5002/webhook
```

### **4. Flask processa**

```
Flask → Salva mensagem no banco
     → Processa fluxo/IA
     → Retorna resposta
```

### **5. Flask envia resposta**

```
Flask → POST http://localhost:5001/send
```

### **6. Servidor WhatsApp envia**

```
Servidor WhatsApp → Envia mensagem no WhatsApp
```

---

## 🎯 RESUMO

| Porta | Serviço | O que faz | Quando usar |
|-------|----------|-----------|-------------|
| **5002** | Flask | Aplicação web principal | Sempre (único) |
| **5001** | WhatsApp | Primeira conta WhatsApp | Quando usuário 1 conectar |
| **5002** | WhatsApp | Segunda conta WhatsApp | Quando usuário 2 conectar |
| **5003** | WhatsApp | Terceira conta WhatsApp | Quando usuário 3 conectar |
| **5004+** | WhatsApp | Outras contas | Quando mais usuários conectarem |

---

## ⚠️ IMPORTANTE

### **Em Produção (Railway):**

- ✅ **DATABASE_URL** deve ser configurada **APENAS no Railway** (variável de ambiente)
- ✅ **NÃO** precisa atualizar em múltiplas portas
- ✅ **NÃO** precisa atualizar em múltiplos serviços
- ✅ Apenas **1 variável DATABASE_URL** no serviço Flask

### **Por quê?**

- O banco de dados é **compartilhado** entre todos os serviços
- Todos os serviços (Flask, WhatsApp servers) usam a **mesma DATABASE_URL**
- Mas cada serviço tem sua própria **porta** para comunicação

---

## 🔍 EXEMPLO PRÁTICO

### **Cenário: 3 usuários conectados**

```
Railway
├── Serviço Flask (porta 5002)
│   └── DATABASE_URL=postgresql://... (ÚNICA)
│
└── Serviço WhatsApp (porta 5001)
    ├── Usuário 1 → Porta 5001
    ├── Usuário 2 → Porta 5002
    └── Usuário 3 → Porta 5003
```

**Todas as instâncias WhatsApp usam o mesmo banco, mas cada uma tem sua própria porta!**

---

**Última atualização:** 27/01/2025

