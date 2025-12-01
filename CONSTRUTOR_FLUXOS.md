# 🎨 Construtor Visual de Fluxos - Bot Ylada

## ✅ Implementado!

O construtor visual de fluxos está pronto para uso pessoal e preparado para comercialização!

## 🚀 Como Acessar

1. **Acesse o dashboard:** http://localhost:5002
2. **Clique em "🎨 Construtor de Fluxos"** no menu lateral
3. **Ou acesse diretamente:** http://localhost:5002/flow-builder

## 📋 Funcionalidades

### ✅ Componentes Disponíveis

#### Mensagens
- **💬 Mensagem** - Envia mensagem simples
- **❓ Pergunta** - Faz pergunta e salva resposta

#### Ações
- **🔑 Palavra-chave** - Responde a palavras-chave específicas
- **🔀 Condição** - Lógica condicional (if/else)
- **⏱️ Aguardar** - Adiciona delay entre ações

#### Integrações
- **🔗 Webhook** - Chama API externa
- **👤 Atribuir Atendente** - Atribui conversa a atendente

### ✅ Funcionalidades do Editor

1. **Drag and Drop**
   - Arraste componentes da sidebar para o canvas
   - Mova nós arrastando pelo canvas
   - Posicione livremente

2. **Edição de Propriedades**
   - Clique em um nó para editar
   - Painel lateral mostra propriedades
   - Alterações em tempo real

3. **Salvar/Carregar**
   - Salva fluxos no servidor
   - Carrega fluxos salvos
   - Backup automático

4. **Exportar**
   - Exporta para JSON
   - Compatível com sistema atual
   - Pode importar para config.yaml

5. **Preview**
   - Visualiza estrutura do fluxo
   - Valida antes de usar
   - Debug facilitado

## 🎯 Como Usar

### 1. Criar um Fluxo

1. Arraste componentes da sidebar para o canvas
2. Clique em cada nó para editar propriedades
3. Configure mensagens, perguntas, etc.
4. Clique em "💾 Salvar"

### 2. Exemplo: Fluxo de Vendas

```
1. Mensagem: "Olá! Bem-vindo à nossa loja"
2. Pergunta: "Qual produto você tem interesse?"
   - Salvar como: "produto_interesse"
3. Condição: Se produto_interesse = "produto1"
   - Mensagem: "Ótima escolha! Produto 1 custa R$ 99"
4. Pergunta: "Gostaria de fazer o pedido?"
   - Salvar como: "quer_comprar"
5. Mensagem: "Obrigado pelo interesse!"
```

### 3. Salvar e Usar

- **Salvar:** Clique em "💾 Salvar"
- **Carregar:** Clique em "📂 Carregar" e digite o nome
- **Exportar:** Clique em "📤 Exportar" para baixar JSON

## 🔧 Integração com Sistema

### Conversão Automática

Os fluxos criados visualmente podem ser convertidos para o formato YAML do `config.yaml`:

```python
from src.flow_converter import FlowConverter

# Converte fluxo visual para YAML
yaml_flow = FlowConverter.visual_to_yaml(flow_data)

# Salva no config.yaml
FlowConverter.save_to_config("vendas", yaml_flow)
```

### API Endpoints

- `GET /api/flows` - Lista todos os fluxos
- `POST /api/flows` - Salva novo fluxo
- `GET /api/flows/<nome>` - Carrega fluxo específico
- `DELETE /api/flows/<nome>` - Deleta fluxo

## 📁 Estrutura de Dados

### Formato do Fluxo (JSON)

```json
{
  "name": "Fluxo de Vendas",
  "nodes": [
    {
      "id": "node-1",
      "type": "message",
      "x": 100,
      "y": 100,
      "data": {
        "text": "Olá! Bem-vindo!"
      }
    },
    {
      "id": "node-2",
      "type": "question",
      "x": 100,
      "y": 200,
      "data": {
        "question": "Qual produto?",
        "save_as": "produto"
      }
    }
  ],
  "created_at": "2024-01-01T00:00:00"
}
```

## 🎨 Interface

### Layout

- **Sidebar Esquerda:** Componentes disponíveis
- **Canvas Central:** Área de edição (arrasta e solta)
- **Painel Direita:** Propriedades do componente selecionado

### Atalhos

- **Clique:** Seleciona nó
- **Arrastar:** Move nó
- **Clique + Delete:** Remove nó (botão 🗑️)

## 🚀 Próximas Melhorias (Para Comercialização)

1. **Conexões Visuais**
   - Linhas conectando nós
   - Fluxo visual completo
   - Validação de conexões

2. **Mais Componentes**
   - Envio de mídia (imagem, vídeo)
   - Integração com banco de dados
   - Ações avançadas

3. **Templates Prontos**
   - Biblioteca de templates
   - Importar templates
   - Compartilhar fluxos

4. **Colaboração**
   - Múltiplos editores
   - Histórico de versões
   - Comentários

5. **Teste em Tempo Real**
   - Simulador de conversa
   - Debug visual
   - Logs de execução

## ✅ Status Atual

- ✅ Editor visual funcional
- ✅ Drag and drop
- ✅ Salvar/carregar fluxos
- ✅ Exportar JSON
- ✅ Integração com sistema
- ✅ Conversão para YAML
- ⏳ Conexões visuais (próximo)
- ⏳ Templates prontos (próximo)

## 💡 Dicas

1. **Organize os nós:** Posicione de cima para baixo
2. **Use nomes descritivos:** Facilita encontrar depois
3. **Teste antes de salvar:** Use Preview
4. **Exporte backups:** Mantenha cópias dos fluxos importantes

## 🎉 Pronto para Usar!

O construtor está funcional e pronto para uso pessoal. 
Conforme você usar, vamos melhorando e adicionando funcionalidades para comercialização!

**Acesse agora:** http://localhost:5002/flow-builder

