import requests
import random
from bs4 import BeautifulSoup
from datetime import datetime
import os

# Ambil webhook dari GitHub Secrets
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Daftar kata kunci pencarian
search_queries = [
    "cewek sexy", "cewek cantik", "anime sexy", "hentai", "bacol", "tobrut", "ceker babat"
]

def get_pinterest_images(search_query):
    search_url = f"https://www.pinterest.com/search/pins/?q={search_query.replace(' ', '%20')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    images = [img.get("src") for img in soup.find_all("img") if img.get("src") and "pinimg.com" in img.get("src")]
    return images

def send_to_discord(image_url, search_query):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    payload = {
        "embeds": [
            {
                "title": "🔍 Hasil Pencarian Gambar",
                "description": f"👤 **Username** : none\n📡 **Search** : {search_query}\n🌐 **Internet** : Pinterest\n⏰ **Time** : {current_time}",
                "image": {"url": image_url},
                "footer": {"text": "Dikirim via Webhook"},
                "color": 16711680  # Warna merah
            }
        ]
    }
    requests.post(WEBHOOK_URL, json=payload)

if WEBHOOK_URL:
    search_query = random.choice(search_queries)
    images = get_pinterest_images(search_query)
    
    if images:
        random_image = random.choice(images)
        send_to_discord(random_image, search_query)
        print(f"Gambar dikirim ({search_query}): {random_image}")
    else:
        print(f"Gagal mengambil gambar untuk {search_query}.")
else:
    print("Webhook URL tidak ditemukan! Pastikan sudah diset di GitHub Secrets.")
