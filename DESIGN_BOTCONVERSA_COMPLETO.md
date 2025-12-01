# 🎨 Design Botconversa - Documento Completo para Replicação

## 📋 Baseado nas Imagens Fornecidas

---

## 1. 🏠 PAINEL DE CONTROLE (Dashboard)

### Layout Geral
- **Sidebar esquerda:** Menu de navegação
- **Área principal:** Cards com estatísticas e gráficos

### Elementos Visuais

#### Cards Principais:
1. **"Estatísticas por período"** (Topo Esquerda)
   - Gráfico de linha com área preenchida (azul)
   - Seletor de período: "24/11/2025" → "01/12/2025"
   - Dropdown: "Novos Contatos"
   - Toggle: Gráfico de linha (ativo) / Gráfico de barras
   - Eixo X: Datas (24 nov 25, 26 nov 25, etc.)
   - Eixo Y: Valores (0 a 4)

2. **"Estatísticas gerais"** (Topo Direita)
   - **Contatos:** "Contatos que interagiram" - **21290**
   - **Interações:** "Mensagem enviada pelo contato" - **21839**
   - **Interações/Inscrito:** **1**

3. **"Eventos personalizados"** (Inferior)
   - Emoji grande (monóculo pensativo)
   - Texto: "Nenhum evento personalizado ainda"
   - Descrição explicativa
   - Botões: "Este mês" (dropdown) + "Criar"

### Cores e Estilo
- Background: Branco (#ffffff)
- Cards: Brancos com sombra sutil
- Gráficos: Azul (#3b82f6) - manter cor Ylada
- Texto: Cinza escuro (#1f2937)

---

## 2. 🎨 CONSTRUTOR DE FLUXOS (Flow Builder)

### Layout
- **Sidebar esquerda:** Menu de navegação
- **Canvas central:** Área de construção de fluxos
- **Dropdown direita:** Componentes disponíveis

### Componentes do Menu Dropdown:
1. **Conteúdo** (Content) - ⭐ ícone estrela
2. **Menu** - 📋 ícone grid
3. **Ação** (Action) - ⚡ ícone raio
4. **Condição** (Condition) - 🔽 ícone triângulo invertido
5. **Conexão de fluxo** (Flow Connection) - 🚀 ícone foguete
6. **Randomizador** (Randomizer) - 🔀 ícone setas cruzadas
7. **Atraso inteligente** (Smart Delay) - ⏰ ícone relógio
8. **Integração** (Integration) - 🔄 ícone swirl
9. **Assistente GPT** (GPT Assistant) - ícone ChatGPT

### Blocos Visuais:

#### Bloco Inicial (Verde Claro)
- Formato: Retângulo arredondado
- Cor: Verde claro (#d1fae5)
- Ícone: 🚀 Foguete
- Texto: "Seu fluxo começa por este bloco. Conecte-o com outro bloco."
- Conector: Linha azul saindo da direita

#### Bloco Conteúdo (Rosa Claro)
- Formato: Retângulo arredondado
- Cor: Rosa claro (#fce7f3)
- Conteúdo interno:
  - Texto da mensagem
  - "Atraso: Digitando X seg."
  - Pergunta: "Qual seu nome por gentileza?"
  - "Salvar: Resposta será salva em: [variável]"
  - Opções: "Ação após resposta válida" / "Se usuário não responder"
  - "Próximo passo"

#### Bloco Ação (Amarelo Claro)
- Formato: Retângulo arredondado
- Cor: Amarelo claro (#fef3c7)
- Ícone: ⚡ Raio
- Conteúdo:
  - "Reiniciar automação"
  - Nome da ação (ex: "PAGTOHDL")
  - "Notificar membro da equipe: [Nome] via WhatsApp: $[TAG]$ [variáveis]"

### Conexões
- **Linhas azuis** conectando blocos
- **Setas** indicando direção do fluxo
- **Múltiplas conexões** possíveis (ramificações)

### Barra Superior do Canvas:
- Título do fluxo: "PAGAMENTO HDL"
- Subtítulo: "Todos os Fluxos"
- Status: "Todas as alterações foram salvas automaticamente"
- Botões verdes:
  - "Visualização" 👁️
  - "Compartilhar fluxo" 📤

### Cores dos Blocos:
- **Inicial:** Verde claro (#d1fae5)
- **Conteúdo:** Rosa claro (#fce7f3)
- **Ação:** Amarelo claro (#fef3c7)
- **Conexões:** Azul (#3b82f6) - manter cor Ylada

---

## 3. 📋 LISTA DE FLUXOS

### Layout
- Título: "Fluxos de conversa"
- Botões verdes: "Criar Pasta +" e "Criar Novo Fluxo +"

### Seção "Fluxos Padrões Básicos":
- 4 botões com bordas tracejadas:
  1. "Fluxo de boas vindas" (borda azul - selecionado)
  2. "Fluxo de resposta padrão"
  3. "Fluxo padrão para mídia"
  4. "Fluxo Pós-Atendimento"

### Seção "Todos os Fluxos":
- Barra de busca: "Busca" 🔍
- Pastas/Categorias (cards):
  - "1-Boas vindas" (8 itens)
  - "3-Indicação" (4 itens)
  - "4-Cupom de descon..." (2 itens)
  - "5-Agendamento" (2 itens)
  - "Atendimento Rotati..." (6 itens)
  - "BlackFriday" (6 itens)
  - "OUTBOUND DIRET..." (1 item)
  - "Pedidos, Orçamento" (4 itens)

### Tabela de Fluxos:
Colunas:
- ☑️ Checkbox
- **Nome** (em negrito)
- **Connections** (ícone de linha ondulada)
- **Execuções**
- **CTR, %**
- **Última alteração** (data)
- ⋮ Menu de opções

Exemplos de linhas:
- PAGAMENTO HDL - 16/10/2025
- AJUDA HLD - 13/10/2025
- SITE HLD - 11/10/2025

---

## 4. 👥 AUDIÊNCIA (Contatos)

### Layout
- Título: "Audiência"
- Botões verdes (topo direita):
  - "Importar Contatos" ⬆️
  - "Baixe Relatório" ⬇️
  - "Criar Contato" 👤
- Barra de busca: "Busca" 🔍

### Coluna Esquerda - Filtros:

#### "Mais popular"
- Subtítulo: "(Use o botão 'Adicionar filtro' para filtrar etiquetas menos populares)"

#### Seção "ETIQUETAS" (TAGS)
- Lista de tags em caixas cinzas arredondadas:
  - HYPEDRINK
  - Leadanuncio
  - Baixoulistamercado
  - WhatsAppsInválidos
  - LEADSALAO
  - VIDEOHYPE
  - etc.

#### Seção "SEQUÊNCIAS"
- "NENHUM ITEM"

#### Seção "CAMPANHAS"
- Lista de campanhas

### Coluna Direita - Tabela de Usuários:

#### Cabeçalho:
- Botão azul "Filtros" 🔽

#### Colunas:
- ☑️ Checkbox
- **Usuários** (com foto/ícone, nome, ID)
- **WhatsApp** (número)
- **Data de inscrição** (data e hora)
- ⋮ Menu de opções

#### Exemplos de linhas:
- n cookies - ID: 840990819 - +5519984400224 - 29/11/2025 08:30
- Geovanne Consultor - ID: 839657317 - +557587092874 - 26/11/2025 17:25
- etc.

---

## 5. 📢 CAMPANHAS

### Layout
- Título: "Campanhas"
- Subtítulo: "Todas as Campanhas 36"
- Botões verdes (topo direita):
  - "Baixe Relatório" ⬇️
  - "Criar Nova Campanha +"
- Barra de busca: "Busca" 🔍

### Tabela de Campanhas:

#### Colunas:
- **Campanha** (nome em negrito + descrição abaixo)
  - Alguns têm ícones: 🍃 (folha verde) ou 🟡 (círculo amarelo)
- **Participantes** (número)
- **Execuções** (número)
- **CTR,%** (porcentagem)
- **Ações:**
  - Botão azul "Mostrar QR"
  - Botão azul "Copiar Link"
  - ⋮ Menu de opções

#### Exemplos de linhas:
- PAGTO HDL, PAGAMENTO HDL - 2 participantes - 0 execuções - 0% CTR
- AJUDA HBL, AJUDA HLD - 2 participantes - 0 execuções - 0% CTR
- AGENDA ANDRE, 01 AGENDA 🍃 - 0 participantes
- etc.

---

## 6. 📡 TRANSMISSÃO (Broadcast)

### Layout
- Título: "Transmissão"
- Tabs (filtros):
  - "Ativas e Agendadas" 📅 (selecionado)
  - "Rascunhos" 📄
  - "Histórico" 🕐
- Botão verde: "Criar Nova Transmissão +"

### Estado Vazio:
- Ícone grande: Bot triste segurando telefone
- Texto: "Não Há Transmissões Agendadas"

### Modal "Criar Transmissão":

#### Seção Esquerda: "Configurações de Transmissão"
1. **Nome:** Campo de texto
2. **Fluxo:** Dropdown "Selecionar"
3. **Atraso:**
   - Radio: "Atraso inteligente" (selecionado) / "Atraso manual"
   - Texto explicativo
   - Radio: "Muito curto 1-5s" (selecionado) / "Curto 5-20s"
4. **Checkbox:** "Definir hora e executar depois"

#### Seção Direita: "Segmentação"
- Texto: "Usuários que receberão esta transmissão: 19479"
- Link: "Mostrar usuários"
- Texto: "Adicionar filtros para refinar seu público"
- Botão tracejado: "Adicionar filtro"

#### Botão Inferior:
- Botão verde grande: "Iniciar agora"

---

## 7. 💬 BATE-PAPO AO VIVO (Live Chat)

### Layout
- **3 colunas:** Lista de chats | Chat ativo | Detalhes do contato

### Coluna Esquerda - Lista de Chats:
- Título: "Live chat"
- Filtros: "Todos" 🔽 e "Ambos" 🔽 + ícone filtro
- Barra de busca: "Busca" 🔍
- Lista de conversas:
  - Foto/ícone circular
  - Nome do contato
  - Timestamp (11:22, 29.11.25, etc.)
  - Preview da mensagem
  - Indicador azul (nova mensagem)
  - Ícone pessoa azul (atribuído)

### Coluna Central - Chat Ativo:
- Header: Nome do contato + foto
- Área de mensagens (com scroll)
- Ícone de download grande (meio da conversa)
- Campo de input: "Digite uma mensagem"
- Ícones: Anexo, Emoji, GIF, Microfone

### Coluna Direita - Detalhes do Contato:
- Header: Nome + ícones (editar, lista, menu)
- ID: "703092255"
- Foto grande circular
- **Status:** "Atendimento está" → "Aberto" (azul) + botão verde "Marcar como Concluído" ✅
- **Informações:**
  - Telefone: +557199547512
  - E-mail: (vazio)
  - Data de inscrição: 24.03.2025 07:56
  - CPF: (vazio)
- **Automação:**
  - Box verde: "Automação está ligada" 🤖
  - Botão: "Pausar automação por" 🔽
- **Atribuição:**
  - Botão azul: "Desvincular-me"
  - Botão azul: "Atribuído a Andre Faula" 🔽
  - Link vermelho: "Remover Atribuição"
- **Etiquetas (Tags):**
  - Seção com botão "+"
  - Tags: "AJUDAHLD X" e "AJUDAHBL X"
- **Sequências:**
  - Seção com botão "+"

---

## 8. ⚙️ AUTOMAÇÃO - PALAVRAS-CHAVE

### Layout
- Título: "Automação"
- Tabs:
  - "Palavras Chave" 🏷️ (selecionado - pill cinza escuro)
  - "Sequências" 🔀
  - "Webhooks" 🔗
- Botão verde: "Adicionar Grupo de Palavras-Chave +"
- Barra de busca: "Busca" 🔍

### Lista de Palavras-Chave:
- Título: "Todas as Palavras-chave 2"

#### Colunas:
- ☑️ Checkbox
- **Título** (com dropdown arrow) + "Untitled" abaixo
- **Mensagem:**
  - Tipo: "Começa com" ou "Contém"
  - Pills roxos com palavras-chave + X para remover + + para adicionar
- **Execuções:** Número (0, 44, etc.)
- **Toggle Switch:** Azul quando ligado
- ⋮ Menu de opções

#### Exemplos:
1. **"Iniciar Fluxo"**
   - Tipo: "Começa com"
   - Palavra: "pronto ja preenchi meus dados"
   - Execuções: 0
   - Toggle: Ligado

2. **"Produtos Herbalife"**
   - Tipo: "Contém"
   - Palavra: "PRODUTO HERBALIFE"
   - Execuções: 44
   - Toggle: Ligado

---

## 9. ⚙️ CONFIGURAÇÕES - CONEXÃO

### Layout
- Título: "Configurações"
- Subtítulo: "Conexão"

### Menu Lateral Esquerdo (Sub-menu):
- **Conexão** (selecionado - verde)
- Campos
- Etiquetas
- Respostas rápidas
- Equipe
- Horários
- Fluxos Padrões
- Companhia
- Registros
- Faturamento
- Integrações

### Card de Status:
- Background: Cinza claro
- **Status:** Círculo verde ✅ + "Automação está ligada" (negrito)
- **Detalhes:** "O número de WhatsApp +5519996049800 está conectado à Ylada Suporte"
  - Número em azul
- **Aviso:** Texto explicativo sobre desconexão após 14 dias
- **Botão vermelho:** "Desconectar"

---

## 10. 🎨 SIDEBAR - MENU PRINCIPAL

### Estrutura:
1. **Logo:** "botconversa" (verde e azul)
2. **Menu Principal:**
   - 🏠 Painel de Controle
   - 👥 Audiência
   - 📢 Campanhas
   - 📡 Transmissão
   - 💬 Bate-papo ao vivo
   - ⚙️ Automação
   - 🔀 Fluxos de conversa
   - ⚙️ Configurações
3. **Separador horizontal**
4. **Modelos** (Templates)
5. **Conta:** "Ylada Suporte" + ID 46470 + seta direita

### Estados:
- Item selecionado: Fundo azul claro (#eff6ff)
- Item hover: Fundo cinza muito claro (#f9fafb)

---

## 🎨 PALETA DE CORES (Adaptar para Ylada BOT)

### Cores Principais (Manter Azul Ylada):
- **Azul Primário:** #3b82f6 (blue-500)
- **Azul Escuro:** #2563eb (blue-600)
- **Azul Claro:** #60a5fa (blue-400)
- **Azul Muito Claro:** #dbeafe (blue-100)

### Cores dos Blocos (Manter):
- **Bloco Inicial:** Verde claro (#d1fae5)
- **Bloco Conteúdo:** Rosa claro (#fce7f3)
- **Bloco Ação:** Amarelo claro (#fef3c7)
- **Conexões:** Azul Ylada (#3b82f6)

### Cores de Status:
- **Sucesso/Ativo:** Verde (#10b981)
- **Atenção:** Amarelo (#f59e0b)
- **Erro:** Vermelho (#ef4444)
- **Info:** Azul Ylada (#3b82f6)

### Cores de Fundo:
- **Background principal:** #f5f7fa
- **Cards:** Branco (#ffffff)
- **Sidebar:** Branco (#ffffff)
- **Hover:** #f9fafb

---

## 📐 ESPAÇAMENTOS E TIPOGRAFIA

### Espaçamentos:
- Padding cards: 20-24px
- Gap entre elementos: 16px
- Border radius: 8-12px
- Sidebar width: 260px

### Tipografia:
- Títulos principais: 24px, bold
- Subtítulos: 18px, semibold
- Texto normal: 14px
- Texto pequeno: 12px
- Font: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

### Fase 1: Layout Base
- [ ] Sidebar idêntica
- [ ] Menu de navegação
- [ ] Header/top bar
- [ ] Cards e containers

### Fase 2: Páginas Principais
- [ ] Dashboard com gráficos
- [ ] Lista de fluxos
- [ ] Construtor visual (melhorar)
- [ ] Página de contatos/audiência
- [ ] Página de campanhas
- [ ] Página de transmissão
- [ ] Live chat
- [ ] Configurações

### Fase 3: Componentes
- [ ] Blocos do construtor (cores corretas)
- [ ] Conexões visuais entre blocos
- [ ] Tabelas com todas as colunas
- [ ] Modais e dropdowns
- [ ] Filtros e busca

### Fase 4: Detalhes
- [ ] Ícones corretos
- [ ] Estados hover/active
- [ ] Animações suaves
- [ ] Responsividade

---

## 🚀 PRÓXIMOS PASSOS

1. **Atualizar sidebar** para ficar idêntica
2. **Melhorar construtor** com cores corretas dos blocos
3. **Criar página de campanhas** completa
4. **Criar página de transmissão**
5. **Implementar live chat** com 3 colunas
6. **Dashboard** com gráficos reais
7. **Página de audiência** com filtros laterais

---

**Documento criado para replicação fiel do design Botconversa mantendo cores azuis do Ylada BOT!** 🎨

