# 🔧 Solução de Problemas - Tenants e QR Code

## ❌ PROBLEMA 1: Erro ao Criar Tenant

### **Causa:**
- Banco de dados não está configurado
- Ou usuário não existe no banco

### **Solução Rápida:**

**Opção A: Usar Modo Simples (Sem Tenants)**
- Acesse `/dashboard` diretamente
- Use o sistema sem precisar criar tenants
- Funciona com o sistema antigo

**Opção B: Configurar Banco de Dados**
```bash
# 1. Configure DATABASE_URL no .env
export DATABASE_URL="postgresql://usuario:senha@localhost/ylada_bot"

# 2. Inicialize o banco
python scripts/init_db.py

# 3. Tente criar tenant novamente
```

**Opção C: Modo Desenvolvimento (Sem Banco)**
- O sistema agora cria usuário automaticamente
- Funciona mesmo sem banco configurado (com limitações)

---

## ❌ PROBLEMA 2: QR Code Não Funciona

### **Causa:**
- Servidor Node.js não está rodando na porta da instância
- Cada instância precisa de seu próprio servidor Node.js

### **Solução:**

**Para funcionar, você precisa:**

1. **Iniciar servidor Node.js para a instância**
   - Cada instância tem uma porta (5001, 5002, etc)
   - Precisa iniciar `whatsapp_server.js` na porta da instância

2. **Modificar whatsapp_server.js para aceitar porta dinâmica**
   - Atualmente está fixo na porta 5001
   - Precisa aceitar porta como parâmetro

---

## 🛠️ CORREÇÃO RÁPIDA

### **Para QR Code Funcionar Agora:**

1. **Use o sistema antigo primeiro:**
   - Acesse `/qr` (não `/instances/:id/connect`)
   - Funciona com o servidor na porta 5001

2. **Ou inicie servidor manualmente:**
```bash
# Inicia servidor na porta 5001
node whatsapp_server.js
```

3. **Depois acesse:**
   - `/qr` para conectar
   - Ou `/instances/:id/connect` (se servidor estiver na porta da instância)

---

## 💡 RECOMENDAÇÃO

**Por enquanto, use o sistema simples:**
1. Acesse `/dashboard`
2. Clique em "Conectar WhatsApp"
3. Use `/qr` para escanear QR Code
4. Funciona sem precisar criar tenants

**Depois, quando banco estiver configurado:**
1. Configure PostgreSQL
2. Inicialize banco
3. Aí sim use o sistema de tenants

---

**Última atualização:** 13/12/2024


