# 🔧 Como Configurar Z-API no Bot Ylada

## 📝 Passo a Passo Completo

### 1. Criar Conta no Z-API

1. Acesse: https://developer.z-api.io
2. Clique em "Criar Conta" ou "Cadastrar"
3. Preencha seus dados
4. Confirme o email

### 2. Ativar Teste Grátis (2 dias)

1. Faça login no dashboard
2. Procure por "Teste Grátis" ou "Free Trial"
3. Ative o teste (não precisa de cartão)

### 3. Criar uma Instância

1. No dashboard, clique em **"Instâncias"** ou **"Criar Instância"**
2. Dê um nome para sua instância (ex: "Bot Ylada")
3. Clique em **"Criar"**

### 4. Conectar seu WhatsApp

1. Após criar a instância, aparecerá um **QR Code**
2. Abra o WhatsApp no seu celular
3. Vá em **Configurações > Aparelhos conectados > Conectar um aparelho**
4. Escaneie o QR Code
5. Pronto! Seu WhatsApp está conectado

### 5. Obter Credenciais

No dashboard da instância, você verá:
- **Instance ID:** (ex: `3C7F8A9B2D1E4F5A`)
- **Token:** (ex: `ABC123XYZ789...`)

**IMPORTANTE:** Guarde essas informações com segurança!

### 6. Configurar no Bot Ylada

#### Opção A: Arquivo de Configuração

Edite `config/config.yaml`:

```yaml
zapi:
  instance_id: "SEU_INSTANCE_ID_AQUI"
  token: "SEU_TOKEN_AQUI"
  base_url: "https://api.z-api.io"
```

#### Opção B: Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
ZAPI_INSTANCE_ID=seu_instance_id_aqui
ZAPI_TOKEN=seu_token_aqui
ZAPI_BASE_URL=https://api.z-api.io
```

### 7. Ativar Modo Z-API no Bot

#### Opção A: Variável de Ambiente
```bash
export BOT_MODE=zapi
python web/app.py
```

#### Opção B: Editar Código
Edite `web/app.py` e mude:
```python
BOT_MODE = os.getenv("BOT_MODE", "zapi")  # Mude de "simple" para "zapi"
```

### 8. Testar

1. Inicie o bot:
```bash
cd "/Users/air/EXTRATOR EUA"
source .venv/bin/activate
python web/app.py
```

2. Acesse: http://localhost:5001

3. Teste enviando uma mensagem:
   - Vá em "Testar Bot"
   - Ou use o endpoint `/send`

---

## ✅ Checklist de Configuração

- [ ] Conta criada no Z-API
- [ ] Teste grátis ativado
- [ ] Instância criada
- [ ] WhatsApp conectado (QR Code escaneado)
- [ ] Instance ID copiado
- [ ] Token copiado
- [ ] Config.yaml atualizado
- [ ] Modo Z-API ativado no bot
- [ ] Bot iniciado e testado

---

## 🧪 Teste Rápido

### Via Dashboard Web:
1. Acesse: http://localhost:5001/test
2. Clique em "Enviar Mensagem"
3. Digite um número e mensagem
4. Verifique se chegou no WhatsApp

### Via API:
```bash
curl -X POST http://localhost:5001/send \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "5511999999999",
    "message": "Teste do Bot Ylada com Z-API!"
  }'
```

---

## 🔍 Verificar se Está Funcionando

### 1. Verificar Status
```bash
curl http://localhost:5001/health
```

### 2. Verificar Modo
```bash
curl http://localhost:5001/conversations
```

Deve retornar:
```json
{
  "mode": "zapi",
  ...
}
```

### 3. Verificar Logs
No terminal onde o bot está rodando, você verá:
```
[*] Modo Z-API ativado
[✓] Mensagem enviada para 5511999999999
```

---

## ⚠️ Problemas Comuns

### Erro: "Z-API Instance ID e Token são obrigatórios"
**Solução:** Verifique se configurou corretamente no `config.yaml` ou `.env`

### Erro: "Erro ao enviar mensagem"
**Solução:** 
- Verifique se a instância está ativa no dashboard Z-API
- Verifique se o WhatsApp ainda está conectado
- Confirme se o número está no formato correto (5511999999999)

### Mensagem não chega
**Solução:**
- Verifique se o número está correto (com código do país)
- Verifique se a instância está online no dashboard
- Veja os logs do bot para mais detalhes

---

## 💡 Dicas

1. **Mantenha o WhatsApp conectado:** Se desconectar, escaneie o QR Code novamente
2. **Teste primeiro:** Use o teste grátis de 2 dias antes de assinar
3. **Backup das credenciais:** Guarde Instance ID e Token em local seguro
4. **Monitoramento:** Use o dashboard Z-API para ver estatísticas

---

## 📞 Suporte

- **Z-API:** Suporte 24/7 no dashboard
- **Documentação:** https://developer.z-api.io/docs
- **Bot Ylada:** Verifique os logs e o dashboard web

---

## 🎯 Próximos Passos

1. ✅ Configure Z-API
2. ✅ Teste o bot
3. ✅ Se gostar, assine o plano mensal (R$ 99,90/mês)
4. ✅ Use em produção!

