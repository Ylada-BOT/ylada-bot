# 🔧 Solução: QR Code Não Escaneia

## ❌ PROBLEMA

O QR Code aparece na tela, mas quando você tenta escanear no WhatsApp, diz "não é possível escanear".

---

## 🔍 CAUSAS POSSÍVEIS

### **1. QR Code Expirado** ⭐ **MAIS COMUM**

**Problema:**
- QR Code do WhatsApp expira em ~20 segundos
- Se você demorar para escanear, o QR Code fica inválido
- Precisa gerar um novo QR Code

**Solução:**
- ✅ QR Code agora atualiza automaticamente a cada 3 segundos
- ✅ Sempre terá um QR Code válido na tela
- ✅ Escaneie rapidamente quando aparecer

---

### **2. Servidor Node.js Não Está Rodando**

**Problema:**
- Servidor WhatsApp precisa estar rodando na porta 5001

**Solução:**
```bash
# Verifica se está rodando
lsof -ti:5001

# Se não estiver, inicia:
node whatsapp_server.js
```

---

### **3. QR Code Mal Formatado**

**Problema:**
- QR Code pode estar sendo gerado incorretamente

**Solução:**
- ✅ Corrigido: QR Code agora usa formato correto
- ✅ Tamanho aumentado para 300x300 (mais fácil de escanear)
- ✅ Margem aumentada

---

## ✅ CORREÇÕES APLICADAS

1. ✅ QR Code atualiza automaticamente a cada 3 segundos
2. ✅ Tamanho aumentado (300x300)
3. ✅ Margem melhorada
4. ✅ Tratamento de erros melhorado

---

## 🚀 COMO USAR AGORA

1. **Acesse:** `http://localhost:5002/qr`
2. **Aguarde:** QR Code aparece (atualiza automaticamente)
3. **Abra WhatsApp no celular:**
   - Vá em: **Configurações > Aparelhos conectados**
   - Toque em: **"Conectar um aparelho"**
4. **Escaneie rapidamente:** QR Code aparece na tela
5. **Pronto!** WhatsApp conecta automaticamente

---

## 💡 DICAS

1. **Escaneie rápido:** QR Code expira em ~20 segundos
2. **Mantenha a página aberta:** QR Code atualiza automaticamente
3. **Se não funcionar:** Recarregue a página (`F5`)

---

## 🔄 SE AINDA NÃO FUNCIONAR

### **Verificar Servidor:**
```bash
# Verifica se servidor está rodando
curl http://localhost:5001/health

# Deve retornar: {"status":"ok","ready":false}
```

### **Reiniciar Servidor:**
```bash
# Para o servidor atual
pkill -f "node whatsapp_server.js"

# Inicia novamente
node whatsapp_server.js
```

### **Verificar QR Code:**
```bash
# Verifica se QR Code está sendo gerado
curl http://localhost:5001/qr

# Deve retornar: {"qr":"...","ready":false}
```

---

**Última atualização:** 13/12/2024


