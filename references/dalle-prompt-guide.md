# 🎨 Guia de Prompt DALL-E 3 — Designer ERA4

## O que o DALL-E 3 RESPEITA

| Técnica | Exemplo | Resultado |
|---------|---------|-----------|
| **Estilo explícito** | "minimalist tech illustration" | Respeita |
| **Mood/ambiente** | "dark moody atmosphere" | Respeita |
| **Elementos grandes** | "glowing blue robot in center" | Respeita bem |
| **Posição geral** | "centered composition" | Respeita parcialmente |
| **Metáfora visual** | "neon sign in dark alley" | Respeita bem |
| **Proporção/formato** | "Instagram post 1:1" | Respeita (quando especificado no parâmetro) |
| **Negativas fortes** | "NO text, NO letters, NO words" | Ajuda a evitar texto |

## O que o DALL-E 3 IGNAORA

| Pedido | Por que ignora | Alternativa |
|--------|---------------|-------------|
| **Cores hex exatas** (#0a0a0f) | Não entende hex | Usar descrição: "deep black with blue neon accents" |
| **Tamanhos de fonte** (48px) | Não entende pixels | Pedir "large bold text" ou "small caption" |
| **Texto legível** (qualquer texto) | Texto sai ilegível/distorcido | **NUNCA pedir texto na imagem** — usar overlay depois |
| **Posições exatas** (x, y) | Não entende coordenadas | Pedir "top third", "center", "bottom left" |
| **Gradientes específicos** | Ignora hex do gradiente | Descrever efeito: "gradient from dark blue to purple" |
| **Fontes específicas** (Helvetica) | Não entende nomes de fonte | Pedir "bold sans-serif", "modern typeface" |

## Truques Pra Forcar Fundo Dark

O DALL-E tem viés pra imagens claras. Pra forçar dark:

```
"Dark background, deep black (#0a0a0f), NO light background, 
NO white background, NO bright colors, neon accents only, 
moody lighting, cinematic dark atmosphere"
```

## Template de Prompt Eficiente

```
[FORMATO] [PROPORÇÃO]
[ESTILO VISUAL]
[FUNDO — com truque de negativa]
[ELEMENTOS PRINCIPAIS — grandes e claramente descritos]
[CORES — por nome, não hex]
[COMPOSIÇÃO — posição geral]
[NÃO incluir: NO text, NO letters, NO words, NO numbers]
```

## Exemplo Bom vs Ruim

### ❌ Ruim (ignorado)
```
Create an Instagram post with dark background #0a0a0f.
Text: "SUA IA ATENDE MAIS RÁPIDO" in 60px bold white.
Blue neon glow #3b82f6.
```

### ✅ Bom (respeitado)
```
Minimalist tech illustration, Instagram post 1:1.
Deep black background, NO light background, NO white.
Moody dark atmosphere with blue neon glow accents.
Large glowing blue robot icon in center, 
construction/maintenance theme.
Bold modern composition, cinematic lighting.
NO text, NO letters, NO words.
```

## Checklist Antes de Enviar Prompt

- [ ] Removi TODO pedido de texto/letra/número
- [ ] Troquei cores hex por descrição ("blue neon" vs "#3b82f6")
- [ ] Adicionei negativas ("NO text", "NO white background")
- [ ] Descrevi elementos grandes e claros (não detalhes pequenos)
- [ ] Especifiquei mood/atmosphere
- [ ] Confirmei que não pedi nada impossível

## Workflow Recomendado

1. **Gerar imagemBase** — prompt SEM texto, só visual
2. **Salvar** em `~/era4-instagram-squad/assets/slide_N_base.png`
3. **Adicionar texto via overlay** — script `add_text_overlay.py`
4. **Salvar final** como `slide_N.png`
5. **Upload no Zernio**

Este workflow separa o que o DALL-E faz bem (visual) do que ele faz mal (texto).
