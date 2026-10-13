from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import yt_dlp

app = FastAPI()

@app.get("/get_song")
def get_song(title: str):
    ydl_opts = {
        'format': 'bestaudio/best',
        'default_search': 'ytsearch1',
        'noplaylist': True,
        'quiet': True
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{title}", download=False)
            if not info or 'entries' not in info or len(info['entries']) == 0:
                raise HTTPException(status_code=404, detail="Song not found")

            video_data = info['entries']
            audio_url = video_data['url'] 

            return RedirectResponse(url=audio_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
