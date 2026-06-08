# Templates de Prompt gpt-image-1 — por Padrão e Tipo de Slide

> Documento vivo — novos templates adicionados conforme experimentos forem consolidados.
> **REGRA ABSOLUTA:** nenhum template pede texto, número ou letra no prompt. Tudo vai no overlay PIL.

---

## Por que os templates antigos estavam errados

O arquivo anterior pedia texto, números e tamanho de fonte no prompt do gpt-image-1. O modelo ignora tudo isso e quando tenta gerar texto, sai ilegível. Estes templates corrigem isso: descrevem **apenas** elementos visuais, atmosfera e composição. Todo texto, número, checklist e destaque é responsabilidade do `add_text_overlay.py`.

---

## Como escolher o template certo

1. Verificar o tipo do slide: hook, dado, consequência, solução ou cta
2. Verificar o padrão visual definido no experiment-log: P1, P2, P3...
3. Usar o template correspondente abaixo
4. Se estiver testando padrão experimental (E1-E4), usar o template experimental

---

## Padrão P1 — Personagem 3D

### P1 · Hook com mascote (Slide 1)

```
Instagram post 1:1 square.
Dark tech illustration, cinematic lighting, premium 3D render quality.
Pitch black background, deep dark atmosphere, NO white background, NO light background, NO bright areas.
Large 3D cartoon robot character centered in lower half of frame, blue and metallic color scheme,
friendly expression, big round eyes, compact body with small antennae.
Robot holding or interacting with [OBJETO: magnifying glass / smartphone / chart / gear].
Behind the robot: subtle circular purple-blue gradient glow on the dark floor.
Upper third of frame: empty dark space for text overlay.
NO text, NO letters, NO numbers, NO words, NO logos.
```

### P1 · Produto / serviço com mascote (Slides 2–4)

```
Instagram post 1:1 square.
Dark tech illustration, clean cinematic composition.
Pitch black background, NO white background, NO light background, deep dark atmosphere.
3D cartoon robot character in lower center, blue and white color scheme, neutral confident expression.
Robot standing next to or pointing toward [ELEMENTO: floating dashboard / checklist panel / data chart].
The element the robot points to is glowing blue neon, abstract, no readable text on it.
Behind robot: very subtle dark blue radial gradient.
Upper half: open dark space for text overlay.
NO text, NO letters, NO numbers, NO words.
```

---

## Padrão P2 — Foto de pessoa com overlay

> P2 **não usa gpt-image-1** para a imagem base. A foto vem de Unsplash ou Pexels. O overlay escuro e o texto são aplicados via PIL com `--overlay-foto`.

**Buscas sugeridas no Unsplash:**

- Hook tech: `businessman looking screen dark office`
- Problema / dado: `stressed entrepreneur laptop night`
- Solução: `team meeting success technology`
- CTA: `confident business person smiling office`

---

## Padrão P3 — Fundo dark para tipografia pura

### P3 · Hook tipográfico (Slide 1)

```
Instagram post 1:1 square.
Minimalist dark tech background, abstract composition.
Pitch black background, NO white background, NO light background, NO bright elements.
Very subtle abstract tech pattern: faint circuit traces or node connections,
opacity 10-15%, barely visible, dark charcoal on black.
No dominant visual element — background texture and atmosphere only.
Slight vignette at edges, darker toward corners.
NO text, NO letters, NO numbers, NO words, NO logos.
```

### P3 · Variação com arcos decorativos nos cantos (Slides 1–2)

```
Instagram post 1:1 square.
Minimalist dark tech background with geometric corner accents.
Pitch black background, NO white background, NO light background.
Subtle curved arc shapes in two opposite corners: top-left and bottom-right.
Arcs are thin lines, blue neon color, partial circles, like decorative frame elements.
Center of frame: completely empty dark space for large text overlay.
Very subtle glow where arcs meet the edges.
NO text, NO letters, NO numbers, NO words.
```

---

## Padrão P5 — Layout comparativo VS

### P5 · Comparativo dois lados (Slide 1 hook ou Slide 2)

```
Instagram post 1:1 square.
Minimalist dark tech illustration, bold contrast composition.
Pitch black background, NO white background, NO light background, deep dark atmosphere.
Two distinct visual zones side by side, divided by a vertical center line with blue neon glow.
Left zone: darker, cooler tone, single faded gray icon or silhouette shape, desaturated.
Right zone: slightly warmer dark tone, single glowing blue icon or shape, vibrant blue neon glow.
Center divider: thin vertical line with neon blue glow, circle element at midpoint.
Top and bottom: empty dark space for text overlay.
NO text, NO letters, NO numbers, NO words, NO VS label.
```

---

## Padrão P6 — Fundo para screenshot embutido

```
Instagram post 1:1 square.
Dark tech layout background, professional composition.
Pitch black background, NO white background, NO light background.
Right side: vertical rounded rectangle placeholder area, dark navy fill, subtle border glow blue,
positioned in right 40% of frame, leaving left 60% empty for text overlay.
The rectangle has subtle inner shadow and depth suggesting a screen or card.
NO text, NO letters, NO interface elements, NO app content, NO words.
```

---

## Templates Experimentais

> Usar apenas com registro no `experiment-log.json`. Não consolidar sem aprovação do Robson.

### E1 · Card arredondado sobre fundo dark

```
Instagram post 1:1 square.
Minimalist dark tech background with card composition.
Pitch black background, NO white background, NO light background.
Center: rounded rectangle card, slightly lighter dark fill (dark navy, not white), thin neon blue border,
subtle inner glow at the border edge. Card occupies center 70% of frame.
Outside the card in corners: subtle curved arc shapes, very faint blue or purple lines.
Inside the card: completely empty for text overlay.
NO text, NO letters, NO numbers, NO words.
```

### E2 · Fundo com textura de grid sutil

```
Instagram post 1:1 square.
Minimalist dark tech background, grid texture.
Pitch black background, NO white background, NO light background.
Very subtle grid pattern across entire frame: thin lines forming squares,
charcoal dark color barely visible against black, 10% opacity maximum.
No dominant elements. Pure texture background. Slight vignette at edges.
NO text, NO letters, NO numbers, NO words, NO shapes.
```

### E3 · Split background gradiente lateral

```
Instagram post 1:1 square.
Dark tech split composition background.
Left half: pitch black, NO light, solid dark atmosphere.
Right half: very dark teal or very dark navy, subtle gradient from center to right edge.
Thin vertical divider line between halves, faint blue neon glow, 1-2px wide.
Both halves completely empty for text and visual overlays.
NO text, NO letters, NO numbers, NO words, NO dominant shapes.
```

### E4 · Número com unidade em destaque

> Usar base **P3** (fundo tipográfico dark). No overlay usar:
> `--tipo dado-unidade --numero "73" --unidade "%"`
> O script renderiza o número em 120px e a unidade em 48px alinhada ao topo do número.

---

## Regras de montagem de prompt

1. Sempre começar com: `Instagram post 1:1 square.`
2. Sempre declarar atmosfera e estilo logo depois
3. Sempre incluir negativas de fundo claro **pelo menos 2 vezes**
4. Nunca incluir pedido de texto, número, letra, logo ou fonte
5. Descrever composição em termos de zonas e posições relativas — não coordenadas
6. Manter entre **100 e 300 palavras** — acima disso o modelo ignora partes
7. Terminar sempre com `NO text, NO letters, NO numbers, NO words.`

---

## Checklist antes de enviar o prompt

- [ ] Removi **todo** pedido de texto, letra, número ou tamanho de fonte
- [ ] Troquei hex por descrição de cor em inglês
- [ ] Incluí negativa de fundo claro pelo menos 2 vezes
- [ ] Descrevi elementos com posição relativa (center, left, upper third)
- [ ] Deixei espaço vazio explícito onde vai o overlay de texto
- [ ] Prompt está entre 100 e 300 palavras
- [ ] Terminei com `NO text, NO letters, NO numbers, NO words`
