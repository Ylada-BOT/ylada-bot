# 🔄 REINICIAR SERVIDOR FLASK

## ⚠️ IMPORTANTE

O erro "Not Found" acontece porque o servidor Flask precisa ser **reiniciado** para carregar as novas rotas!

---

## 🚀 COMO REINICIAR

### **1. Pare o servidor atual:**
- Vá no terminal onde o Flask está rodando
- Pressione: `Ctrl + C`
- Aguarde parar completamente

### **2. Inicie novamente:**
```bash
cd "/Users/air/Ylada BOT"
python web/app.py
```

Ou se estiver usando venv:
```bash
cd "/Users/air/Ylada BOT"
source venv/bin/activate  # Se tiver venv
python web/app.py
```

---

## ✅ DEPOIS DE REINICIAR

1. Acesse: `http://localhost:5002/organizations/new`
2. Deve funcionar sem erro "Not Found"
3. Crie a organização "Portal Magra"
4. ✅ Salvo em `data/organizations.json`

---

## 📋 VERIFICAÇÕES

### **Se ainda der erro:**

1. **Verifique se o servidor está rodando:**
   - Deve aparecer: `Running on http://0.0.0.0:5002`

2. **Verifique se a rota está registrada:**
   - No terminal, deve aparecer: `[✓] Rotas de organizations registradas`

3. **Verifique o template:**
   - Arquivo existe: `web/templates/organizations/create.html`

---

**Reinicie o servidor e teste novamente!** 🔄
