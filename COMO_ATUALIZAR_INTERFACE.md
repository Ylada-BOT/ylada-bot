# 🔄 Como Atualizar a Interface

## ⚠️ PROBLEMA: Mudanças não aparecem

Se você fez mudanças mas não aparecem no navegador:

### **1. Limpar Cache do Navegador**

**Chrome/Edge:**
- Pressione `Ctrl+Shift+R` (Windows) ou `Cmd+Shift+R` (Mac)
- Ou: `Ctrl+F5` (Windows) ou `Cmd+Shift+R` (Mac)

**Firefox:**
- Pressione `Ctrl+Shift+R` (Windows) ou `Cmd+Shift+R` (Mac)
- Ou: `Ctrl+F5`

**Safari:**
- Pressione `Cmd+Option+R`

### **2. Reiniciar Servidor Flask**

```bash
# Para o servidor atual
# Pressione Ctrl+C no terminal onde está rodando

# Ou mate o processo:
lsof -ti:5002 | xargs kill

# Reinicie:
python3 web/app.py
```

### **3. Verificar se Arquivo foi Salvo**

Certifique-se de que salvou o arquivo no editor!

### **4. Modo Hard Refresh**

1. Abra DevTools (F12)
2. Clique com botão direito no botão de recarregar
3. Escolha "Esvaziar cache e atualizar forçadamente"

---

## 🔍 VERIFICAR SE ESTÁ ATUALIZADO

### **Teste 1: Verificar Porta**
```bash
curl http://localhost:5002/health
```
Deve retornar: `{"status": "ok"}`

### **Teste 2: Verificar Template**
Abra o código-fonte da página (Ctrl+U) e procure por:
- Se vê `base_tenant.html` → Está atualizado
- Se vê `base.html` → Pode estar desatualizado

### **Teste 3: Verificar Console**
1. Abra DevTools (F12)
2. Vá na aba Console
3. Veja se há erros

---

## 🚀 FORÇAR ATUALIZAÇÃO

### **Opção 1: Hard Refresh**
```
Ctrl+Shift+R (Windows)
Cmd+Shift+R (Mac)
```

### **Opção 2: Limpar Cache Manualmente**
1. DevTools (F12)
2. Aba "Application" ou "Armazenamento"
3. "Limpar dados do site"
4. Recarregar

### **Opção 3: Modo Anônimo**
Abra em janela anônima/privada para testar sem cache

---

**Última atualização:** 23/12/2024





