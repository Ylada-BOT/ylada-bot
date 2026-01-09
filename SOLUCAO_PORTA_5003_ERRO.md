# ✅ Solução: Erro "Servidor WhatsApp não está acessível na porta 5003"

## 🐛 PROBLEMA IDENTIFICADO

Pelos logs:
```
[!] Servidor WhatsApp não está acessível em http://whatsapp-server-2 (porta 5003)
[!] Em produção, cada porta precisa de um serviço Node.js separado no Railway
```

**Causa:**
- O usuário 3 estava tentando usar a porta **5003** (calculada como `5001 + (3-1) = 5003`)
- Mas o serviço `whatsapp-server-2` no Railway está rodando apenas na porta **5001**
- Em produção, só temos **UM serviço Node.js** na porta 5001
- Todos os usuários devem usar a **mesma porta** (5001) em produção

---

## ✅ SOLUÇÃO APLICADA

Corrigi a função `get_or_create_user_instance` em `web/utils/instance_helper.py` para:

1. **Em produção:** Todos os usuários usam porta **5001** (único serviço Node.js)
2. **Em desenvolvimento:** Cada usuário usa sua própria porta (5001, 5002, 5003...)

**Mudanças:**
- Detecta se está em produção (`IS_PRODUCTION`)
- Se estiver em produção, força porta 5001 para todos
- Se estiver em desenvolvimento, mantém portas diferentes

---

## 🚀 PRÓXIMOS PASSOS

### **1. Fazer Deploy da Correção**

```bash
git add web/utils/instance_helper.py
git commit -m "Corrigir: todos os usuários usam porta 5001 em produção"
git push
```

### **2. Limpar Instância do Usuário 3 (Opcional)**

Se o usuário 3 já tiver uma instância criada com porta 5003, você pode:

**Opção A:** Deletar o arquivo `data/user_instances.json` no Railway (será recriado automaticamente)

**Opção B:** Aguardar - a correção já atualiza instâncias existentes para porta 5001

### **3. Aguardar Redeploy**

- O Railway vai fazer deploy automaticamente
- Aguarde 1-2 minutos

---

## 🔍 VERIFICAÇÃO

Após o deploy, os logs devem mostrar:

**Antes (erro):**
```
[!] Servidor WhatsApp não está acessível em http://whatsapp-server-2 (porta 5003)
```

**Depois (correto):**
```
[*] Usuário 3 solicitando QR code na porta 5001
[✓] Servidor WhatsApp está rodando em http://whatsapp-server-2:5001
```

---

## 📋 CHECKLIST

- [ ] Correção aplicada no código
- [ ] Commit e push feitos
- [ ] Aguardei deploy no Railway
- [ ] Testei com usuário 3 e funcionou
- [ ] QR code aparece corretamente

---

## 💡 EXPLICAÇÃO TÉCNICA

### **Por que isso aconteceu?**

O sistema foi projetado para suportar múltiplas portas (uma por usuário), mas em produção no Railway:

- ✅ Temos apenas **UM serviço Node.js** (`whatsapp-server-2`)
- ✅ Esse serviço roda apenas na porta **5001**
- ✅ Todos os usuários devem usar a **mesma porta** (5001)

### **Solução:**

- **Desenvolvimento:** Cada usuário tem sua porta (permite testar múltiplas contas localmente)
- **Produção:** Todos usam porta 5001 (único serviço disponível)

---

## 🎯 RESULTADO ESPERADO

Após a correção:

1. ✅ Usuário 1 → Porta 5001
2. ✅ Usuário 2 → Porta 5001
3. ✅ Usuário 3 → Porta 5001
4. ✅ Todos os usuários → Porta 5001

Todos compartilham o mesmo serviço Node.js, mas cada um tem sua própria sessão WhatsApp (separada por `clientId` e `session_dir`).

---

**Última atualização:** 27/01/2025

