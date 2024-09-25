from django.test import TestCase, Client
from django.urls import reverse
import json
from unittest.mock import patch

class PlaySuperOverTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('play_super_over')  # Make sure this matches the URL name in your urlpatterns

    @patch('game.views.Read_input_files')
    def test_play_super_over(self, mock_read_input_files):
        """
        Test the play_super_over function for valid input and check the response.
        """

        # Mock data for input files
        mock_input_files = mock_read_input_files.return_value
        mock_input_files.bowling_shot_mapping_file.return_value = {
            "pace": ["cover drive", "pull"],
            "spin": ["sweep", "reverse sweep"]
        }
        mock_input_files.commentary_file.return_value = {
            "Great shot!": {"result": [4], "shot": ["cover drive"]},
            "What a hit!": {"result": [6], "shot": ["pull"]},
            "Clean shot!": {"result": [1], "shot": ["sweep"]}
        }
        mock_input_files.shot_timing_outcome_file.return_value = {
            "timing": {
                "early": [0, 1],
                "perfect": [4, 6],
                "late": [1, 2, 5]  # Includes no-ball outcome 5
            }
        }

        # Prepare input data for the POST request
        input_data = {
            "bowling-type": "pace",
            "shot": "cover drive",
            "timing": "perfect",
            "batsman": "Batsman A",
            "bowler": "Bowler B"
        }

        # Simulate a POST request to the play_super_over endpoint
        response = self.client.post(self.url, json.dumps(input_data), content_type='application/json')

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check the structure of the response
        response_data = response.json()
        self.assertIn('result', response_data)
        self.assertIn('ball_outcomes', response_data)
        self.assertIn('current_ball', response_data)
        self.assertIn('total_runs', response_data)
        self.assertIn('wickets_lost', response_data)
        self.assertIn('target_runs', response_data)
        self.assertIn('Total_wickets', response_data)

        # Check if the total_runs and wickets_lost are being updated
        self.assertGreaterEqual(response_data['total_runs'], 0)
        self.assertGreaterEqual(response_data['wickets_lost'], 0)

        # Additional assertions can be made based on expected outcomes
        self.assertIsInstance(response_data['ball_outcomes'], list)
        self.assertIsInstance(response_data['current_ball'], dict)

