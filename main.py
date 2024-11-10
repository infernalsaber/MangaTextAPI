from fastapi import FastAPI, HTTPException, Query
from pathlib import Path
import json
from functools import lru_cache, cache
import glob
from collections import defaultdict

app = FastAPI(
    title="MangaTextAPI",
    description="A manga text search engine API",
    version="0.0.1"
)

@lru_cache
def load_manga_data(manga_name: str) -> dict:
    """Load manga data from JSON file"""
    try:
        file_path = Path(f"manga/{manga_name}.json")
        with open(file_path) as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Manga '{manga_name}' not found")

# @cache
def search_text(text: dict, query: str) -> list:
    """
    Custom search implementation
    Returns list of matches containing the query string
    """
    results = defaultdict(dict)
    # Implement custom search logic here
    # This is a basic case-insensitive substring search
    query_words = query.lower().split()
    
    for chapter in text['chapters'].keys():
        for page in text['chapters'][chapter].keys():
            for query in query_words:
                if not query in text['chapters'][chapter][page].lower():
                    break
                if not results[eval(chapter)].get("pages"):
                    results[eval(chapter)]["pages"] = []
                results[eval(chapter)]["pages"].append(eval(page))
    return results

@app.get("/raw/{manga_name}")
async def get_raw_text(manga_name: str):
    """Get raw text content for a specific manga"""
    data = load_manga_data(manga_name)
    return data

@app.get("/search/{manga_name}")
async def search_manga(manga_name: str, q: str = Query(..., description="Search query")):
    """Search for specific text in manga content"""
    data = load_manga_data(manga_name)
    results = search_text(data, q)
    
    if not results:
        return {"message": "No matches found", "results": []}
    
    total_results = sum([len(v.get("pages", [])) for v in results.values()])
    
    return {
        "message": f"{total_results} matches found",
        'title': data['title'],
        'search_query': q,
        "results": results,
        "last_updated": data['last_updated']
    }

@app.get("/list")
async def list_manga():
    """List all available manga"""
    Path("manga").mkdir(exist_ok=True)
    manga_files = glob.glob("manga/*.json")
    manga_list = [Path(file).stem for file in manga_files]
    
    print(manga_list)
    print(load_manga_data.cache_info())
    
    mangas = []
    
    for endpoint in manga_list:
        mangas.append({
            "endpoint": f"/{endpoint}",
            "title": load_manga_data(endpoint)['title']
        })
    
    return mangas
    
@app.get("/")
async def root():
    return "Welcome to MangaTextAPI, go to /docs to get started and /list to see the available manga"

@app.get("/info")
async def info():
    return {
        "title": app.title,
        "description": app.description,
        "version": app.version,
        "link": "https://github.com/infernalsaber/MangaTextAPI"
    }
