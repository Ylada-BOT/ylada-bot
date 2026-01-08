# 🔄 Como Reiniciar o Servidor para Aplicar Mudanças

## ⚠️ IMPORTANTE

Após qualquer mudança no código ou no `.env`, você precisa **reiniciar o servidor Flask** para aplicar as mudanças.

---

## 🚀 COMO REINICIAR

### **Opção 1: Reiniciar Manualmente (Recomendado)**

1. **Pare o servidor atual:**
   - No terminal onde o Flask está rodando, pressione `Ctrl+C`
   - Ou em outro terminal:
     ```bash
     pkill -f "python.*app.py"
     ```

2. **Inicie novamente:**
   ```bash
   cd "/Users/air/Ylada BOT"
   source venv/bin/activate
   python web/app.py
   ```

### **Opção 2: Reiniciar Automaticamente**

```bash
cd "/Users/air/Ylada BOT"
pkill -f "python.*app.py"
sleep 2
source venv/bin/activate
python web/app.py &
```

---

## ✅ VERIFICAR SE ESTÁ FUNCIONANDO

Após reiniciar, você deve ver no console:

```
[✓] Variáveis de ambiente carregadas de /caminho/para/.env
[✓] IA configurada com API Key do .env (Provider: openai, Model: gpt-4o-mini)
[✓] Rotas de autenticação registradas
...
```

---

## 🔍 VERIFICAR SE API KEY ESTÁ CARREGADA

### **Teste 1: Verificar no Dashboard**
1. Acesse: `http://localhost:5002/`
2. Faça login
3. Vá em "⚙️ Configuração de IA"
4. Deve mostrar: "API Key configurada via .env" (não mostra a chave por segurança)

### **Teste 2: Testar IA**
1. No Dashboard, use "💬 Teste a IA"
2. Digite: "Olá"
3. Deve responder como "Carol" (não erro de API Key)

### **Teste 3: Verificar Logs**
```bash
# Ver últimas linhas do log
tail -20 /tmp/flask.log

# Ou se estiver rodando em foreground, veja o console
```

---

## 🛠️ PROBLEMAS COMUNS

### **Problema: "IA não configurada"**
**Solução:**
1. Verifique se `.env` tem `AI_API_KEY=sk-proj-...`
2. Reinicie o servidor Flask
3. Verifique os logs para ver se carregou

### **Problema: "Erro ao processar com IA"**
**Solução:**
1. Verifique se a API Key está correta no `.env`
2. Verifique se tem créditos na OpenAI
3. Verifique conexão com internet

### **Problema: Mudanças no código não aparecem**
**Solução:**
1. Reinicie o servidor Flask
2. Limpe cache do navegador (Ctrl+Shift+R ou Cmd+Shift+R)

---

## 📝 NOTA

O servidor Flask precisa ser reiniciado sempre que:
- ✅ Mudar algo no `.env`
- ✅ Mudar código Python
- ✅ Adicionar novas rotas
- ✅ Mudar configurações de IA

**Última atualização:** Hoje







