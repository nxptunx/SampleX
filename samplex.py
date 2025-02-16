import requests
from bs4 import BeautifulSoup
import os
import re

def download_samplefocus_mp3(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 OPR/116.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.samplefocus.com/",
        "DNT": "1",
        "Connection": "keep-alive"
    }
    try:
        with requests.Session() as session:
            session.get("https://www.samplefocus.com/", headers=headers)
            response = session.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            audio_tag = soup.find('audio')
            if audio_tag and (src := audio_tag.get('src')):
                mp3_url = src
            else:
                download_btn = soup.find('a', {'class': re.compile(r'download', re.I)})
                mp3_url = download_btn.get('href') if download_btn else None
            if not mp3_url:
                if match := re.search(r'"(https?://[^"]+\.mp3)"', response.text):
                    mp3_url = match.group(1)
            if not mp3_url:
                return "MP3 URL not found. Page structure may have changed."
            mp3_url = requests.compat.urljoin(url, mp3_url)
            mp3_response = session.get(mp3_url, headers=headers, stream=True)
            mp3_response.raise_for_status()
            filename = os.path.basename(mp3_url.split('?')[0])
            if not filename.endswith('.mp3'):
                filename = f"{os.path.basename(url)}.mp3"
            with open(filename, 'wb') as f:
                for chunk in mp3_response.iter_content(chunk_size=32768):
                    f.write(chunk)
            return f"Successfully downloaded: {filename}"
    except requests.RequestException as e:
        return f"Network error: {str(e)}"
    except Exception as e:
        return f"Critical error: {str(e)}"
if __name__ == "__main__":
    url = input("Enter SampleFocus URL: ").strip()
    print(download_samplefocus_mp3(url))