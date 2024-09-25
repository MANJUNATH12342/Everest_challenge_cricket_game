from django.test import TestCase, Client
from django.urls import reverse
import json
from unittest.mock import patch
from django.conf import settings
from pathlib import Path

class ProcessInputTestCase(TestCase):
    base_dir = Path(settings.BASE_DIR)

    def setUp(self):
        self.client = Client()
        self.url = reverse('process_input')  # Ensure this URL is correct

    @patch('game.utils.Read_input_files.bowling_shot_mapping_file')  # Adjust import path as needed
    @patch('game.utils.Read_input_files.commentary_file')  # Adjust import path as needed
    @patch('game.utils.Read_input_files.shot_timing_outcome_file')  # Adjust import path as needed
    @patch('random.choice')  # Mocking random.choice
    def test_process_input_valid(self, mock_random_choice, mock_shot_timing_outcome_file, 
                                  mock_commentary_file, mock_bowling_shot_mapping_file):
        """
        Test valid input for bowling type, shot, and timing, and checks outcome and commentary.
        """

        # Mock data for input files
        mock_bowling_shot_mapping_file.return_value = {
            "pace": ["cover drive", "pull"],
            "spin": ["sweep", "reverse sweep"]
        }

        mock_commentary_file.return_value = {
            "Great shot!": {"result": [4], "shot": ["cover drive"]},
            "What a hit!": {"result": [6], "shot": ["pull"]},
            "Clean shot!": {"result": [1], "shot": ["sweep"]}
        }

        mock_shot_timing_outcome_file.return_value = {
            "timing": {
                "early": [0, 1],
                "perfect": [4, 6],
                "late": [1, 2, 5]  # Includes no-ball outcome 5
            }
        }

        # Control random.choice to return specific outcome for testing
        mock_random_choice.side_effect = lambda x: x[0]  # Always returns the first item

        # Input data for the test
        input_data = {
            "bowling-type": "pace",
            "shot": "cover drive",
            "timing": "perfect"
        }

        # Send POST request with the input data
        response = self.client.post(self.url, json.dumps(input_data), content_type='application/json')

        # Expected outcome based on mock data
        expected_outcome = 4  # From the "perfect" timing mapping
        expected_commentary = "Great shot!"  # Commentary for the shot

        # Assertions to check response data
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data['outcome'], expected_outcome)
        self.assertEqual(response_data['commentary'], expected_commentary)

