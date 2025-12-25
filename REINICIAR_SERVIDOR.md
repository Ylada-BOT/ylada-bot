# 🔄 Reiniciar Servidor Flask

## ⚠️ IMPORTANTE

O servidor Flask precisa ser **reiniciado** para carregar a nova connection string do Supabase!

## 📋 COMO REINICIAR

### **1. Pare o servidor atual**

No terminal onde o Flask está rodando:
- Pressione **Ctrl+C** para parar

### **2. Inicie novamente**

```bash
python3 web/app.py
```

Ou se estiver usando outro comando:
```bash
python web/app.py
```

---

## ✅ DEPOIS DE REINICIAR

Você deve ver mensagens como:
```
[✓] Banco de dados conectado
[✓] Rotas de organizations registradas
```

---

## 🧪 TESTAR

Depois de reiniciar:

1. Acesse: `http://localhost:5002/admin/organizations`
2. Clique em **"+ Nova Organização"**
3. Preencha o nome
4. Clique em **"Criar Organização"**
5. Deve funcionar e salvar no Supabase! 🎉

---

**O servidor precisa ser reiniciado para carregar as novas variáveis de ambiente!**

