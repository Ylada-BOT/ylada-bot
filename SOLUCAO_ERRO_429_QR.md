# 🔧 Solução: Erro 429 (Too Many Requests) no QR Code

## ⚠️ PROBLEMA

Erro **429 (Too Many Requests)** ao tentar buscar QR Code.

**Causa:**
- Frontend está fazendo polling muito frequente (a cada 3-5 segundos)
- Railway ou rate limiter está bloqueando muitas requisições

---

## ✅ SOLUÇÃO APLICADA

### **1. Ajustes no Frontend**

Ajustei os intervalos de polling no arquivo `web/templates/instances/connect.html`:

- ✅ Intervalo de verificação de status: **3s → 10s**
- ✅ Retry após erro: **5s → 10s**
- ✅ Delay inicial: **1s → 2s**
- ✅ Tratamento especial para erro 429 (aumenta delay progressivamente)

### **2. Tratamento de Erro 429**

Adicionei tratamento específico:
- Quando recebe erro 429, aumenta o delay progressivamente
- Delay máximo: 30 segundos
- Reseta quando recebe sucesso

---

## 🚀 PRÓXIMOS PASSOS

### **Opção 1: Aguardar e Recarregar (Mais Simples)**

1. **Recarregue a página** (F5)
2. **Aguarde 30-60 segundos** (para o rate limit resetar)
3. **Tente novamente**

### **Opção 2: Fazer Deploy das Alterações**

As alterações que fiz vão reduzir a frequência de requisições:

1. **Faça commit e push:**
   ```bash
   git add web/templates/instances/connect.html
   git commit -m "Reduzir frequência de polling QR code para evitar 429"
   git push
   ```

2. **Aguarde deploy no Railway** (automático)

3. **Teste novamente**

---

## 🔍 VERIFICAÇÃO

Após as alterações, o frontend vai:
- ✅ Fazer requisições a cada **10 segundos** (em vez de 3-5s)
- ✅ Aumentar delay automaticamente se receber 429
- ✅ Reduzir carga no servidor

---

## 📋 CHECKLIST

- [ ] Alterações aplicadas no frontend
- [ ] Commit e push feito (se quiser deployar)
- [ ] Aguardei 30-60 segundos (para rate limit resetar)
- [ ] Recarreguei a página (F5)
- [ ] Testei novamente

---

## 💡 DICA

Se ainda der erro 429:

1. **Aguarde mais tempo** (1-2 minutos)
2. **Recarregue a página** (F5)
3. **Ou faça deploy** das alterações que fiz

---

**Última atualização:** 27/01/2025

