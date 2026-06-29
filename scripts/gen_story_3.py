import os, json, urllib.request, base64

# Ler OPENAI_API_KEY do .env
env_path = os.path.expanduser("~/era4-instagram-squad/.env")
api_key = None
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line.startswith("OPENAI_API_KEY"):
            api_key = line.split("=", 1)[1]
            break

print(f"API key loaded: {api_key[:10]}...")

prompt = (
    "Dark tech aesthetic Instagram story background, 9:16 vertical format. "
    "Background color: deep black #0a0a0f with subtle dark blue gradient. "
    "Large bold number '70%' centered in neon green #22c55e, glowing effect. "
    "Below the number, white bold sans-serif text: 'dos clientes nunca mais contatados'. "
    "Smaller text at bottom in light gray: 'Follow-up automatico resolve isso'. "
    "Clean minimalist design, no photos, typography-focused. "
    "Subtle circuit board pattern in background at 10% opacity. "
    "Professional dark tech brand aesthetic, high contrast, readable text."
)

payload = json.dumps({
    "model": "gpt-image-1",
    "prompt": prompt,
    "n": 1,
    "size": "1024x1536"
}).encode()

req = urllib.request.Request(
    "https://api.openai.com/v1/images/generations",
    data=payload,
    headers={"Content-Type": "application/json", "Authorization": "Bearer " + api_key},
    method="POST"
)

print("Generating image...")
with urllib.request.urlopen(req, timeout=120) as resp:
    data = json.loads(resp.read())
    img_bytes = base64.b64decode(data["data"][0]["b64_json"])
    out_path = os.path.expanduser("~/era4-instagram-squad/assets/story_3.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(img_bytes)
    print(f"Image saved: {out_path} ({len(img_bytes)} bytes)")
