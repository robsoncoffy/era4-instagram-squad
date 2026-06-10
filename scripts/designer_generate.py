import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

# --- Download de fotos reais (P7 e P8) ---

def download_unsplash_photo(query, output_path, w=1024, h=1024):
    """Baixa foto do Unsplash Source (não precisa de API key).
    Unsplash Source: https://source.unsplash.com/{w}x{h}/?{query}
    """
    url = f"https://source.unsplash.com/{w}x{h}/?{query}"
    print(f"  Baixando foto: {url}")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        # Unsplash Source redireciona para a foto real — seguir redirects
        with urllib.request.urlopen(req, timeout=30) as resp:
            # A URL final contém a foto
            final_url = resp.url
            # Agora baixar a imagem da URL final
            with urllib.request.urlopen(final_url, timeout=60) as img_resp:
                img_data = img_resp.read()
                if len(img_data) < 1000:
                    print(f"  ⚠ Foto muito pequena ({len(img_data)} bytes), tentando alternativa...")
                    return False
                with open(output_path, "wb") as f:
                    f.write(img_data)
                print(f"  ✅ Foto salva: {output_path} ({len(img_data)} bytes)")
                return True
    except Exception as e:
        print(f"  ❌ Erro ao baixar foto: {e}")
        return False

def download_unsplash_photo_api(query, output_path, api_key=None):
    """Alternativa: usa Unsplash API se houver access key configurada."""
    if api_key:
        url = f"https://api.unsplash.com/search/photos?query={query}&per_page=1&orientation=square"
        try:
            req = urllib.request.Request(url, headers={
                "Authorization": f"Client-ID {api_key}",
                "User-Agent": "Mozilla/5.0"
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read())
            if result["results"]:
                img_url = result["results"][0]["urls"]["regular"]
                with urllib.request.urlopen(img_url, timeout=60) as img_resp:
                    img_data = img_resp.read()
                with open(output_path, "wb") as f:
                    f.write(img_data)
                print(f"  ✅ Foto Unsplash API salva: {output_path} ({len(img_data)} bytes)")
                return True
        except Exception as e:
            print(f"  ❌ Erro Unsplash API: {e}")
    return False

# Ler API key

unsplash_key = None
api_key = None
with open(os.path.expanduser("~/era4-instagram-squad/.env")) as f:
    for line in f:
        if "OPENAI_API_KEY" in line and "=" in line:
            api_key = line.strip().split("=", 1)[1]
            break

if not api_key:
    print("ERRO: OPENAI_API_KEY nao encontrada")
    exit(1)

# Tentar ler Unsplash key (opcional — se não tiver, usa Unsplash Source)
with open(os.path.expanduser("~/era4-instagram-squad/.env")) as f:
    for line in f:
        if "UNSPLASH_ACCESS_KEY" in line and "=" in line:
            unsplash_key = line.strip().split("=", 1)[1].strip()
            break

unsplash_key = unsplash_key if unsplash_key and unsplash_key != "your_key_here" else None

print(f"API key encontrada: {api_key[:10]}...")
if unsplash_key:
    print(f"Unsplash key encontrada: {unsplash_key[:8]}...")
else:
    print("Unsplash key não configurada — usando Unsplash Source (sem key)")

# Config
ASSETS_DIR = os.path.expanduser("~/era4-instagram-squad/assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

SLIDES = [
    {
        "numero": 1,
        "prompt": 'Instagram carrossel post, 1:1 square format, modern dark tech aesthetic. Pitch black background #0a0a0f, NO white background, NO light background. Large bold number "75%" centered in electric blue #3b82f6, below it smaller white text "das PMEs ainda não usam IA" in sans-serif font. Minimalist layout, clean design, subtle circuit board pattern in the background. Dark tech aesthetic, NO white background, dark background #0a0a0f throughout.',
        "alt": "Slide 1 - Hook: 75% das PMEs ainda nao usam IA"
    },
    {
        "numero": 2,
        "prompt": 'Instagram carrossel post, 1:1 square format, modern dark tech aesthetic. Pitch black background #0a0a0f, NO white background, NO light background. Large bold number "30 min" centered in orange-red #f97316, below it smaller white text "é o tempo médio de resposta de uma PME" in sans-serif font. Small icon of a clock with exclamation mark. Minimalist layout, clean design. Dark tech aesthetic, NO white background, dark background #0a0a0f throughout.',
        "alt": "Slide 2 - Problema: 30 min tempo medio de resposta"
    },
    {
        "numero": 3,
        "prompt": 'Instagram carrossel post, 1:1 square format, modern dark tech aesthetic. Pitch black background #0a0a0f, NO white background, NO light background. Large bold number "40%" centered in neon green #22c55e, below it smaller white text "dos leads são perdidos por demora" in sans-serif font. Simple ascending bar chart graphic in green. Minimalist layout, clean design. Dark tech aesthetic, NO white background, dark background #0a0a0f throughout.',
        "alt": "Slide 3 - Dado: 40% dos leads perdidos por demora"
    },
    {
        "numero": 4,
        "prompt": 'Instagram carrossel post, 1:1 square format, modern dark tech aesthetic. Pitch black background #0a0a0f, NO white background, NO light background. Text "IA no WhatsApp" centered in white bold font, below it three connected boxes with arrows showing flow: "Atende" -> "Qualifica" -> "Converte" in electric blue #3b82f6. Minimalist icons for each step. Clean flowchart design. Dark tech aesthetic, NO white background, dark background #0a0a0f throughout.',
        "alt": "Slide 4 - Solucao: IA no WhatsApp fluxo Atende Qualifica Converte"
    },
    {
        "numero": 5,
        "prompt": 'Instagram carrossel post, 1:1 square format, modern dark tech aesthetic. Gradient background from deep blue #1e3a5f to purple #4c1d95, NO white background. Large bold white text "Não fique nos 75%" centered, below it smaller text "Fala com a ERA4" in electric blue #3b82f6. Small ERA4 logo placeholder at bottom. Button-style visual element. Dark tech aesthetic, vibrant gradient, NO white background.',
        "alt": "Slide 5 - CTA: Nao fique nos 75% - Fala com a ERA4"
    }
]

results = []
erros = []

for slide in SLIDES:
    num = slide["numero"]
    print(f"\nGerando slide {num}...")
    
    data = json.dumps({
        "model": "gpt-image-1",
        "prompt": slide["prompt"],
        "n": 1,
        "size": "1024x1024"
    }).encode("utf-8")
    
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    )
    
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
        
        b64 = result["data"][0]["b64_json"]
        img_bytes = base64.b64decode(b64)
        
        filepath = os.path.join(ASSETS_DIR, f"slide3_{num}.png")
        with open(filepath, "wb") as f:
            f.write(img_bytes)
        
        print(f"  -> Salvo: {filepath} ({len(img_bytes)} bytes)")
        results.append({
            "numero": num,
            "arquivo_local": f"~/era4-instagram-squad/assets/slide3_{num}.png",
            "url_publica": f"https://raw.githubusercontent.com/robsoncoffy/era4-instagram-squad/main/assets/slide3_{num}.png",
            "prompt_usado": slide["prompt"][:100] + "...",
            "alt_text": slide["alt"]
        })
    except Exception as e:
        print(f"  -> ERRO: {e}")
        erros.append({"slide": num, "erro": str(e)})
    
    if num < len(SLIDES):
        time.sleep(5)

# Salvar resultado
output = {
    "data_criacao": datetime.now(timezone(timedelta(hours=-3))).isoformat(),
    "slides_gerados": results,
    "total_slides": len(results),
    "erros": erros
}

output_path = os.path.expanduser("~/era4-instagram-squad/queue/design-assets.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n\nResultado salvo em {output_path}")
print(f"Slides gerados: {len(results)}/{len(SLIDES)}")
if erros:
    print(f"Erros: {len(erros)}")
    for e in erros:
        print(f"  Slide {e['slide']}: {e['erro']}")
