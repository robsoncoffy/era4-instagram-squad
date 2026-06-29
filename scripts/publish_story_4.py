import os, json, urllib.request

# Ler ZERNIO_API_KEY do .env
env_path = os.path.expanduser("~/era4-instagram-squad/.env")
zernio_key = None
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line.startswith("ZERNIO_API_KEY"):
            zernio_key = line.split("=", 1)[1]
            break

print(f"Zernio key loaded: {zernio_key[:10]}...")

media_url = "https://media.zernio.com/temp/1781211785329_jhjetf27_story_4.png"

payload = json.dumps({
    "content": "IA no WhatsApp: Atende | Qualifica | Converte. Fala com a ERA4.",
    "mediaItems": [{"type": "image", "url": media_url}],
    "platforms": [{
        "platform": "instagram",
        "accountId": "6a21fe912b2567671ad44380",
        "platformSpecificData": {"contentType": "story"}
    }],
    "publishNow": True
}).encode()

req = urllib.request.Request(
    "https://api.zernio.com/v1/posts",
    data=payload,
    headers={"Content-Type": "application/json", "Authorization": "Bearer " + zernio_key},
    method="POST"
)
with urllib.request.urlopen(req, timeout=60) as resp:
    result = json.loads(resp.read())
    print(json.dumps(result, indent=2))
