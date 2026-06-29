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

prompt = """Dark tech background #0a0a0f, large bold white text centered reading "IA no WhatsApp" with three vertical icons below: a headset icon labeled "ATENDE", a filter icon labeled "QUALIFICA", and a dollar sign icon labeled "CONVERTE". Neon green #22c55e accent color for icons and subtle glow effects. Small text at bottom reading "Fala com a ERA4". Clean minimalist sans-serif typography, Instagram story vertical format, professional dark aesthetic with subtle grid pattern in background."""

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
with urllib.request.urlopen(req, timeout=120) as resp:
    data = json.loads(resp.read())
    img_bytes = base64.b64decode(data["data"][0]["b64_json"])
    out_path = os.path.expanduser("~/era4-instagram-squad/assets/story_4.png")
    with open(out_path, "wb") as f:
        f.write(img_bytes)
    print(f"Image saved: {out_path} ({len(img_bytes)} bytes)")
