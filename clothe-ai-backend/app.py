import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

# Import routers
from routes import outfits, garments

# Load environment variables (like the GEMINI_API_KEY)
load_dotenv()

app = FastAPI(
    title="Clothe AI Backend",
    description="Backend API for the AI Clothe Tracker Assistant using FastAPI and Gemini.",
    version="1.0.0",
)

# Include the routers
app.include_router(outfits.router)
app.include_router(garments.router)

@app.get("/")
def read_root():
    """Simple health check endpoint."""
    return {"message": "Clothe AI Backend is running!"}

if __name__ == "__main__":
    # Note: Use `uvicorn app:app --reload` for development from the terminal
    # This is for basic local testing/deployment
    uvicorn.run(app, host="0.0.0.0", port=8000)