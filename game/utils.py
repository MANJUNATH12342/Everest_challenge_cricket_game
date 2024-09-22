import json
from django.conf import settings
from pathlib import Path
from django.http import JsonResponse
from datetime import datetime

class Read_input_files():
        # Load JSON files
    def bowling_shot_mapping_file(self):
        base_dir = Path(settings.BASE_DIR)
        with open(base_dir / 'input_data' / 'bowling_shot_mapping.json') as f:
            bowling_shot_mapping = json.load(f)
        return bowling_shot_mapping
    
    def commentary_file(self):
        base_dir = Path(settings.BASE_DIR)
        with open(base_dir / 'input_data' / 'commentary.json') as f:
            commentary = json.load(f)
        return commentary
    
    def shot_timing_outcome_file(self):
        base_dir = Path(settings.BASE_DIR)
        with open(base_dir / 'input_data' / 'shot_timing_outcome.json') as f:
            shot_timing_outcome = json.load(f)
        return shot_timing_outcome
    
    def teams_file(self):
        base_dir = Path(settings.BASE_DIR)
        with open(base_dir / 'input_data' / 'teams.json') as f:
            teams_players_mapping = json.load(f)
        return teams_players_mapping
    
    def super_over_match_result(self,json_data):
        base_dir = Path(settings.BASE_DIR)
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f'super_over_match_{current_time}.json'
        new_data = {k: v for k, v in json_data.items() if k != "current_ball" and k!="play_again" }
        json_object = json.dumps(new_data,indent=4)
        with open(base_dir / 'output_data' / file_name,'w') as f:
            f.write(json_object)
            
        return json_object

class Validation_and_operation():
    def validate_inputs(self,bowling_type, shot, timing, bowling_shot_mapping, shot_timing_outcome):
        if bowling_type not in bowling_shot_mapping:
            return JsonResponse({'error': 'Invalid bowling type'}, status=400)

        if shot not in bowling_shot_mapping[bowling_type]:
            return JsonResponse({'error': 'Invalid shot'}, status=400)

        if timing not in shot_timing_outcome['timing']:
            return JsonResponse({'error': 'Invalid timing'}, status=400)

        return None
    