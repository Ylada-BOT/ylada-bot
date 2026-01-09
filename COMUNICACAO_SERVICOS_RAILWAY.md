# 🔗 Comunicação Entre Serviços no Railway

## ✅ CADA SERVIÇO PODE TER SEU PRÓPRIO DOMÍNIO

No Railway, **cada serviço pode ter seu próprio domínio**:

- **ylada-bot** (Flask) → `https://yladabot.com`
- **whatsapp-server-2** (Node.js) → `https://whatsapp-server-2.railway.app` (ou outro)

**Isso é normal e recomendado!** ✅

---

## 🎯 OPÇÕES DE COMUNICAÇÃO

### **Opção 1: Domínios Separados (Recomendado)** ✅

Cada serviço tem seu próprio domínio:

```
ylada-bot → https://yladabot.com
whatsapp-server-2 → https://whatsapp-server-2.railway.app
```

**Configuração:**
- No serviço `ylada-bot`, variável:
  ```bash
  WHATSAPP_SERVER_URL=https://whatsapp-server-2.railway.app
  ```

**Vantagens:**
- ✅ Cada serviço é independente
- ✅ Fácil de gerenciar
- ✅ Escala separadamente

---

### **Opção 2: Comunicação Interna (Mais Eficiente)** ⭐

No Railway, serviços no mesmo projeto podem se comunicar internamente usando o nome do serviço:

```
whatsapp-server-2 → http://whatsapp-server-2:5001
```

**Configuração:**
- No serviço `ylada-bot`, variável:
  ```bash
  WHATSAPP_SERVER_URL=http://whatsapp-server-2:5001
  ```

**Vantagens:**
- ✅ Mais rápido (comunicação interna)
- ✅ Não precisa de domínio público
- ✅ Mais seguro (não exposto externamente)

**Como funciona:**
- Railway cria uma rede interna entre serviços
- Usa o nome do serviço como hostname
- Porta é a mesma (5001)

---

### **Opção 3: Mesmo Domínio com Rotas (Avançado)**

Usar o mesmo domínio com rotas diferentes (requer configuração de proxy/nginx).

**Não recomendado** para este caso.

---

## 🚀 RECOMENDAÇÃO

### **Use Opção 2 (Comunicação Interna):**

1. **No serviço `ylada-bot`, Variables:**
   ```bash
   WHATSAPP_SERVER_URL=http://whatsapp-server-2:5001
   ```

2. **Não precisa gerar domínio** para o whatsapp-server-2
3. **Comunicação é interna** (mais rápido e seguro)

---

## 📋 CONFIGURAÇÃO FINAL

### **Serviço ylada-bot (Flask):**

**Variables:**
```bash
DATABASE_URL=postgresql://...
SECRET_KEY=...
WHATSAPP_SERVER_URL=http://whatsapp-server-2:5001  ← Comunicação interna!
```

### **Serviço whatsapp-server-2 (Node.js):**

**Variables:**
```bash
PORT=5001
NODE_ENV=production
```

**Networking:**
- Não precisa gerar domínio público (opcional)
- Pode deixar sem domínio se usar comunicação interna

---

## 🔍 VERIFICAÇÃO

Após configurar, teste:

1. **Acesse:** `https://yladabot.com/qr`
2. **Deve funcionar** mesmo sem domínio público no whatsapp-server-2
3. **Comunicação é interna** entre os serviços

---

## 💡 RESUMO

| Opção | URL | Quando Usar |
|-------|-----|-------------|
| **Interna** | `http://whatsapp-server-2:5001` | ✅ Recomendado (mais rápido) |
| **Pública** | `https://whatsapp-server-2.railway.app` | Se precisar acessar externamente |

**Para seu caso, use comunicação interna!** ✅

---

**Última atualização:** 27/01/2025

