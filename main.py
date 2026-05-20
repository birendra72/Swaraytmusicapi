from fastapi import FastAPI, HTTPException
from ytmusicapi import YTMusic

# Initialize the API and YouTube Music client
app = FastAPI(title="Swara Audio Engine")
yt = YTMusic()

@app.get("/")
def health_check():
    """Tells Render and your app that the server is awake."""
    return {"status": "online", "engine": "ytmusicapi"}

@app.get("/search")
def search_music(query: str, filter_type: str = "songs"):
    """
    Search for music. 
    Defaults to 'songs' to ensure pure audio (no music video intros/ads).
    Available filters: songs, videos, albums, artists, playlists.
    """
    try:
        results = yt.search(query=query, filter=filter_type)
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trending")
def get_home_feed():
    """
    Pulls the latest hits and charts to populate your Jetpack Compose Home Screen.
    """
    try:
        charts = yt.get_charts()
        return {"status": "success", "data": charts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/song/{video_id}")
def get_song_details(video_id: str):
    """
    Pass the videoId from the search results to this endpoint 
    to get the raw playback data.
    """
    try:
        details = yt.get_song(video_id)
        return {"status": "success", "data": details}
    except Exception as e:
        raise HTTPException(status_code=404, detail="Song data not found")

@app.get("/podcasts")
def get_podcasts(query: str, limit: int = 20):
    """
    Search for podcasts in YTMusic.
    """
    try:
        results = yt.search(query=query, filter="podcasts", limit=limit)
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/videos")
def get_videos(query: str, limit: int = 20):
    """
    Search for videos in YTMusic.
    """
    try:
        results = yt.search(query=query, filter="videos", limit=limit)
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/live")
def get_live(query: str, limit: int = 20):
    """
    Search for live streams in YTMusic.
    Since there is no explicit 'live' filter, we search general results.
    """
    try:
        results = yt.search(query=query, limit=limit)
        return {"status": "success", "data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/charts")
def get_global_charts(country: str = "IN"):
    """
    Get top charts for a specific country.
    """
    try:
        charts = yt.get_charts(country=country)
        return {"status": "success", "data": charts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
