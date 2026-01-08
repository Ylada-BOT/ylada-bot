# 🔧 Problema: Senha com Hash Incorreto

## 🔍 Problema Identificado

O usuário `portalmagra@gmail.com` existe no banco de dados, mas a senha está com hash **SHA256** quando deveria ser **bcrypt**.

- ❌ **Hash atual**: SHA256 (`8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92`)
- ✅ **Hash necessário**: bcrypt (formato: `$2b$12$...`)

O sistema usa **bcrypt** para autenticação no banco de dados, mas o script SQL criou com SHA256.

---

## ✅ Soluções

### **Opção 1: Usar Endpoint de API (Mais Rápido)** ⭐

Criei um endpoint temporário para atualizar a senha:

```bash
curl -X POST https://yladabot.com/api/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{
    "email": "portalmagra@gmail.com",
    "password": "123456"
  }'
```

Ou use o navegador com JavaScript:

```javascript
fetch('https://yladabot.com/api/auth/reset-password', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'portalmagra@gmail.com',
    password: '123456'
  })
})
.then(r => r.json())
.then(data => console.log(data));
```

### **Opção 2: Executar Script Python Localmente**

1. Instale dependências (se necessário):
   ```bash
   pip install bcrypt sqlalchemy
   ```

2. Execute o script:
   ```bash
   python3 scripts/atualizar_senha_portalmagra.py
   ```

### **Opção 3: Usar Registro (Criar Novo Usuário)**

Se não conseguir atualizar, pode criar um novo usuário:

1. Acesse: https://yladabot.com/register
2. Use um email diferente temporariamente
3. Depois, exclua o usuário antigo e renomeie o novo

---

## 🔍 Verificar se Funcionou

Após atualizar a senha, tente fazer login:

1. Acesse: https://yladabot.com/login
2. Email: `portalmagra@gmail.com`
3. Senha: `123456`

Se ainda não funcionar, verifique os logs do servidor para ver o erro exato.

---

## 📝 Notas Técnicas

- **bcrypt** é usado para hash de senha no banco de dados
- **SHA256** é usado apenas no modo simplificado (arquivo JSON)
- O hash bcrypt tem formato: `$2b$12$...` (60 caracteres)
- O hash SHA256 tem formato: `8d969eef...` (64 caracteres hexadecimais)

---

## 🚀 Próximos Passos

1. Execute o endpoint de API para atualizar a senha
2. Tente fazer login
3. Se funcionar, remova o endpoint temporário `/reset-password` por segurança

