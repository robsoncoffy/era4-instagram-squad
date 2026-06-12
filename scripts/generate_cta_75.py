#!/usr/bin/env python3
"""
Pipeline Designer — CTA 75% PMEs IA
Gera 5 slides via gpt-image-1 + overlay PIL.
"""
import os
import sys
import json
import base64
import requests
import time
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────
BASE_DIR = Path(os.path.expanduser("~/era4-instagram-squad"))
ASSETS_DIR = BASE_DIR / "assets"
QUEUE_DIR = BASE_DIR / "queue"
SCRIPTS_DIR = BASE_DIR / "scripts"

ASSETS_DIR.mkdir(exist_ok=True)

# ── API Key ────────────────────────────────────────────────────────────
def read_env_key(key_name):
    env_file = BASE_DIR / ".env"
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if key_name in line and "=" in line and not line.startswith("#"):
                return line.split("=", 1)[1].strip()
    return None

API_KEY=read_env_key("OPENAI_API_KEY")
if not API_KEY:
    print("ERRO: OPENAI_API_KEY nao encontrada")
    sys.exit(1)

# ── gpt-image-1 ────────────────────────────────────────────────────────
def generate_image(prompt, output_path, retries=2):
    """Gera imagem via gpt-image-1 e salva em output_path."""
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }
    
    for attempt in range(retries + 1):
        try:
            print(f"  Gerando {output_path.name} (tentativa {attempt+1})...")
            resp = requests.post(url, headers=headers, json=payload, timeout=120)
            if resp.status_code == 200:
                data = resp.json()
                img_bytes = base64.b64decode(data["data"][0]["b64_json"])
                with open(output_path, "wb") as f:
                    f.write(img_bytes)
                print(f"  OK: {output_path.name} ({len(img_bytes)} bytes)")
                return True
            else:
                print(f"  ERRO {resp.status_code}: {resp.text[:200]}")
                if attempt < retries:
                    time.sleep(5)
        except Exception as e:
            print(f"  EXCEPTION: {e}")
            if attempt < retries:
                time.sleep(5)
    
    print(f"  FALHA ao gerar {output_path.name}")
    return False

# ── Prompts por slide ─────────────────────────────────────────────────
# P3 — Tipografia pura: fundo escuro, sem texto, sem elementos visuais
# P5 — Layout comparativo VS
# P10 — Personagem 3D + CTA

prompts = {
    "slide_1": (
        "Dark background #0a0a0f with subtle gradient to deep navy #0f172a. "
        "Minimalist tech aesthetic. No text, no letters, no words, no numbers. "
        "Subtle glowing blue light effect in the center area, very faint. "
        "Clean, empty, dark canvas ready for text overlay. "
        "NO text, NO letters, NO words, NO logos, NO numbers."
    ),
    "slide_2": (
        "Dark background #0a0a0f with subtle gradient. "
        "Minimalist tech aesthetic with very faint geometric grid lines in darker tone. "
        "Subtle blue and orange light accents on opposite sides. "
        "No text, no letters, no words, no numbers. "
        "Clean dark canvas for text overlay. "
        "NO text, NO letters, NO words, NO logos, NO numbers."
    ),
    "slide_3": (
        "Dark background #0a0a0f. "
        "Split composition: left side slightly red-tinted dark, right side slightly orange-tinted dark. "
        "Subtle diagonal dividing line. "
        "No text, no letters, no words, no numbers. "
        "Minimalist, clean, dark canvas for text overlay. "
        "NO text, NO letters, NO words, NO logos, NO numbers."
    ),
    "slide_4": (
        "Dark background #0a0a0f with subtle green-tinted glow in lower portion. "
        "Minimalist tech aesthetic. Very faint circuit-board pattern in dark green. "
        "No text, no letters, no words, no numbers. "
        "Clean dark canvas for text overlay. "
        "NO text, NO letters, NO words, NO logos, NO numbers."
    ),
    "slide_5": (
        "3D cartoon robot character, blue and white color scheme, friendly confident expression, "
        "centered in lower half of frame, dark navy #0a0a0f background, "
        "subtle purple circle glow behind character, "
        "small rounded button shape near the character in blue, "
        "NO text, NO letters, NO words, NO logos."
    ),
}

# ── Gerar todas as imagens base ────────────────────────────────────────
print("=" * 60)
print("GERANDO IMAGENS BASE VIA GPT-IMAGE-1")
print("=" * 60)

results = {}
for slide_name, prompt in prompts.items():
    output = ASSETS_DIR / f"{slide_name}_base.png"
    success = generate_image(prompt, output)
    results[slide_name] = {
        "success": success,
        "path": str(output)
    }
    time.sleep(2)  # Rate limit

# ── Verificar resultados ───────────────────────────────────────────────
print("\n" + "=" * 60)
print("RESULTADO GERACAO")
print("=" * 60)
for slide, r in results.items():
    status = "OK" if r["success"] else "FALHA"
    print(f"  {slide}: {status}")

# Salvar status para o proximo script usar
status_file = QUEUE_DIR / "generation-status.json"
with open(status_file, "w") as f:
    json.dump(results, f, indent=2)

print(f"\nStatus salvo em: {status_file}")
