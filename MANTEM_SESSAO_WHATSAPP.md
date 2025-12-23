# 🔄 Como Manter Sessão do WhatsApp

## ✅ CORREÇÃO APLICADA

A sessão do WhatsApp agora é mantida entre reinicializações do servidor!

### **O que foi feito:**
- ✅ Configurado `dataPath` para salvar sessão em `.wwebjs_auth`
- ✅ Adicionado cache da versão web em `.wwebjs_cache`
- ✅ Sessão persiste mesmo após reiniciar o servidor

---

## 📋 COMO FUNCIONA AGORA

### **Primeira Conexão:**
1. Inicie o servidor: `node whatsapp_server.js`
2. Acesse: `http://localhost:5002/qr`
3. Escaneie o QR Code uma vez
4. ✅ Conectado!

### **Próximas Vezes:**
1. Inicie o servidor: `node whatsapp_server.js`
2. **NÃO precisa escanear QR Code novamente!**
3. ✅ Reconecta automaticamente usando a sessão salva

---

## 🔧 SE PRECISAR RECONECTAR

### **Opção 1: Limpar Sessão e Reconectar**
```bash
# Para servidor
pkill -f "node whatsapp_server.js"

# Limpa sessão
rm -rf .wwebjs_auth
rm -rf .wwebjs_cache

# Reinicia
node whatsapp_server.js
```

Depois escaneie o QR Code novamente.

### **Opção 2: Usar Script de Correção**
```bash
./corrigir_whatsapp.sh
```

---

## 📁 ONDE A SESSÃO É SALVA

- **Sessão:** `.wwebjs_auth/session-ylada_bot/`
- **Cache:** `.wwebjs_cache/`

**⚠️ IMPORTANTE:** Não delete essas pastas se quiser manter a conexão!

---

## 🐛 SE NÃO RECONECTAR AUTOMATICAMENTE

1. **Verifique se as pastas existem:**
   ```bash
   ls -la .wwebjs_auth
   ls -la .wwebjs_cache
   ```

2. **Se não existirem, a sessão foi perdida:**
   - Escaneie o QR Code novamente
   - Na próxima vez, deve reconectar automaticamente

3. **Se existirem mas não reconectar:**
   - Limpe e reconecte (veja Opção 1 acima)

---

**Última atualização:** 23/12/2024

