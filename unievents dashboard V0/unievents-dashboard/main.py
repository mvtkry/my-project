from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pathlib import Path

app = FastAPI(title="UniEvents Dashboard")

# Setup templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Sample data for demonstration
SAMPLE_DATA = {
    "total_events": 24,
    "active_participants": 156,
    "completed_scorings": 18,
    "leaderboard_entries": 50,
    "recent_events": [
        {"id": 1, "name": "Spring Hackathon", "date": "2024-03-15", "participants": 45, "status": "upcoming"},
        {"id": 2, "name": "Chess Tournament", "date": "2024-03-10", "participants": 32, "status": "completed"},
        {"id": 3, "name": "Debate Finals", "date": "2024-03-05", "participants": 16, "status": "scoring"},
    ],
    "top_participants": [
        {"rank": 1, "name": "Alex Chen", "score": 9850, "events": 12},
        {"rank": 2, "name": "Jamie Smith", "score": 9720, "events": 10},
        {"rank": 3, "name": "Taylor Wong", "score": 9540, "events": 11},
    ]
}

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Redirect root to dashboard"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/dashboard")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard overview"""
    return templates.TemplateResponse(
        "dashboard/index.html", 
        {"request": request, "data": SAMPLE_DATA, "active_page": "overview"}
    )

@app.get("/dashboard/events", response_class=HTMLResponse)
async def events(request: Request):
    """Events management page"""
    return templates.TemplateResponse(
        "dashboard/events.html", 
        {"request": request, "events": SAMPLE_DATA["recent_events"], "active_page": "events"}
    )

@app.get("/dashboard/participants", response_class=HTMLResponse)
async def participants(request: Request):
    """Participants list and management"""
    return templates.TemplateResponse(
        "dashboard/participants.html", 
        {"request": request, "active_page": "participants"}
    )

@app.get("/dashboard/scoring", response_class=HTMLResponse)
async def scoring(request: Request):
    """Scoring interface"""
    return templates.TemplateResponse(
        "dashboard/scoring.html", 
        {"request": request, "active_page": "scoring"}
    )

@app.get("/dashboard/leaderboard", response_class=HTMLResponse)
async def leaderboard(request: Request):
    """Leaderboard display"""
    return templates.TemplateResponse(
        "dashboard/leaderboard.html", 
        {"request": request, "leaders": SAMPLE_DATA["top_participants"], "active_page": "leaderboard"}
    )

@app.get("/dashboard/single-entry", response_class=HTMLResponse)
async def single_entry(request: Request):
    """Single entry form for quick scoring"""
    return templates.TemplateResponse(
        "dashboard/single-entry.html", 
        {"request": request, "active_page": "single-entry"}
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    