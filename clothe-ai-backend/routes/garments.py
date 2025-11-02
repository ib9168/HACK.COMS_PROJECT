from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Import the data access functions from the Model layer
import models.garment as garment_model 

# Define the router instance (CRUCIAL for app.py to include this route)
router = APIRouter(prefix="/api/garments", tags=["Closet Management"])

# --- Pydantic Models for Data Validation ---

# Base model for reading data out
class GarmentResponse(BaseModel):
    id: str
    name: str
    category: str
    color: str
    
    # Allows the model to be created from SQLAlchemy/Pandas objects
    class Config:
        from_attributes = True 

# Model for creating a new garment (ID is generated in the model)
class GarmentCreate(BaseModel):
    name: str
    category: str
    color: str

# Model for updating existing garment (fields are optional)
class GarmentUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    color: Optional[str] = None

# --- API Endpoints (CRUD) ---

@router.get("/", response_model=List[GarmentResponse])
def list_all_garments():
    """
    READ: Returns the entire list of garments in the user's closet.
    """
    # Calls the model layer function to fetch all data
    return garment_model.list_garments()

@router.post("/", response_model=GarmentResponse, status_code=201)
def create_garment(garment: GarmentCreate):
    """
    CREATE: Adds a new garment to the database.
    """
    # Calls the model layer function to perform the data creation
    new_record = garment_model.add_garment(
        name=garment.name, 
        category=garment.category, 
        color=garment.color
    )
    return new_record

@router.put("/{garment_id}", response_model=GarmentResponse)
def update_garment_item(garment_id: str, updates: GarmentUpdate):
    """
    UPDATE: Updates an existing garment by ID.
    """
    # Convert Pydantic model to a clean dict, ignoring fields that weren't provided (None)
    update_dict = updates.model_dump(exclude_none=True)
    
    if not update_dict:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    
    try:
        # Calls the model layer function to perform the update
        updated_record = garment_model.update_garment(garment_id, update_dict)
        return updated_record
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Garment ID '{garment_id}' not found")

@router.delete("/{garment_id}", status_code=204)
def delete_garment_item(garment_id: str):
    """
    DELETE: Removes a garment by its ID. Returns 204 No Content on success.
    """
    # Calls the model layer function to perform the deletion
    garment_model.remove_garment(garment_id)
    return # FastAPI automatically returns 204 No Content for successful None/empty return