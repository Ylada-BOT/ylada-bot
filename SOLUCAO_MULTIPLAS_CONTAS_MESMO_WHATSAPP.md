# 🔧 Solução: Múltiplas Contas Mostrando o Mesmo WhatsApp

## ⚠️ PROBLEMA

Quando você faz login com contas diferentes:
- **Conta 1:** Nutri (yladanutri@gmail.com)
- **Conta 2:** PORTAL MAGRA (portalmagra@gmail.com)

Ambas as contas estão mostrando o **mesmo WhatsApp conectado** (mesmo número: +55 (19) 98186-8000).

---

## 🔍 CAUSA

O problema era que as chamadas ao servidor WhatsApp **não estavam passando o `user_id`** como parâmetro. Sem o `user_id`, o servidor não sabia qual sessão usar e retornava a mesma sessão para todos os usuários.

### **O que estava acontecendo:**

1. **Conta Nutri** fazia login → `user_id = 2` (por exemplo)
2. **Conta PORTAL MAGRA** fazia login → `user_id = 3` (por exemplo)
3. Ambas faziam requisições para `/chats` **sem passar `user_id`**
4. O servidor WhatsApp retornava a mesma sessão (a primeira que encontrou)
5. Ambas viam o mesmo WhatsApp conectado

---

## ✅ SOLUÇÃO IMPLEMENTADA

Corrigi **todas as chamadas** ao servidor WhatsApp para passar o `user_id`:

### **1. Buscar Conversas (`/api/conversations`)**
```python
# ANTES (ERRADO):
response = requests.get(f"{server_url}/chats", timeout=10)

# DEPOIS (CORRETO):
response = requests.get(f"{server_url}/chats", params={"user_id": user_id}, timeout=10)
```

### **2. Buscar Mensagens (`/api/conversations/<chat_id>/messages`)**
```python
# ANTES (ERRADO):
response = requests.get(f"{server_url}/chats/{chat_id}/messages", params={"limit": limit})

# DEPOIS (CORRETO):
response = requests.get(f"{server_url}/chats/{chat_id}/messages", params={"limit": limit, "user_id": user_id})
```

### **3. Verificar Status (`/api/whatsapp-status`)**
```python
# JÁ ESTAVA CORRETO:
status_response = requests.get(f"{server_url}/status?user_id={user_id}", timeout=3)
```

### **4. Desconectar WhatsApp (`/api/whatsapp-disconnect`)**
```python
# ANTES (ERRADO):
response = requests.post(f"{server_url}/disconnect", timeout=5)

# DEPOIS (CORRETO):
response = requests.post(f"{server_url}/disconnect", json={"user_id": user_id}, timeout=5)
```

### **5. Verificar Status na Página de Instância**
```python
# ANTES (ERRADO):
status_response = requests.get(f"{server_url}/status", timeout=1)

# DEPOIS (CORRETO):
status_response = requests.get(f"{server_url}/status?user_id={user_id}", timeout=1)
```

---

## 🔄 COMO FUNCIONA AGORA

### **Separação por `user_id`:**

1. **Cada usuário tem seu próprio `user_id`** (vem do banco de dados)
2. **Cada `user_id` tem sua própria sessão WhatsApp** no servidor Node.js
3. **Cada sessão é armazenada separadamente:**
   - Diretório de autenticação: `.wwebjs_auth_user_{user_id}`
   - Cache: `.wwebjs_cache_user_{user_id}`
   - Client ID: `ylada_bot_user_{user_id}`

### **Fluxo Correto:**

```
Conta Nutri (user_id=2)
├── Faz login
├── Busca QR Code: /qr?user_id=2
├── Escaneia QR Code → Conecta WhatsApp 1
└── Busca conversas: /chats?user_id=2 → Retorna conversas do WhatsApp 1

Conta PORTAL MAGRA (user_id=3)
├── Faz login
├── Busca QR Code: /qr?user_id=3
├── Escaneia QR Code → Conecta WhatsApp 2
└── Busca conversas: /chats?user_id=3 → Retorna conversas do WhatsApp 2
```

---

## 🧪 COMO TESTAR

### **1. Faça Login com Conta 1 (Nutri)**
1. Acesse: `https://yladabot.com/login`
2. Faça login com: `yladanutri@gmail.com`
3. Vá em "Conectar WhatsApp"
4. Escaneie o QR Code com o WhatsApp da conta Nutri
5. Aguarde conexão
6. Vá em "Conversas" → Deve mostrar conversas do WhatsApp da Nutri

### **2. Faça Logout e Login com Conta 2 (PORTAL MAGRA)**
1. Clique em "Sair"
2. Faça login com: `portalmagra@gmail.com`
3. Vá em "Conectar WhatsApp"
4. Escaneie o QR Code com o WhatsApp da conta PORTAL MAGRA
5. Aguarde conexão
6. Vá em "Conversas" → Deve mostrar conversas do WhatsApp do PORTAL MAGRA

### **3. Verifique se Estão Separadas**
- **Conta Nutri** deve mostrar apenas conversas do WhatsApp da Nutri
- **Conta PORTAL MAGRA** deve mostrar apenas conversas do WhatsApp do PORTAL MAGRA
- **Não devem aparecer conversas misturadas**

---

## 📋 CHECKLIST

- [x] Corrigir chamada `/chats` para passar `user_id`
- [x] Corrigir chamada `/chats/{chat_id}/messages` para passar `user_id`
- [x] Corrigir chamada `/status` na página de instância para passar `user_id`
- [x] Corrigir chamada `/disconnect` para passar `user_id`
- [x] Verificar se `/qr` já estava passando `user_id` (estava correto)
- [x] Verificar se `/api/whatsapp-status` já estava passando `user_id` (estava correto)

---

## 💡 IMPORTANTE

### **Cada Conta Precisa Conectar Seu Próprio WhatsApp**

- **Não** é possível usar o mesmo WhatsApp em duas contas diferentes
- Cada conta precisa escanear seu próprio QR Code
- Cada conta terá seu próprio número de WhatsApp conectado

### **Se Você Quer Usar o Mesmo WhatsApp em Múltiplas Contas:**

Isso **não é possível** com a arquitetura atual. O WhatsApp Web.js não permite que o mesmo número seja conectado em múltiplas sessões simultaneamente.

**Alternativa:** Use **múltiplas instâncias na mesma conta** (veja `COMO_CONECTAR_MULTIPLOS_TELEFONES.md`)

---

## 🚀 PRÓXIMOS PASSOS

1. **Faça deploy das alterações** (se ainda não fez)
2. **Teste com as duas contas** seguindo o passo a passo acima
3. **Verifique se cada conta mostra apenas suas próprias conversas**
4. **Se ainda houver problema**, verifique os logs do servidor WhatsApp para ver qual `user_id` está sendo usado

---

**Última atualização:** 27/01/2025

