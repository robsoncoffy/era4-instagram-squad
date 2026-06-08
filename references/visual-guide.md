# 🎨 Guia Visual ERA4 — Designer (Pixel)

Baseado em referências reais: era4.ia, @obrunookamoto, @pixeleducacao
Documento vivo — atualizado semanalmente pelo Pixel com novos padrões pesquisados

---

## Identidade Visual ERA4

| Elemento | Valor | Uso |
|----------|-------|-----|
| **Fundo principal** | `#0a0a0f` (preto profundo) | Fundo padrão, peças de marca forte |
| **Fundo alternativo** | `#0f172a` (dark navy) | Gradiente secundário |
| **Fundo teal/verde-azul** | `#0d3d4a` | Carrosséis estilo tech ERA4 legacy |
| **Texto principal** | `#f8fafc` (branco) | Headlines, títulos |
| **Texto secundário** | `#94a3b8` (cinza claro) | Subtexto, descrições |
| **Azul neon / ciano** | `#3b82f6` ou `#00c8ff` | Dados, destaque de palavras-chave, highlight boxes |
| **Roxo** | `#8b5cf6` | Gradientes, detalhes |
| **Verde** | `#22c55e` | Checkmarks, positivo |
| **Laranja/dourado** | `#f59e0b` | Alerta, palavras em destaque, estrelas |
| **Vermelho** | `#ef4444` | Erro, X, negativo |
| **Branco puro** | `#ffffff` | Texto sobre foto/imagem com overlay escuro |

---

## Tipografia (overlay PIL)

| Nível | Tamanho | Peso | Uso |
|-------|---------|------|-----|
| Hook headline | 64-80px | Bold/ExtraBold | Frase principal do slide 1 |
| Dado/número | 96-120px | ExtraBold | Números de impacto isolados |
| Título de slide | 48-60px | Bold | Títulos dos slides 2-4 |
| Subtexto | 28-36px | Regular | Apoio, descrição, contexto |
| Destaque inline | 48-60px | ExtraBold | Palavra-chave colorida dentro do título |
| CTA | 40-52px | Bold | Slide final |
| Rodapé/link | 20-24px | Regular | era4.com.br/contato |

**Fonte preferida:** Inter ExtraBold / Bold, Helvetica Neue, ou sans-serif bold disponível.
**Caixa alta:** ERA4 usa ALL CAPS em frases curtas de slide.
**Italic:** não usar. Nunca.

---

## Padrões consolidados (testados e aprovados)

### P1 — Personagem 3D centralizado
**Status:** ✅ consolidado
**Quando usar:** hook com mascote, slide de produto, apresentação de serviço

Robô 3D estilizado centralizado na metade inferior do slide.
Fundo dark ou gradient azul profundo.
Logo e título no terço superior.
Personagem ocupa 50-60% da altura do slide.

Referência: "O PIXEL — espião do bem" e "INTELIGÊNCIA ARTIFICIAL NO SEU NEGÓCIO" (era4.ia).

Prompt base gpt-image-1:
"3D cartoon robot character, blue and white color scheme, friendly expression, holding [OBJETO], centered in lower half of frame, dark navy background, subtle purple circle glow behind character, NO text, NO letters, NO words."

---

### P2 — Foto de pessoa com overlay escuro + highlight box
**Status:** ✅ consolidado
**Quando usar:** slides de problema, consequência, solução com prova real

Foto de empresário em ambiente de trabalho.
Overlay preto semitransparente 40-60% de opacidade.
Texto branco bold no terço inferior.
1-2 palavras-chave com highlight box colorida.
Logo ERA4 no canto superior direito.

Referência: "TODOS OS CLIENTES NO MESMO LUGAR" e "CRM AUTOMATIZADO" (era4.ia).

Regra: fotos vêm de Unsplash ou Pexels. Nunca pedir foto de pessoa ao gpt-image-1.
Overlay: mínimo 40%, máximo 65% de opacidade.

---

### P3 — Tipografia pura / alta tipografia
**Status:** ✅ consolidado
**Quando usar:** slides de impacto com frase curta, carrosséis de diagnóstico, posts rápidos

Fundo dark sólido.
Headline dominante em caixa alta, 3-4 palavras por linha.
1-2 palavras em cor de destaque (azul ciano ou laranja dourado).
Sem elemento visual além da tipografia.

Variação: curvas/arcos decorativos nos cantos do slide para dar energia (estilo Pixel Educação, adaptado para dark).

---

### P4 — Highlight box (técnica de overlay)
**Status:** ✅ consolidado — aplicar em qualquer padrão
**Quando usar:** destacar palavra-chave ou frase CTA em qualquer slide

Variações:
- Fundo azul `#3b82f6` + texto branco → palavra-chave no meio da headline
- Fundo laranja `#f59e0b` + texto preto → urgência ou número
- Fundo roxo `#8b5cf6` + texto branco → CTA secundário
- Fundo verde `#22c55e` + texto preto → benefício, checkmark inline

Implementação PIL: retângulo colorido com padding 8px H / 4px V → texto por cima.

---

### P5 — Layout comparativo VS
**Status:** ✅ consolidado
**Quando usar:** hook de contraste, diagnóstico, problema vs solução

Duas colunas com separador central.
Cada lado com ícone + texto descritivo.
Separador: círculo "VS" em vermelho/laranja com borda neon.

Referência: "EMPRESA TRADICIONAL vs EMPRESA AI FIRST" (@obrunookamoto).

---

### P6 — Screenshot / prova social embutida
**Status:** ✅ consolidado
**Quando usar:** slides de resultado, prova de plataforma, demonstração de produto

Screenshot de interface ou app integrado ao slide.
Fundo dark dominante.
Screenshot à direita ou centralizado, texto à esquerda ou abaixo.

Referência: "Google Meu Negócio" com screenshot do app (era4.ia).

---

## Padrões em teste (usar com registro no experiment-log)

### E1 — Card com cantos arredondados sobre fundo dark
**Status:** 🧪 em teste
**Inspiração:** Pixel Educação (fundo claro) adaptado para dark
**Hipótese:** card cria hierarquia visual clara e separa conteúdo do fundo

Card com cantos arredondados, fundo `#1a1a2e` sobre `#0a0a0f`.
Borda fina neon (azul ou roxo) no card.
Curvas decorativas nos cantos do slide, fora do card.

---

### E2 — Fundo com textura de grid sutil
**Status:** 🧪 em teste
**Inspiração:** posts tech do LinkedIn adaptados para Instagram
**Hipótese:** grid dá profundidade sem poluir, reforça identidade tech

Grid de linhas finas `#1e293b` sobre `#0a0a0f` aplicado via PIL.
Espaçamento: 48px entre linhas H e V.
Opacidade: 15-25%.

---

### E3 — Gradiente de cor lateral (split background)
**Status:** 🧪 em teste
**Inspiração:** posts tech internacionais de automação
**Hipótese:** split cria tensão visual que mantém o olho no slide

Metade esquerda: `#0a0a0f`. Metade direita: `#0d3d4a` ou `#1a0a2e`.
Separação com linha neon fina vertical.
Texto à esquerda, elemento visual à direita.

---

### E4 — Número em destaque com unidade em tamanho menor
**Status:** 🧪 em teste
**Inspiração:** infográficos de dados do @obrunookamoto
**Hipótese:** contraste de tamanho entre número e unidade aumenta impacto do dado

Número principal: 120px ExtraBold, azul neon.
Unidade (%, R$, h): 48px Bold, cinza claro, alinhada ao topo do número.
Subtexto abaixo: 28px Regular, cinza claro.

---

## Como o Pixel atualiza este guia

Todo segunda-feira o Pixel executa o fluxo de pesquisa semanal:

1. Vasculha era4.ia, @obrunookamoto, @pixeleducacao + indicações do briefing.
2. Identifica padrões novos não registrados neste guia.
3. Adiciona em "Padrões em teste" com status 🧪, hipótese e inspiração.
4. Após 3 usos com aprovação do Robson → move para "Padrões consolidados" ✅.
5. Após 3 usos com reprovação → remove e registra o motivo no experiment-log.

**Regra:** se passou 2 semanas sem atualização, o Pixel falhou na missão de pesquisa.

---

## Layout por tipo de slide

### Hook (Slide 1) — objetivo: parar o scroll em 0,3s
Escolher entre P1, P2 ou P3. Verificar no experiment-log e variar.

### Problema / Dado (Slide 2)
Padrão: número gigante centralizado, azul neon ou laranja. Testar: E4.

### Consequência (Slide 3)
Padrão: lista vertical com ícones X ou alerta, laranja/vermelho. Testar: E2.

### Solução (Slide 4)
Padrão: checklist verde, headline no topo, layout limpo. Testar: E1.

### CTA (Slide 5)
Padrão: gradiente azul-roxo, botão com borda neon, link rodapé. Testar: E3.

### Estático
Headline dominante (máx 2 linhas), elemento de suporte, CTA no rodapé.

### Stories (9:16)
Composição vertical, blocos grandes, texto maior, curvas nos cantos, CTA no frame final.

---

## Elementos de marca ERA4 no overlay

- Logo ERA4 (branco) — canto superior direito ou topo centralizado
- era4.com.br/contato — rodapé discreto em cinza claro
- Numeração de slide (ex: 1/5) — canto superior direito, em cinza, quando carrossel

---

## Gradientes

- Fundo padrão: `linear-gradient(180deg, #0a0a0f 0%, #0f172a 100%)`
- CTA: `linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%)`
- Solução: `linear-gradient(180deg, #0f172a 0%, #0a1f0a 100%)`
- Alerta: `linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)`
- Tech legacy ERA4: `linear-gradient(180deg, #0d3d4a 0%, #0a0a0f 100%)`

---

## Regras absolutas

- Fundo claro é falha de missão, exceto aprovação explícita do Robson.
- Nunca incluir texto no prompt do gpt-image-1.
- Nunca pedir foto de pessoa ao gpt-image-1.
- Nunca usar mais de 3 cores de destaque no mesmo slide.
- Nunca usar fonte serif.
- Overlay sobre foto: entre 40% e 65% de opacidade.
- Highlight box: padding mínimo 8px H e 4px V.
- Nunca deixar este guia parado por mais de 2 semanas sem atualização.
