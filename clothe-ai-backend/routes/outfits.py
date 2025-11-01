#This file handles the text-based user input and outfit generation
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from services import gemini_service
from models import garment as garment_model #  to avoid confusion with the file name

router = APIRouter(prefix="/api/outfits", tags=["Outfits"])

# Request model for the "Find ideas" feature
class UserInput(BaseModel):
    userId: str # Not strictly used in this function but good for context
    text: str   # e.g., "I have a red floral skirt"

# Request model for the "Outfit" button feature
class GarmentPair(BaseModel):
    userId: str
    garmentIds: List[str] # List of IDs for the items the user selected to pair

# 1. Endpoint for "Find ideas" (uses generate_outfit_idea) 
@router.post("/find-ideas")
async def find_fashion_ideas(req: UserInput):
    """
    Receives text input (e.g., "I have a red floral skirt") and
    returns a fashion advice/idea from Gemini.
    """
    idea_text = gemini_service.generate_outfit_idea(req.text)
    return {"userId": req.userId, "idea": idea_text}

# 2. Endpoint for parsing garment text (your existing analyze endpoint) 
@router.post("/analyze")
async def analyze_user_input(req: UserInput):
    """
    Receives the user's clothing text input, sends it to Gemini for parsing,
    and returns structured attributes back to the frontend.
    """
    structured_data = gemini_service.parse_garment_text(req.text)
    return {"userId": req.userId, "parsed": structured_data}

#  3. Endpoint for "Outfit" pairing (uses generate_outfit_from_closet) 
@router.post("/generate")
async def generate_outfit_pair(req: GarmentPair):
    """
    Receives a list of garment IDs selected by the user, retrieves their data,
    and asks Gemini to suggest a good pairing.
    """
    # 1. Retrieve the full garment data for the selected IDs
    all_garments = garment_model.list_garments()
    selected_garments = [
        g for g in all_garments if g['id'] in req.garmentIds
    ]
    
    if not selected_garments:
        return {"userId": req.userId, "outfit_suggestion": "Please select at least one item to generate an outfit."}

    # 2. Send the data to the Gemini service
    suggestion = gemini_service.generate_outfit_from_closet(selected_garments)
    
    return {"userId": req.userId, "outfit_suggestion": suggestion, "items_used": selected_garments}

