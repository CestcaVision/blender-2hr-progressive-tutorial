import os
import json
import urllib.request

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CACHE_DIR = os.path.join(BASE_DIR, ".cache_pbr")
os.makedirs(CACHE_DIR, exist_ok=True)

def download_polyhaven_asset(asset_id):
    print(f"Fetching metadata for {asset_id}...")
    meta_url = f"https://api.polyhaven.com/files/{asset_id}"
    req = urllib.request.Request(meta_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        meta = json.loads(resp.read().decode('utf-8'))

    blend_info = meta.get("blend", {}).get("1k", {}).get("blend", {})
    blend_url = blend_info.get("url")
    includes = blend_info.get("include", {})

    local_base_blend = os.path.join(CACHE_DIR, f"{asset_id}_1k.blend")
    if not os.path.exists(local_base_blend) and blend_url:
        print(f"Downloading base blend from {blend_url}...")
        urllib.request.urlretrieve(blend_url, local_base_blend)

    tex_dir = os.path.join(CACHE_DIR, "textures")
    os.makedirs(tex_dir, exist_ok=True)

    for tex_rel, tex_data in includes.items():
        tex_filename = os.path.basename(tex_rel)
        tex_local = os.path.join(tex_dir, tex_filename)
        if not os.path.exists(tex_local):
            print(f"Downloading texture {tex_filename}...")
            urllib.request.urlretrieve(tex_data["url"], tex_local)

    print(f"Asset {asset_id} downloaded successfully!")

download_polyhaven_asset("Lantern_01")
download_polyhaven_asset("marble_bust_01")
print("All open assets downloaded!")
