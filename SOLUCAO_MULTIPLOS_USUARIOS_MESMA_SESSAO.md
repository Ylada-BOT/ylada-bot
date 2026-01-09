# 🔧 Solução: Múltiplos Usuários Compartilhando Mesma Sessão WhatsApp

## ❌ PROBLEMA

Quando você entra com outro usuário (ex: `ylada nutri @gmail`), o sistema conecta com o **mesmo número de telefone** do usuário anterior.

**Causa:**
- Todos os usuários estão usando a mesma porta (5001) em produção
- O `clientId` é baseado apenas na porta: `ylada_bot_5001`
- A sessão é baseada apenas na porta: `.wwebjs_auth_5001`
- **Todos os usuários compartilham a mesma sessão WhatsApp!**

---

## ✅ SOLUÇÃO

Modificar o servidor Node.js para suportar múltiplos clientes simultaneamente, um por `user_id`.

**Mudanças necessárias:**
1. Servidor aceita `user_id` via query string
2. Gerencia múltiplos clientes WhatsApp simultaneamente
3. Cada cliente tem sua própria sessão baseada no `user_id`

---

## 🚀 IMPLEMENTAÇÃO

### **Opção 1: Modificar Servidor Node.js (Recomendado)**

Modificar `whatsapp_server.js` para:
- Aceitar `user_id` via query string: `/qr?user_id=3`
- Gerenciar múltiplos clientes simultaneamente
- Cada cliente usa: `clientId = ylada_bot_user_${user_id}`

### **Opção 2: Criar Serviços Separados (Mais Simples)**

Criar um serviço Node.js separado no Railway para cada usuário:
- Usuário 1 → Serviço `whatsapp-server-2` (porta 5001)
- Usuário 2 → Serviço `whatsapp-server-3` (porta 5002)
- Usuário 3 → Serviço `whatsapp-server-4` (porta 5003)

**Limitação:** Precisa criar um serviço por usuário no Railway.

---

## 💡 RECOMENDAÇÃO

**Para produção com múltiplos usuários:**

A melhor solução é modificar o servidor Node.js para suportar múltiplos clientes simultaneamente. Isso permite:
- ✅ Múltiplos usuários na mesma porta
- ✅ Cada usuário tem sua própria sessão
- ✅ Não precisa criar múltiplos serviços no Railway

---

## 📋 PRÓXIMOS PASSOS

1. Modificar `whatsapp_server.js` para suportar múltiplos clientes
2. Modificar Flask para passar `user_id` nas requisições
3. Testar com múltiplos usuários

---

**Última atualização:** 27/01/2025

