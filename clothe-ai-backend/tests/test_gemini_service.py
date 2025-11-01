# tests/test_gemini_service.py
import unittest
import json
from unittest.mock import patch, MagicMock
from services.gemini_service import parse_garment_text, generate_outfit_idea, generate_outfit_from_closet

class TestGeminiService(unittest.TestCase):

    # --- Test 1: Structured Parsing (analyze) ---
    @patch('services.gemini_service.client')
    def test_parse_garment_text_success(self, mock_client):
        # 1. Define the mocked successful AI response (as a JSON string)
        mock_json_response = {
            "name": "Flowy Maxi Skirt",
            "category": "Skirt",
            "color": "Red Floral"
        }
        mock_response_text = json.dumps(mock_json_response)
        
        # 2. Configure the mock client's behavior
        mock_response = MagicMock()
        mock_response.text = mock_response_text
        mock_client.models.generate_content.return_value = mock_response

        # 3. Call the function with test data
        result = parse_garment_text("I have a red floral flowy maxi skirt")

        # 4. Assertions: check if the result matches the mocked output
        self.assertEqual(result, mock_json_response)
        self.assertEqual(result['category'], "Skirt")

    # --- Test 2: Outfit Idea Generation (find-ideas) ---
    @patch('services.gemini_service.client')
    def test_generate_outfit_idea_success(self, mock_client):
        # 1. Define the mocked successful AI response (as a plain string)
        expected_suggestion = "A great match for your skirt is a crisp white linen shirt..."
        
        # 2. Configure the mock client's behavior
        mock_response = MagicMock()
        mock_response.text = expected_suggestion
        mock_client.models.generate_content.return_value = mock_response

        # 3. Call the function
        result = generate_outfit_idea("red floral skirt")

        # 4. Assertions
        self.assertIn("linen shirt", result)
        self.assertEqual(result, expected_suggestion)

# Run the tests
if __name__ == '__main__':
    unittest.main()