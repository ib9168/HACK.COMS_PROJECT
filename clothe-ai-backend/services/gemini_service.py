import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the Gemini client
# The client automatically uses the GEMINI_API_KEY from the environment
try:
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    # You might want to raise an error or handle this more robustly
    client = None

def parse_garment_text(text_input: str) -> dict:
    """
    Uses Gemini to parse a user's free-form clothing description
    into a structured JSON object.

    Example input: "I have a red floral skirt"
    Example output: {"name": "Floral Skirt", "category": "Skirt", "color": "Red"}
    """
    if not client:
        return {"error": "Gemini service not available"}

    prompt = f"""
    Analyze the following user input describing a piece of clothing.
    Extract the 'name', 'category', and 'color'.
    The 'category' must be a general term like 'Shirt', 'Pants', 'Dress', 'Skirt', 'Jacket', 'Shoes', etc.
    The 'name' should be a more specific description.

    User Input: "{text_input}"
    """
    
    # Configure the model to output a JSON object using Pydantic
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Specific name/description of the garment."},
                    "category": {"type": "string", "description": "The general category, e.g., Shirt, Pants, Skirt."},
                    "color": {"type": "string", "description": "The primary color or pattern description."},
                },
                "required": ["name", "category", "color"],
            },
        ),
    )

    try:
        # The response text will be a JSON string
        return json.loads(response.text)
    except json.JSONDecodeError:
        print("Gemini response was not valid JSON.")
        return {"error": "Failed to parse garment attributes"}

def generate_outfit_idea(garment_text: str) -> str:
    """
    Uses Gemini to generate fashion advice/outfit ideas based on user input,
    drawing on famous credible fashion data as requested.
    This will be used for the "Find ideas" button.
    """
    if not client:
        return "Sorry, the AI assistant is currently unavailable."

    prompt = f"""
    You are a professional fashion assistant. Provide a creative and practical outfit suggestion
    for the user's item, drawing inspiration from credible fashion articles and magazines.
    Be encouraging and descriptive.

    The user has this item: "{garment_text}"

    Suggest:
    1. A complete outfit idea (what to pair it with).
    2. A brief tip on accessorizing.
    3. A specific occasion or style where this outfit would shine.
    """
    
    # For this task, a text response is sufficient
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )

    return response.text

def generate_outfit_from_closet(garment_list: list[dict]) -> str:
    """
    Uses Gemini to pair items from the user's closet (e.g., a shirt and a pant).
    This will be used for the 'Outfit' button.
    """
    if not client:
        return "Sorry, the AI cannot suggest a pairing right now."

    closet_items = "\n".join([f"- {g['color']} {g['name']} ({g['category']})" for g in garment_list])
    
    prompt = f"""
    You are a professional fashion stylist. A user has selected the following items
    from their digital closet. Suggest a well-matched outfit using ONLY these items.
    Explain briefly why the combination works (e.g., color theory, style synergy).
    
    User's selected items:
    {closet_items}

    Provide a concise, stylish response.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )

    return response.text