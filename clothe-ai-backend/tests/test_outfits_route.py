from fastapi.testclient import TestClient
from unittest.mock import patch
from app import app # Import the main FastAPI application instance

# Create a test client instance pointing to your FastAPI app
client = TestClient(app)

# Define mock data that Gemini *should* return for different functions
MOCK_PARSED_DATA = {"name": "Trousers", "category": "Bottom", "color": "Navy"}
MOCK_IDEA = "Style your navy trousers with a silk blouse for a chic look."
MOCK_PAIRING = "The selected items create a perfect monochromatic outfit suggestion."

# Mock data for database lookup (used in the /generate test)
MOCK_GARMENT_DB = [
    {"id": "a1", "name": "Striped Shirt", "category": "Top", "color": "Black/White"},
    {"id": "b2", "name": "Jeans", "category": "Bottom", "color": "Dark Blue"}
]

class TestOutfitRoutes:
    
    # --- Test 1: POST /api/outfits/analyze (Parsing text into structured data) ---
    # We patch the external service function
    @patch('services.gemini_service.parse_garment_text', return_value=MOCK_PARSED_DATA)
    def test_analyze_user_input_success(self, mock_parse):
        response = client.post(
            "/api/outfits/analyze",
            json={"userId": "test1234", "text": "I have a navy blue pant"}
        )
        # 1. Assert the HTTP status code is 200 (OK)
        assert response.status_code == 200
        data = response.json()
        
        # 2. Assert the returned data matches the mock service's output
        assert data["userId"] == "test1234"
        assert data["parsed"]["color"] == "Navy"
        
        # 3. Verify the service function was called exactly once
        mock_parse.assert_called_once()


    # --- Test 2: POST /api/outfits/find-ideas (Getting long-form advice) ---
    @patch('services.gemini_service.generate_outfit_idea', return_value=MOCK_IDEA)
    def test_find_fashion_ideas_success(self, mock_idea):
        response = client.post(
            "/api/outfits/find-ideas",
            json={"userId": "test1234", "text": "red floral skirt"}
        )
        assert response.status_code == 200
        data = response.json()
        
        # Assert the AI response is correctly returned
        assert data["idea"] == MOCK_IDEA
        mock_idea.assert_called_once()
        
        
    # --- Test 3: POST /api/outfits/generate (Getting outfit pairing) ---
    # This requires mocking BOTH the database lookup AND the gemini service call
    @patch('services.gemini_service.generate_outfit_from_closet', return_value=MOCK_PAIRING)
    @patch('models.garment.list_garments', return_value=MOCK_GARMENT_DB)
    def test_generate_outfit_pair_success(self, mock_list_garments, mock_generate):
        # Request uses the IDs defined in MOCK_GARMENT_DB
        request_ids = ["a1", "b2"]
        response = client.post(
            "/api/outfits/generate",
            json={"userId": "test1234", "garmentIds": request_ids}
        )
        assert response.status_code == 200
        data = response.json()
        
        # 1. Assert the final AI suggestion is returned
        assert data["outfit_suggestion"] == MOCK_PAIRING
        
        # 2. Verify the model function was called to get the items
        mock_list_garments.assert_called_once()
        
        # 3. Verify the Gemini function was called with the correct *filtered* data
        # It should only be called with the two items specified by the IDs
        mock_generate.assert_called_once()
        
        # 4. Check if the items used in the response are correct
        assert len(data["items_used"]) == 2
        assert data["items_used"][0]["id"] == "a1"

    # --- Test 4: POST /api/outfits/generate (Handling no items selected) ---
    @patch('services.gemini_service.generate_outfit_from_closet')
    @patch('models.garment.list_garments', return_value=MOCK_GARMENT_DB)
    def test_generate_outfit_pair_no_items(self, mock_list_garments, mock_generate):
        # Request with IDs that don't exist in the mock database
        response = client.post(
            "/api/outfits/generate",
            json={"userId": "test1234", "garmentIds": ["z9"]}
        )
        assert response.status_code == 200
        data = response.json()
        
        # The route should return a specific message for no items
        assert "Please select at least one item" in data["outfit_suggestion"]
        
        # The Gemini service should NOT have been called
        mock_generate.assert_not_called()