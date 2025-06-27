from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import io
import matplotlib
matplotlib.use('Agg')  # Prevent GUI issues
import matplotlib.pyplot as plt

app = FastAPI()

# Mount static files (style.css)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory analytics data
analytics_data = {
    "questions": 0,
    "predictions": 0,
    "treatments": 0
}

@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Template rendering failed: {str(e)}")

@app.post("/ask")
async def ask(symptoms: str = Form(...)):
    analytics_data["questions"] += 1
    return JSONResponse({"response": f"Based on symptoms ({symptoms}), rest and hydrate."})

@app.post("/predict")
async def predict(symptoms: str = Form(...)):
    analytics_data["predictions"] += 1
    return JSONResponse({"prediction": "Common Cold", "risk": "Low"})

@app.post("/treatment")
async def treatment(condition: str = Form(...)):
    analytics_data["treatments"] += 1
    return JSONResponse({"treatment": f"For {condition}, take fluids, rest, and paracetamol."})

@app.get("/analytics", response_class=HTMLResponse)
def analytics_page(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})

@app.get("/analytics-graph")
def analytics_graph():
    data = {'questions': 3, 'predictions': 2, 'treatments': 1}  # replace with real values
    plt.figure(figsize=(6, 4))
    plt.bar(data.keys(), data.values(), color='skyblue')
    plt.title('HealthAI Usage Stats')
    plt.ylabel('Count')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return StreamingResponse(buf, media_type="image/png")