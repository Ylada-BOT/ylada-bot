# 📱 Como Conectar o WhatsApp

## Problema Atual

O dashboard pode estar mostrando "Conectado" mesmo quando não está realmente conectado. Isso acontece porque o servidor Node.js está rodando, mas o WhatsApp ainda não foi escaneado.

## Solução: Conectar WhatsApp Passo a Passo

### 1. Verificar se o servidor está rodando

O servidor Node.js precisa estar rodando na porta 5001. Se não estiver:

```bash
cd "/Users/air/Ylada BOT"
node whatsapp_server.js
```

### 2. Acessar a página de QR Code

1. No dashboard, clique no botão **"Conectar WhatsApp"**
2. Ou acesse diretamente: `http://localhost:5002/qr`

### 3. Escanear o QR Code

1. Abra o WhatsApp no seu celular
2. Vá em: **Configurações** > **Aparelhos conectados** > **Conectar um aparelho**
3. Escaneie o QR Code que aparece na tela
4. Aguarde a confirmação de conexão

### 4. Verificar Status

Após escanear:
- O dashboard deve mostrar "✓ Conectado" em verde
- O servidor Node.js deve mostrar "✅ WhatsApp conectado com sucesso!"

## Se ainda mostrar "Conectado" sem estar

### Opção 1: Reiniciar o servidor Node.js

```bash
# Parar o servidor atual (Ctrl+C no terminal onde está rodando)
# Ou matar o processo:
lsof -ti:5001 | xargs kill

# Reiniciar:
node whatsapp_server.js
```

### Opção 2: Limpar sessão antiga

Se houver uma sessão antiga que não está funcionando:

```bash
# Deletar pasta de sessão
rm -rf data/sessions/ylada_bot
```

Depois reinicie o servidor e escaneie o QR Code novamente.

## Verificar Status Real

Para verificar se está realmente conectado:

```bash
curl http://localhost:5001/status
```

Deve retornar:
```json
{
  "ready": true,
  "hasQr": false,
  "actuallyConnected": true,
  "clientInitialized": true
}
```

Se `actuallyConnected` for `false`, você precisa escanear o QR Code.

## Testar Envio de Mensagem

Após conectar, você pode testar enviando uma mensagem:

```bash
curl -X POST http://localhost:5001/send \
  -H "Content-Type: application/json" \
  -d '{"phone": "5511999999999", "message": "Teste"}'
```

Se funcionar, está realmente conectado!

## Próximos Passos

Após conectar:
1. ✅ Criar um fluxo de automação
2. ✅ Enviar uma mensagem de teste
3. ✅ Verificar se o lead é capturado
4. ✅ Verificar se as notificações funcionam
