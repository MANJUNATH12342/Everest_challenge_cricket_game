from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
import json

class ProcessInputViewTest(TestCase):
    
    def setUp(self):
        # Set up the client for testing
        self.client = Client()
        self.url = reverse('process_input')  # Assuming this is the correct URL name for the view
    
    @patch('game.views.Read_input_files')
    def test_valid_input(self, mock_read_files):
        # Mock the input files
        mock_read_files.return_value.bowling_shot_mapping_file.return_value = {
            'fast': ['cut', 'drive']
        }
        mock_read_files.return_value.commentary_file.return_value = {
            'Good shot': {'result': [1, 2], 'shot': ['cut']},
            'No ball': {'result': [5]}
        }
        mock_read_files.return_value.shot_timing_outcome_file.return_value = {
            'timing': {
                'early': [1, 2, 5],
                'perfect': [4]
            }
        }

        # Simulate valid input
        valid_data = {
            'bowling-type': 'fast',
            'shot': 'cut',
            'timing': 'early'
        }

        response = self.client.post(self.url, data=json.dumps(valid_data), content_type='application/json')

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertIn('outcome', response_data)
        self.assertIn('commentary', response_data)

    @patch('game.views.Read_input_files')
    def test_invalid_bowling_type(self, mock_read_files):
        mock_read_files.return_value.bowling_shot_mapping_file.return_value = {
            'fast': ['cut', 'drive']
        }
        mock_read_files.return_value.commentary_file.return_value = {}
        mock_read_files.return_value.shot_timing_outcome_file.return_value = {'timing': {}}

        invalid_bowling_type_data = {
            'bowling-type': 'spin',  # Invalid bowling type
            'shot': 'cut',
            'timing': 'early'
        }

        response = self.client.post(self.url, data=json.dumps(invalid_bowling_type_data), content_type='application/json')

        # Check if the response returns 400 for invalid bowling type
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid bowling type')

    @patch('game.views.Read_input_files')
    def test_invalid_shot(self, mock_read_files):
        mock_read_files.return_value.bowling_shot_mapping_file.return_value = {
            'fast': ['cut', 'drive']
        }
        mock_read_files.return_value.commentary_file.return_value = {}
        mock_read_files.return_value.shot_timing_outcome_file.return_value = {'timing': {}}

        invalid_shot_data = {
            'bowling-type': 'fast',
            'shot': 'sweep',  # Invalid shot for 'fast' bowling
            'timing': 'early'
        }

        response = self.client.post(self.url, data=json.dumps(invalid_shot_data), content_type='application/json')

        # Check if the response returns 400 for invalid shot
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid shot')

    @patch('game.views.Read_input_files')
    def test_invalid_timing(self, mock_read_files):
        mock_read_files.return_value.bowling_shot_mapping_file.return_value = {
            'fast': ['cut', 'drive']
        }
        mock_read_files.return_value.commentary_file.return_value = {}
        mock_read_files.return_value.shot_timing_outcome_file.return_value = {
            'timing': {
                'early': [1, 2, 5],
                'perfect': [4]
            }
        }

        invalid_timing_data = {
            'bowling-type': 'fast',
            'shot': 'cut',
            'timing': 'late'  # Invalid timing
        }

        response = self.client.post(self.url, data=json.dumps(invalid_timing_data), content_type='application/json')

        # Check if the response returns 400 for invalid timing
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid timing')

    def test_invalid_json_format(self):
        # Send invalid JSON format
        response = self.client.post(self.url, data="invalid json", content_type='application/json')

        # Check if the response returns 400 for invalid JSON
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid JSON format')

    @patch('game.views.Read_input_files')
    def test_file_not_found(self, mock_read_files):
        # Mock a file not found error
        mock_read_files.side_effect = FileNotFoundError()

        valid_data = {
            'bowling-type': 'fast',
            'shot': 'cut',
            'timing': 'early'
        }

        response = self.client.post(self.url, data=json.dumps(valid_data), content_type='application/json')

        # Check if the response returns 404 for file not found
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['error'], 'File not found')

    def test_invalid_method(self):
        # Use GET instead of POST to trigger the "Invalid request method" error
        response = self.client.get(self.url)
        
        # Check if the content type is JSON or HTML
        if response.headers['Content-Type'] == 'application/json':
            # If JSON, check for the error message
            self.assertEqual(response.json()['error'], 'Invalid request method')
        else:
            # If not JSON, fail the test
            self.fail(f'Expected JSON response, but got {response.headers["Content-Type"]}')

class PlaySuperOverViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('play_super_over')  # Adjust if your URL pattern is different

    def mock_input_files(self):
        """Mock the Read_input_files class and methods"""
        from unittest.mock import patch, MagicMock

        # Mock Read_input_files and its methods
        self.mock_read_input_files = patch('game.utils.Read_input_files').start()
        self.mock_input_files = MagicMock()
        self.mock_read_input_files.return_value = self.mock_input_files

        # Mock JSON file returns
        self.mock_input_files.bowling_shot_mapping_file.return_value = {
            'Fast': ['Flick', 'Drive'],
            'Spin': ['Cut', 'Defend']
        }
        self.mock_input_files.commentary_file.return_value = {
            'Good shot': {'result': [1, 2, 3, 4, 6], 'shot': ['Flick', 'Drive']},
            'Great shot': {'result': [4, 6], 'shot': ['Drive']}
        }
        self.mock_input_files.shot_timing_outcome_file.return_value = {
            'timing': {
                'Good': [1, 2, 3, 4],
                'Perfect': [6, 4],
                'Late': [0]
            }
        }
        self.mock_input_files.teams_file.return_value = {
            'teams': [
                {'name': 'India', 'players': ['Player1', 'Player2']},
                {'name': 'Australia', 'players': ['PlayerA', 'PlayerB']}
            ]
        }

    def tearDown(self):
        patch.stopall()




    def test_no_json(self):
        self.mock_input_files()
        response = self.client.post(self.url, 'invalid data', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertEqual(response_data['error'], 'Invalid JSON format')

       
    @patch('game.views.Read_input_files')
    def test_invalid_bowling_type(self, mock_read_files):
        mock_read_files.return_value.bowling_shot_mapping_file.return_value = {
            'fast': ['cut', 'drive']
        }
        mock_read_files.return_value.commentary_file.return_value = {}
        mock_read_files.return_value.shot_timing_outcome_file.return_value = {'timing': {}}

        invalid_bowling_type_data = {
            'bowling-type': 'spin',  # Invalid bowling type
            'shot': 'cut',
            'timing': 'early'
        }

        response = self.client.post(self.url, data=json.dumps(invalid_bowling_type_data), content_type='application/json')

        # Check if the response returns 400 for invalid bowling type
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid bowling type')

    @patch('game.views.Read_input_files')
    def test_invalid_shot(self, mock_read_files):
        mock_read_files.return_value.bowling_shot_mapping_file.return_value = {
            'fast': ['cut', 'drive']
        }
        mock_read_files.return_value.commentary_file.return_value = {}
        mock_read_files.return_value.shot_timing_outcome_file.return_value = {'timing': {}}

        invalid_shot_data = {
            'bowling-type': 'fast',
            'shot': 'sweep',  # Invalid shot for 'fast' bowling
            'timing': 'early'
        }

        response = self.client.post(self.url, data=json.dumps(invalid_shot_data), content_type='application/json')

        # Check if the response returns 400 for invalid shot
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid shot')

    @patch('game.views.Read_input_files')
    def test_invalid_timing(self, mock_read_files):
        mock_read_files.return_value.bowling_shot_mapping_file.return_value = {
            'fast': ['cut', 'drive']
        }
        mock_read_files.return_value.commentary_file.return_value = {}
        mock_read_files.return_value.shot_timing_outcome_file.return_value = {
            'timing': {
                'early': [1, 2, 5],
                'perfect': [4]
            }
        }

        invalid_timing_data = {
            'bowling-type': 'fast',
            'shot': 'cut',
            'timing': 'late'  # Invalid timing
        }

        response = self.client.post(self.url, data=json.dumps(invalid_timing_data), content_type='application/json')

        # Check if the response returns 400 for invalid timing
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Invalid timing')

