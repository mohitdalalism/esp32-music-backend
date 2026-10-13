from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import yt_dlp
import os

app = FastAPI()

@app.get("/get_song")
def get_song(title: str):
    # Setup standard web headers to keep YouTube from throwing 403 / Player extraction blocks
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1',
        'noplaylist': True,
        'quiet': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
        }
    }
    try:
        # Trigger an internal check to ensure yt-dlp binary remains refreshed
        os.system("pip install --upgrade yt-dlp")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{title}", download=False)
            if not info or 'entries' not in info or len(info['entries']) == 0:
                raise HTTPException(status_code=404, detail="Song not found")
                
            video_data = info['entries'][0]
            audio_url = video_data['url'] 
            
            return RedirectResponse(url=audio_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

