#!/usr/bin/env python3
"""
Script de Overlay de Texto — ERA4 Designer
Adiciona texto legível sobre imagem base gerada pelo gpt-image-1.
Usa PIL (Pillow). Fonte: Helvetica Bold ou Inter Bold.

Uso:
  python3 add_text_overlay.py \
    --input slide_1_base.png \
    --output slide_1.png \
    --texto "SUA IA ATENDE MAIS RÁPIDO?" \
    --subtitulo "O lead espera 5 minutos" \
    --tipo hook

  python3 add_text_overlay.py \
    --input slide_2_base.png \
    --output slide_2.png \
    --texto "40" \
    --subtitulo "% das vendas perdidas" \
    --tipo dado

  python3 add_text_overlay.py \
    --input slide_3_base.png \
    --output slide_3.png \
    --texto "RESPOSTA LENTA\\nLEAD PERDIDO\\nVENDA FECHADA PELO CONCORRENTE" \
    --tipo lista

  python3 add_text_overlay.py \
    --input slide_4_base.png \
    --output slide_4.png \
    --texto "RESPONDE EM SEGUNDOS\\nQUALIFICA SEM HUMANO\\nAGENDA AUTOMATICAMENTE" \
    --tipo checklist

  python3 add_text_overlay.py \
    --input slide_5_base.png \
    --output slide_5.png \
    --texto "FALA COM A ERA4" \
    --subtitulo "era4.com.br/contato" \
    --tipo cta

  python3 add_text_overlay.py \
    --input slide_1_base.png \
    --output slide_1.png \
    --texto "TEXTO PRINCIPAL" \
    --overlay-foto
"""

import argparse
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("ERRO: Pillow não instalado. Rodar: pip3 install Pillow")
    sys.exit(1)

# ── Configurações de fonte ──────────────────────────────────────────
FONT_PATHS_BOLD = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/SFNS.ttf",
    "/System/Library/Fonts/SFNSRounded.ttf",
    "/System/Library/Fonts/SFCompact.ttf",
]

FONT_PATHS_REGULAR = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/SFNS.ttf",
    "/System/Library/Fonts/SFNSRounded.ttf",
    "/System/Library/Fonts/SFCompact.ttf",
]


def find_font(paths, size, style="regular"):
    for i, p in enumerate(paths):
        if os.path.exists(p):
            try:
                # Helvetica.ttc e HelveticaNeue.ttc são coleções — usar índice para bold/regular
                if p.endswith(".ttc"):
                    idx = 0
                    if style == "bold" and i == 0:
                        idx = 0  # Helvetica.ttc primeiro item muitas vezes é bold/regular
                    return ImageFont.truetype(p, size, index=idx)
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


# ── Paleta ERA4 ────────────────────────────────────────────────────
COLORS = {
    "bg_dark": (10, 10, 15),
    "white": (248, 250, 252),
    "gray": (148, 163, 184),
    "blue": (59, 130, 246),
    "purple": (139, 92, 246),
    "green": (34, 197, 94),
    "orange": (245, 158, 11),
    "red": (239, 68, 68),
    "laranja": (245, 158, 11),
    "verde": (34, 197, 94),
    "azul": (59, 130, 246),
    "roxo": (139, 92, 246),
    "vermelho": (239, 68, 68),
    "cinza": (148, 163, 184),
    "branco": (248, 250, 252),
    "lime": (132, 204, 22),
    "verde_lime": (132, 204, 22),
    "verde-limao": (132, 204, 22),
}


def resolve_color(name):
    """Resolve nome de cor (pt/en) para RGB."""
    if not name:
        return COLORS["white"]
    name_lower = name.lower().strip()
    # direto
    if name_lower in COLORS:
        return COLORS[name_lower]
    # hex
    if name_lower.startswith("#") and len(name_lower) == 7:
        try:
            return tuple(int(name_lower[i:i+2], 16) for i in (1, 3, 5))
        except ValueError:
            pass
    return COLORS["white"]


# ── Configurações por tipo de slide ────────────────────────────────
SLIDE_CONFIGS = {
    "hook": {
        "text_size": 64,
        "text_y": 0.18,
        "text_color": "white",
        "sub_size": 32,
        "sub_y": 0.78,
        "sub_color": "blue",
        "glow": True,
    },
    "dado": {
        "text_size": 120,
        "text_y": 0.35,
        "text_color": "blue",
        "sub_size": 32,
        "sub_y": 0.65,
        "sub_color": "gray",
        "glow": True,
    },
    "problema": {
        "text_size": 52,
        "text_y": 0.20,
        "text_color": "white",
        "sub_size": 28,
        "sub_y": 0.75,
        "sub_color": "gray",
        "glow": False,
    },
    "consequencia": {
        "text_size": 52,
        "text_y": 0.20,
        "text_color": "white",
        "sub_size": 28,
        "sub_y": 0.75,
        "sub_color": "orange",
        "glow": False,
    },
    "lista": {
        "text_size": 36,
        "text_y": 0.15,
        "text_color": "white",
        "sub_size": 28,
        "sub_y": 0.85,
        "sub_color": "gray",
        "glow": False,
        "line_spacing": 60,
    },
    "checklist": {
        "text_size": 34,
        "text_y": 0.12,
        "text_color": "white",
        "sub_size": 28,
        "sub_y": 0.88,
        "sub_color": "green",
        "glow": False,
        "line_spacing": 56,
        "check_prefix": True,
    },
    "solucao": {
        "text_size": 48,
        "text_y": 0.15,
        "text_color": "green",
        "sub_size": 28,
        "sub_y": 0.80,
        "sub_color": "white",
        "glow": False,
    },
    "cta": {
        "text_size": 58,
        "text_y": 0.30,
        "text_color": "white",
        "sub_size": 28,
        "sub_y": 0.70,
        "sub_color": "gray",
        "glow": True,
    },
    "default": {
        "text_size": 52,
        "text_y": 0.20,
        "text_color": "white",
        "sub_size": 28,
        "sub_y": 0.75,
        "sub_color": "gray",
        "glow": False,
    },
    "foto": {
        "text_size": 52,
        "text_y": 0.25,
        "text_color": "white",
        "sub_size": 28,
        "sub_y": 0.75,
        "sub_color": "gray",
        "glow": False,
        "overlay_foto": True,
    },
}


def wrap_text(text, font, max_width, draw):
    """Quebra texto em linhas que cabem em max_width."""
    # Se o texto já vem com \n, respeitar quebras explícitas
    explicit_lines = text.split("\\n")
    all_lines = []
    for eline in explicit_lines:
        words = eline.strip().split()
        if not words:
            continue
        current = ""
        for word in words:
            test = f"{current} {word}".strip()
            bbox = draw.textbbox((0, 0), test, font=font)
            w = bbox[2] - bbox[0]
            if w <= max_width:
                current = test
            else:
                if current:
                    all_lines.append(current)
                current = word
        if current:
            all_lines.append(current)
    return all_lines if all_lines else [text]


def add_glow(draw, position, text, font, glow_color, radius=4):
    """Adiciona glow ao texto."""
    x, y = position
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx == 0 and dy == 0:
                continue
            alpha_factor = 1.0 / max(abs(dx), abs(dy))
            glow_layer = tuple(
                min(255, int(c * alpha_factor * 0.3))
                for c in glow_color[:3]
            )
            draw.text((x + dx, y + dy), text, font=font, fill=glow_layer)


def draw_centered_text(draw, img_width, y_ratio, text, font, color_name, glow=False):
    """Desenha texto horizontalmente centralizado."""
    if not text:
        return
    max_width = img_width * 0.85
    lines = wrap_text(text, font, max_width, draw)
    color = resolve_color(color_name)
    line_height = font.size + 10
    total_height = len(lines) * line_height
    start_y = int(img_width * y_ratio) - total_height // 2
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (img_width - tw) // 2
        y = start_y + i * line_height
        if glow:
            add_glow(draw, (x, y), line, font, color)
        draw.text((x, y), line, font=font, fill=color)


def draw_list(draw, img_w, img_h, y_ratio, text, font, color_name,
              line_spacing=56, check_prefix=False, sub_text=""):
    """Desenha lista (com ou sem checkmark)."""
    if not text:
        return
    max_width = img_w * 0.80
    lines = wrap_text(text, font, max_width, draw)
    color = resolve_color(color_name)
    total_height = len(lines) * line_spacing
    start_y = int(img_h * y_ratio)

    for i, line in enumerate(lines):
        y = start_y + i * line_spacing
        # Checkmark verde
        if check_prefix:
            check_x = int(img_w * 0.10)
            draw.text((check_x, y), "✓", font=font, fill=COLORS["green"])
            text_x = int(img_w * 0.16)
        else:
            # Bullet laranja
            bullet_x = int(img_w * 0.10)
            draw.text((bullet_x, y), "•", font=font, fill=COLORS["orange"])
            text_x = int(img_w * 0.16)
        draw.text((text_x, y), line, font=font, fill=color)

    # Subtexto abaixo da lista
    if sub_text:
        sub_font = find_font(FONT_PATHS_REGULAR, 24)
        sub_y = start_y + len(lines) * line_spacing + 20
        bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
        tw = bbox[2] - bbox[0]
        x = (img_w - tw) // 2
        draw.text((x, sub_y), sub_text, font=sub_font, fill=COLORS["gray"])


def apply_foto_overlay(img):
    """Aplica escurecimento assimétrico: lado esquerdo mais escuro (60%),
    lado direito mais claro (30%). Gradiente horizontal suave.
    Ideal para layout P7: texto à esquerda, foto visível à direita.
    """
    w, h = img.size
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for x in range(w):
        # Gradiente: esquerda opaca (alpha 153 = 60%) -> direita translúcida (alpha 77 = 30%)
        alpha = int(153 - (x / w) * 76)
        draw.line([(x, 0), (x, h)], fill=(10, 10, 15, alpha))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def main():
    parser = argparse.ArgumentParser(description="Overlay de texto ERA4")
    parser.add_argument("--input", required=True, help="Imagem base (sem texto)")
    parser.add_argument("--output", required=True, help="Imagem final (com texto)")
    parser.add_argument("--texto", required=True, help="Texto principal (use \\n para quebras)")
    parser.add_argument("--subtitulo", default="", help="Subtítulo ou apoio")
    parser.add_argument("--tipo", default="default",
                        choices=["hook", "dado", "problema", "consequencia",
                                 "lista", "checklist", "solucao", "cta", "foto", "default"],
                        help="Tipo do slide")
    parser.add_argument("--highlight", default="", help="Palavra para highlight")
    parser.add_argument("--highlight-cor", default="blue", help="Cor do highlight")
    parser.add_argument("--overlay-foto", action="store_true",
                        help="Aplica escurecimento 50% (para foto de fundo)")
    args = parser.parse_args()

    # ── Validar input ────────────────────────────────────────────────
    input_path = os.path.expanduser(args.input)
    output_path = os.path.expanduser(args.output)

    if not os.path.isfile(input_path):
        print(f"ERRO: arquivo não encontrado: {input_path}")
        sys.exit(1)

    # ── Abrir imagem ─────────────────────────────────────────────────
    try:
        img = Image.open(input_path).convert("RGBA")
    except Exception as e:
        print(f"ERRO ao abrir imagem: {e}")
        sys.exit(1)

    img_w, img_h = img.size

    # ── Overlay escuro base (legibilidade) ───────────────────────────
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)

    # Gradiente escuro topo e bottom
    for y in range(0, int(img_h * 0.25)):
        alpha = int(180 * (1 - y / (img_h * 0.25)))
        draw_overlay.line([(0, y), (img_w, y)], fill=(10, 10, 15, alpha))
    for y in range(int(img_h * 0.75), img_h):
        alpha = int(180 * ((y - img_h * 0.75) / (img_h * 0.25)))
        draw_overlay.line([(0, y), (img_w, y)], fill=(10, 10, 15, alpha))

    img = Image.alpha_composite(img, overlay)

    # ── Overlay foto (se pedido ou tipo=foto) ──────────────────────────
    if args.overlay_foto or args.tipo == "foto":
        img = apply_foto_overlay(img)

    draw = ImageDraw.Draw(img)

    # ── Configuração do tipo ─────────────────────────────────────────
    cfg = SLIDE_CONFIGS.get(args.tipo, SLIDE_CONFIGS["default"])

    # ── Fontes ───────────────────────────────────────────────────────
    font_main = find_font(FONT_PATHS_BOLD, cfg["text_size"], style="bold")
    font_sub = find_font(FONT_PATHS_REGULAR, cfg["sub_size"], style="regular")

    # ── Desenhar conforme o tipo ─────────────────────────────────────
    if args.tipo in ("lista", "checklist"):
        draw_list(
            draw, img_w, img_h, cfg["text_y"],
            args.texto, font_main,
            cfg["text_color"],
            line_spacing=cfg.get("line_spacing", 56),
            check_prefix=(args.tipo == "checklist"),
            sub_text=args.subtitulo,
        )
    else:
        # Texto centralizado (hook, dado, problema, consequência, solução, cta)
        draw_centered_text(
            draw, img_w, cfg["text_y"],
            args.texto, font_main,
            cfg["text_color"], glow=cfg["glow"]
        )

        # Subtítulo
        if args.subtitulo:
            draw_centered_text(
                draw, img_w, cfg["sub_y"],
                args.subtitulo, font_sub,
                cfg["sub_color"], glow=False
            )

    # ── Highlight (se especificado) ──────────────────────────────────
    if args.highlight and args.tipo not in ("lista", "checklist"):
        highlight_font = find_font(FONT_PATHS_BOLD, cfg["text_size"] + 8)
        highlight_color = resolve_color(args.highlight_cor)
        bbox = draw.textbbox((0, 0), args.highlight, font=highlight_font)
        tw = bbox[2] - bbox[0]
        x = (img_w - tw) // 2
        y = int(img_h * cfg["text_y"]) - (bbox[3] - bbox[1]) // 2
        add_glow(draw, (x, y), args.highlight, highlight_font, highlight_color, radius=6)
        draw.text((x, y), args.highlight, font=highlight_font, fill=highlight_color)

    # ── Salvar ───────────────────────────────────────────────────────
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    final = img.convert("RGB")
    final.save(output_path, "PNG", quality=95)
    print(f"OK: {output_path}")


if __name__ == "__main__":
    main()
