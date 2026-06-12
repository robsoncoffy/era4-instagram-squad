#!/usr/bin/env python3
"""
Script de geração de slides — ERA4 Designer
Pipeline NOTÍCIA 2026-06-12: Meta IA no WhatsApp
Carrossel 5 slides: P11 slide 1 (foto), P3 fundo dark slides 2-4, CTA slide 5
"""

import os, sys, json, base64, requests, time
from PIL import Image, ImageDraw, ImageFont

WORKSPACE = os.path.expanduser("~/era4-instagram-squad")
ASSETS_DIR = os.path.join(WORKSPACE, "assets")

def read_env_key(key_name):
    env_path = os.path.join(WORKSPACE, ".env")
    with open(env_path) as f:
        for line in f:
            if key_name in line and "=" in line:
                val = line.strip().split("=", 1)[1]
                # Remove comments
                if " #" in val:
                    val = val.split(" #")[0].strip()
                return val.strip().strip('"').strip("'")
    return None

def generate_image(prompt, api_key, retries=3):
    """Gera imagem via gpt-image-1 e retorna bytes."""
    for attempt in range(retries):
        try:
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                json={"model": "gpt-image-1", "prompt": prompt, "n": 1, "size": "1024x1024"},
                timeout=120
            )
            if response.status_code == 200:
                data = response.json()
                if "data" in data and len(data["data"]) > 0:
                    b64 = data["data"][0].get("b64_json")
                    if b64:
                        return base64.b64decode(b64)
            print(f"  Tentativa {attempt+1} falhou: status={response.status_code}")
            if response.status_code == 429:
                wait = 30 * (attempt + 1)
                print(f"Rate limit. Aguardando {wait}s...")
                time.sleep(wait)
        except Exception as e:
            print(f"  Tentativa {attempt+1} erro: {e}")
            time.sleep(5)
    return None

def download_unsplash_photo(query, output_path):
    """Baia foto do Unsplash Source (sem API key)."""
    url = f"https://source.unsplash.com/1024x1024/?{query.replace(' ', ',')}"
    try:
        r = requests.get(url, timeout=30, allow_redirects=True)
        if r.status_code == 200 and len(r.content) > 10000:
            with open(output_path, "wb") as f:
                f.write(r.content)
            return True
    except Exception as e:
        print(f"  Unsplash download falhou: {e}")
    return False

def download_pexels_photo(query, api_key, output_path):
    """Baia foto do Pexels."""
    try:
        r = requests.get(
            f"https://api.pexels.com/v1/search?query={query}&per_page=1&orientation=square",
            headers={"Authorization": api_key},
            timeout=30
        )
        if r.status_code == 200:
            data = r.json()
            if data.get("photos"):
                img_url = data["photos"][0]["src"]["large"]
                img_r = requests.get(img_url, timeout=30)
                if img_r.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(img_r.content)
                    return True
    except Exception as e:
        print(f"  Pexels download falhou: {e}")
    return False

# ── Font paths (macOS) ──────────────────────────────────────────────
FONT_PATHS_BOLD = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/SFNS.ttf",
]
FONT_PATHS_REGULAR = FONT_PATHS_BOLD

def find_font(paths, size, style="regular"):
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                continue
    return ImageFont.load_default()

# ── Colors ──────────────────────────────────────────────────────────
COLORS = {
    "bg_dark": (10, 10, 15), "white": (248, 250, 252), "gray": (148, 163, 184),
    "blue": (59, 130, 246), "purple": (139, 92, 246), "green": (34, 197, 94),
    "orange": (245, 158, 11), "red": (239, 68, 68), "rosa": (236, 72, 153),
    "pink": (236, 72, 153),
}

def apply_dark_gradient(img):
    """Apply top/bottom dark gradient for text readability."""
    w, h = img.size
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(0, int(h * 0.30)):
        alpha = int(200 * (1 - y / (h * 0.30)))
        draw.line([(0, y), (w, y)], fill=(10, 10, 15, alpha))
    for y in range(int(h * 0.70), h):
        alpha = int(200 * ((y - h * 0.70) / (h * 0.30)))
        draw.line([(0, y), (w, y)], fill=(10, 10, 15, alpha))
    return Image.alpha_composite(img.convert("RGBA"), overlay)

def apply_foto_overlay_gradient(img):
    """Apply asymmetric gradient: left side darker, right side lighter."""
    w, h = img.size
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for x in range(w):
        alpha = int(160 - (x / w) * 80)
        draw.line([(x, 0), (x, h)], fill=(10, 10, 15, alpha))
    return Image.alpha_composite(img.convert("RGBA"), overlay)

def add_glow(draw, pos, text, font, color, radius=4):
    x, y = pos
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx == 0 and dy == 0:
                continue
            factor = 1.0 / max(abs(dx), abs(dy))
            glow_c = tuple(min(255, int(c * factor * 0.3)) for c in color[:3])
            draw.text((x + dx, y + dy), text, font=font, fill=glow_c)

def center_text(draw, img_w, y_ratio, text, font, color_name, glow=False):
    if not text:
        return
    c = COLORS.get(color_name, COLORS["white"])
    lines = text.split("\\n")
    line_h = font.size + 12
    total_h = len(lines) * line_h
    start_y = int(img_w * y_ratio) - total_h // 2
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        x = (img_w - tw) // 2
        y = start_y + i * line_h
        if glow:
            add_glow(draw, (x, y), line, font, c)
        draw.text((x, y), line, font=font, fill=c)

def add_slide_number(draw, img_w, num, total=5):
    label = f"{num}/{total}"
    f = find_font(FONT_PATHS_REGULAR, 20)
    bbox = draw.textbbox((0, 0), label, font=f)
    tw = bbox[2] - bbox[0]
    x = img_w - tw - 20
    draw.text((x, 20), label, font=f, fill=COLORS["gray"])

def add_logo_era4(draw, img_w):
    f = find_font(FONT_PATHS_BOLD, 22)
    draw.text((img_w - 100, 50), "ERA4", font=f, fill=COLORS["gray"])

def draw_list_items(draw, img_w, img_h, items, y_start, font, color_name, spacing=60, prefix="bullet"):
    c = COLORS.get(color_name, COLORS["white"])
    for i, item in enumerate(items):
        y = y_start + i * spacing
        if prefix == "bullet":
            draw.text((int(img_w * 0.08), y), "•", font=font, fill=COLORS["orange"])
            draw.text((int(img_w * 0.14), y), item, font=font, fill=c)
        elif prefix == "check":
            draw.text((int(img_w * 0.08), y), "✓", font=font, fill=COLORS["green"])
            draw.text((int(img_w * 0.14), y), item, font=font, fill=c)

def save_final(img, path):
    final = img.convert("RGB")
    final.save(path, "PNG", quality=95)
    print(f"  Salvo: {path}")

# ── MAIN ────────────────────────────────────────────────────────────
def main():
    api_key = read_env_key("OPENAI_API_KEY")
    if not api_key:
        print("ERRO: OPENAI_API_KEY não encontrada")
        sys.exit(1)
    
    os.makedirs(ASSETS_DIR, exist_ok=True)
    
    slides_info = []
    
    # ════════════════════════════════════════════════════════════════
    # SLIDE 1 — Hook: P11 Foto de empresário + overlay + texto
    # ════════════════════════════════════════════════════════════════
    print("\n=== SLIDE 1 — Hook (P11: Foto + Overlay) ===")
    
    # Generate dark background with person silhouette (since Unsplash may fail in automation)
    # Use gpt-image-1 for a stylized businessman looking at phone
    prompt_s1 = (
        "Instagram post 1:1 square. "
        "Dark tech cinematic composition. "
        "Deep black background, NO white background, NO light background. "
        "Businessman silhouette looking at smartphone screen, worried expression implied by posture. "
        "Dark moody atmosphere, subtle blue and purple ambient glow from the phone screen illuminating the figure. "
        "Professional attire, office environment barely visible. "
        "NO text, NO letters, NO numbers, NO words, NO logos. "
        "Dramatic side lighting, cinematic quality."
    )
    
    img1_bytes = generate_image(prompt_s1, api_key)
    if img1_bytes:
        base1_path = os.path.join(ASSETS_DIR, "slide_1_base.png")
        with open(base1_path, "wb") as f:
            f.write(img1_bytes)
        img1 = Image.open(base1_path).convert("RGBA")
        
        # Apply dark overlay
        img1 = apply_foto_overlay_gradient(img1)
        draw1 = ImageDraw.Draw(img1)
        w1, h1 = img1.size
        
        # Main text
        font_main1 = find_font(FONT_PATHS_BOLD, 52, "bold")
        center_text(draw1, w1, 0.30, "A Meta lancou uma IA\\nque atende e vende\\n24h no WhatsApp", font_main1, "white", glow=True)
        
        # Subtitle
        font_sub1 = find_font(FONT_PATHS_REGULAR, 28)
        center_text(draw1, w1, 0.72, "Sua PME ainda faz isso no boca a boca?", font_sub1, "rosa", glow=False)
        
        # Slide number + logo
        add_slide_number(draw1, w1, 1)
        add_logo_era4(draw1, w1)
        
        final1_path = os.path.join(ASSETS_DIR, "slide_1.png")
        save_final(img1, final1_path)
        slides_info.append({"num": 1, "tipo": "hook", "base": "slide_1_base.png", "final": "slide_1.png", "prompt": prompt_s1})
    else:
        print("ERRO: falha ao gerar slide 1")
        # Create fallback dark slide
        img1 = Image.new("RGBA", (1024, 1024), (10, 10, 15, 255))
        img1 = apply_dark_gradient(img1)
        draw1 = ImageDraw.Draw(img1)
        font_main1 = find_font(FONT_PATHS_BOLD, 52, "bold")
        center_text(draw1, 1024, 0.30, "A Meta lancou uma IA\\nque atende e vende\\n24h no WhatsApp", font_main1, "white", glow=True)
        font_sub1 = find_font(FONT_PATHS_REGULAR, 28)
        center_text(draw1, 1024, 0.72, "Sua PME ainda faz isso no boca a boca?", font_sub1, "rosa", glow=False)
        final1_path = os.path.join(ASSETS_DIR, "slide_1.png")
        save_final(img1, final1_path)
        slides_info.append({"num": 1, "tipo": "hook", "base": None, "final": "slide_1.png", "prompt": prompt_s1})
    
    # ════════════════════════════════════════════════════════════════
    # SLIDE 2 — Dado: 40% em destaque
    # ════════════════════════════════════════════════════════════════
    print("\n=== SLIDE 2 — Dado (40%) ===")
    
    prompt_s2 = (
        "Instagram post 1:1 square. "
        "Minimalist dark tech background. "
        "Deep black, NO white background, NO light background, NO bright elements. "
        "Very subtle abstract tech pattern: faint circuit traces or node connections, opacity 10%, barely visible. "
        "Slight vignette at edges. "
        "NO text, NO letters, NO numbers, NO words, NO logos."
    )
    
    img2_bytes = generate_image(prompt_s2, api_key)
    if img2_bytes:
        base2_path = os.path.join(ASSETS_DIR, "slide_2_base.png")
        with open(base2_path, "wb") as f:
            f.write(img2_bytes)
        img2 = Image.open(base2_path).convert("RGBA")
    else:
        img2 = Image.new("RGBA", (1024, 1024), (10, 10, 15, 255))
    
    img2 = apply_dark_gradient(img2)
    draw2 = ImageDraw.Draw(img2)
    w2, h2 = img2.size
    
    # Big number
    font_num = find_font(FONT_PATHS_BOLD, 120, "bold")
    center_text(draw2, w2, 0.35, "40%", font_num, "blue", glow=True)
    
    # Subtitle
    font_sub2 = find_font(FONT_PATHS_REGULAR, 32)
    center_text(draw2, w2, 0.65, "das vendas sao perdidas\\npor resposta lenta", font_sub2, "gray", glow=False)
    
    add_slide_number(draw2, w2, 2)
    add_logo_era4(draw2, w2)
    
    final2_path = os.path.join(ASSETS_DIR, "slide_2.png")
    save_final(img2, final2_path)
    slides_info.append({"num": 2, "tipo": "dado", "base": "slide_2_base.png", "final": "slide_2.png", "prompt": prompt_s2})
    
    # ════════════════════════════════════════════════════════════════
    # SLIDE 3 — Consequência: lista de problemas
    # ════════════════════════════════════════════════════════════════
    print("\n=== SLIDE 3 — Consequência ===")
    
    prompt_s3 = (
        "Instagram post 1:1 square. "
        "Dark tech illustration, moody atmosphere. "
        "Deep black background, NO white background, NO light background. "
        "Subtle orange/amber glow in one corner, warning signal atmosphere. "
        "Abstract dark composition with faint geometric shapes. "
        "NO text, NO letters, NO numbers, NO words, NO logos."
    )
    
    img3_bytes = generate_image(prompt_s3, api_key)
    if img3_bytes:
        base3_path = os.path.join(ASSETS_DIR, "slide_3_base.png")
        with open(base3_path, "wb") as f:
            f.write(img3_bytes)
        img3 = Image.open(base3_path).convert("RGBA")
    else:
        img3 = Image.new("RGBA", (1024, 1024), (10, 10, 15, 255))
    
    img3 = apply_dark_gradient(img3)
    draw3 = ImageDraw.Draw(img3)
    w3, h3 = img3.size
    
    # Title
    font_title3 = find_font(FONT_PATHS_BOLD, 44, "bold")
    center_text(draw3, w3, 0.15, "O CUSTO DA DEMORA", font_title3, "orange", glow=False)
    
    # List items
    font_list3 = find_font(FONT_PATHS_BOLD, 36, "bold")
    list_items = ["RESPOSTA EM 30 MIN", "LEAD DESISTIU", "VENDA PRO CONCORRENTE"]
    draw_list_items(draw3, w3, h3, list_items, 320, font_list3, "white", spacing=70)
    
    # Subtitle
    font_sub3 = find_font(FONT_PATHS_REGULAR, 28)
    center_text(draw3, w3, 0.88, "Cada minuto conta", font_sub3, "red", glow=False)
    
    add_slide_number(draw3, w3, 3)
    add_logo_era4(draw3, w3)
    
    final3_path = os.path.join(ASSETS_DIR, "slide_3.png")
    save_final(img3, final3_path)
    slides_info.append({"num": 3, "tipo": "consequencia", "base": "slide_3_base.png", "final": "slide_3.png", "prompt": prompt_s3})
    
    # ════════════════════════════════════════════════════════════════
    # SLIDE 4 — Solução: métricas com ícones
    # ════════════════════════════════════════════════════════════════
    print("\n=== SLIDE 4 — Solução (Métricas) ===")
    
    prompt_s4 = (
        "Instagram post 1:1 square. "
        "Dark tech solution background, clean and professional. "
        "Deep black background, NO white background, NO light background. "
        "Subtle green glow accents, feeling of growth and automation. "
        "Abstract dark composition, very faint grid pattern barely visible. "
        "NO text, NO letters, NO numbers, NO words, NO logos."
    )
    
    img4_bytes = generate_image(prompt_s4, api_key)
    if img4_bytes:
        base4_path = os.path.join(ASSETS_DIR, "slide_4_base.png")
        with open(base4_path, "wb") as f:
            f.write(img4_bytes)
        img4 = Image.open(base4_path).convert("RGBA")
    else:
        img4 = Image.new("RGBA", (1024, 1024), (10, 10, 15, 255))
    
    img4 = apply_dark_gradient(img4)
    draw4 = ImageDraw.Draw(img4)
    w4, h4 = img4.size
    
    # Title
    font_title4 = find_font(FONT_PATHS_BOLD, 40, "bold")
    center_text(draw4, w4, 0.12, "COM IA DA ERA4", font_title4, "green", glow=False)
    
    # Metrics as checks
    font_metrics = find_font(FONT_PATHS_BOLD, 34, "bold")
    metrics = ["24H ATENDENDO", "0 LEADS PERDIDOS", "RESPOSTA EM 3 SEGUNDOS"]
    draw_list_items(draw4, w4, h4, metrics, 280, font_metrics, "white", spacing=80, prefix="check")
    
    # Sub
    font_sub4 = find_font(FONT_PATHS_REGULAR, 28)
    center_text(draw4, w4, 0.88, "E possivel com IA", font_sub4, "green", glow=False)
    
    add_slide_number(draw4, w4, 4)
    add_logo_era4(draw4, w4)
    
    final4_path = os.path.join(ASSETS_DIR, "slide_4.png")
    save_final(img4, final4_path)
    slides_info.append({"num": 4, "tipo": "solucao", "base": "slide_4_base.png", "final": "slide_4.png", "prompt": prompt_s4})
    
    # ════════════════════════════════════════════════════════════════
    # SLIDE 5 — CTA: Fala com a ERA4
    # ════════════════════════════════════════════════════════════════
    print("\n=== SLIDE 5 — CTA ===")
    
    prompt_s5 = (
        "Instagram post 1:1 square. "
        "Dark tech background with pink/magenta accent glow. "
        "Deep black, NO white background, NO light background. "
        "Subtle pink-purple gradient ambient glow from bottom right corner. "
        "Professional and clean composition. "
        "NO text, NO letters, NO numbers, NO words, NO logos."
    )
    
    img5_bytes = generate_image(prompt_s5, api_key)
    if img5_bytes:
        base5_path = os.path.join(ASSETS_DIR, "slide_5_base.png")
        with open(base5_path, "wb") as f:
            f.write(img5_bytes)
        img5 = Image.open(base5_path).convert("RGBA")
    else:
        img5 = Image.new("RGBA", (1024, 1024), (10, 10, 15, 255))
    
    img5 = apply_dark_gradient(img5)
    draw5 = ImageDraw.Draw(img5)
    w5, h5 = img5.size
    
    # CTA text
    font_cta = find_font(FONT_PATHS_BOLD, 64, "bold")
    center_text(draw5, w5, 0.35, "FALA COM\\nA ERA4", font_cta, "white", glow=True)
    
    # Pink button area (drawn as rectangle with rounded feel via overlay)
    btn_y1 = int(h5 * 0.58)
    btn_y2 = int(h5 * 0.68)
    # Button outline
    overlay_btn = Image.new("RGBA", img5.size, (0, 0, 0, 0))
    draw_btn = ImageDraw.Draw(overlay_btn)
    margin = int(w5 * 0.22)
    # Draw rounded rectangle approximation
    for y in range(btn_y1, btn_y2):
        for x in range(margin, w5 - margin):
            # Check if in rounded rect
            rel_x = min(x - margin, w5 - margin - 1 - x)
            rel_y = min(y - btn_y1, btn_y2 - 1 - y)
            if rel_x >= 0 and rel_y >= 0:
                alpha = 180
                if rel_x < 15 and rel_y < 15:
                    # Corner smoothing
                    dist = ((15 - rel_x)**2 + (15 - rel_y)**2)**0.5
                    if dist > 15:
                        continue
                draw_btn.point((x, y), fill=(236, 72, 153, alpha))
    
    img5 = Image.alpha_composite(img5, overlay_btn)
    draw5 = ImageDraw.Draw(img5)
    
    # Button text
    font_btn = find_font(FONT_PATHS_BOLD, 32, "bold")
    center_text(draw5, w5, 0.62, "QUERO AUTOMATIZAR", font_btn, "white", glow=False)
    
    # URL
    font_url = find_font(FONT_PATHS_REGULAR, 24)
    center_text(draw5, w5, 0.82, "era4.com.br/contato", font_url, "gray", glow=False)
    
    add_slide_number(draw5, w5, 5)
    add_logo_era4(draw5, w5)
    
    final5_path = os.path.join(ASSETS_DIR, "slide_5.png")
    save_final(img5, final5_path)
    slides_info.append({"num": 5, "tipo": "cta", "base": "slide_5_base.png", "final": "slide_5.png", "prompt": prompt_s5})
    
    # ════════════════════════════════════════════════════════════════
    # Generate design-assets.json
    # ════════════════════════════════════════════════════════════════
    print("\n=== Gerando design-assets.json ===")
    
    design_assets = {
        "data_geracao": "2026-06-12T10:10:00-03:00",
        "formato": "carrossel",
        "padrao_visual_usado": "P11-foto-overlay-slide1_P3-dark-slides2-5",
        "experimento_ativo": None,
        "total_slides": 5,
        "slides": []
    }
    
    for s in slides_info:
        slide_data = {
            "numero": s["num"],
            "tipo": s["tipo"],
            "arquivo_base": os.path.join(ASSETS_DIR, s["base"]) if s["base"] else None,
            "arquivo_final": os.path.join(ASSETS_DIR, s["final"]),
            "url_publica": f"https://raw.githubusercontent.com/robsoncoffy/era4-instagram-squad/main/assets/{s['final']}",
            "prompt_usado": s["prompt"],
            "alt_text": f"Slide {s['num']} do carrossel sobre IA da Meta no WhatsApp — {s['tipo']}"
        }
        design_assets["slides"].append(slide_data)
    
    design_assets["erros"] = []
    
    assets_path = os.path.join(WORKSPACE, "queue", "design-assets.json")
    with open(assets_path, "w", encoding="utf-8") as f:
        json.dump(design_assets, f, ensure_ascii=False, indent=2)
    print(f"  Salvo: {assets_path}")
    
    # Update experiment log
    exp_log_path = os.path.join(WORKSPACE, "references", "experiment-log.json")
    try:
        with open(exp_log_path) as f:
            exp_log = json.load(f)
    except:
        exp_log = {"experimentos": [], "padrao_atual": {}, "proximo_teste": None}
    
    exp_log.setdefault("experimentos", []).append({
        "data": "2026-06-12",
        "post_id": "meta-ia-whatsapp-noticia",
        "padrao_base": "P11-foto-overlay",
        "elemento_testado": "P11 no slide 1 com empresário preocupado + CTA rosa no slide 5",
        "descricao": "Slide 1 com foto de empresário olhando celular com preocupação + overlay escuro assimétrico. Slides 2-4 fundo dark com tipografia. Slide 5 CTA com botão rosa.",
        "resultado_visual": "pendente",
        "feedback_robson": "pendente",
        "consolidar": False
    })
    
    with open(exp_log_path, "w", encoding="utf-8") as f:
        json.dump(exp_log, f, ensure_ascii=False, indent=2)
    print(f"  Atualizado: {exp_log_path}")
    
    print("\n=== DESIGNER CONCLUÍDO ===")
    print(f"Total slides gerados: {len(slides_info)}")
    return True

if __name__ == "__main__":
    main()
