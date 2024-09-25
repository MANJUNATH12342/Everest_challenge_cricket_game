import json
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils import Read_input_files,Validation_and_operation

def index(request):
    return render(request, 'index.html')

def super_over_view(request):

    return render(request, 'super_over.html')  # Render the HTML form

@csrf_exempt
def get_mapping_data(request):
    """
    This function returns all the input json files 
    """
    try:

        input_files = Read_input_files()
        bowling_shot_mapping = input_files.bowling_shot_mapping_file()
        commentary = input_files.commentary_file()
        shot_timing_outcome = input_files.shot_timing_outcome_file()
        teams_players_mapping = input_files.teams_file()

        data = {
            'bowling_shot_mapping': bowling_shot_mapping,
            'commentary': commentary,
            'shot_timing_outcome': shot_timing_outcome,
            'Team_players': teams_players_mapping
        }

        return JsonResponse(data)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@csrf_exempt
def process_input(request):
    """
    This function allows the user to give the input for bowling type , shot, and timing and returns the random runs and commentary
    according to the  mapping in the input json files  
    """
    try:
        input_files = Read_input_files()
        validate_inputs_and_operation = Validation_and_operation()
        bowling_shot_mapping = input_files.bowling_shot_mapping_file()
        commentary = input_files.commentary_file()
        shot_timing_outcome = input_files.shot_timing_outcome_file()

        if request.method == 'POST':
            # Get input data from the request
            input_data = json.loads(request.body)
            bowling_type = input_data.get('bowling-type')
            shot = input_data.get('shot')
            timing = input_data.get('timing')
            
            validation_error = validate_inputs_and_operation.validate_inputs(bowling_type, shot, timing, bowling_shot_mapping, shot_timing_outcome)
            if validation_error:
                return validation_error

            # Determine possible outcomes based on timing
            possible_outcomes = shot_timing_outcome['timing'][timing]
            outcome = random.choice(possible_outcomes)

            # Determine commentary
            commentary_text = "No commentary available"
            commentary_matched_for_multiple_outcome = []
            for key, value in commentary.items():
                
                values = value.get('result', [])
    
                if outcome in values:
                    if 'shot' in value and shot in value['shot']:
                        commentary_matched_for_multiple_outcome.append(key)
                        # commentary_text = key
                    elif 'shot' not in value:
                        commentary_matched_for_multiple_outcome.append(key)
                        # commentary_text = key
       
            if outcome == 5:
                
                commentary_text = random.choice(commentary_matched_for_multiple_outcome) + ". Its a no ball and four runs"
            else:
                commentary_text = random.choice(commentary_matched_for_multiple_outcome) 
                    # break

            return JsonResponse({'outcome': outcome, 'commentary': commentary_text})
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except FileNotFoundError:
        return JsonResponse({'error': 'File not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



@csrf_exempt
def play_super_over(request):
    """ 
    This function allows the user to give the input for bowling type , shot, timing , batsman, and bowler for the super over
    and returns the the random runs and commentary according to the  mapping in the input json files
    """
    try:
        # Load JSON files
        input_files = Read_input_files()
        validate_inputs_and_operation = Validation_and_operation()
        bowling_shot_mapping = input_files.bowling_shot_mapping_file()
        commentary = input_files.commentary_file()
        shot_timing_outcome = input_files.shot_timing_outcome_file()
        game_track=[]
        # Game state (for demonstration, use session to track state)
        if 'game_state' not in request.session:
            request.session['game_state'] = {
                'balls_played': 0,
                'wickets_lost': 0,
                'total_runs': 0,
                'ball_outcomes': [],
                'target_runs': 21,
                'wickets': 2,

            }

        game_state = request.session['game_state']

        if request.method == 'POST':
            input_data = json.loads(request.body)
            bowling_type = input_data.get('bowling-type')
            shot = input_data.get('shot')
            timing = input_data.get('timing')
            bowler = input_data.get('bowler')
            batsman = input_data.get('batsman')
            
            # Validate input data
            validation_error = validate_inputs_and_operation.validate_inputs(bowling_type, shot, timing, bowling_shot_mapping, shot_timing_outcome)
            if validation_error:
                return validation_error

            # Determine possible outcomes based on timing
            possible_outcomes = shot_timing_outcome['timing'][timing]
            outcome = random.choice(possible_outcomes)

            # Match commentary
            commentary_text = random.choice([
                key for key, value in commentary.items()
                if outcome in value.get('result', []) and (shot in value.get('shot', []) or 'shot' not in value)
            ]) if outcome != 5 else "No ball, four runs!"

            # Process ball outcome (runs, wicket)
            if outcome != "wicket":
                game_state['total_runs'] += outcome
            else:
                game_state['wickets_lost'] += 1

            game_state['balls_played'] += 1
            # Record ball 
            game_state['ball_outcomes'].append({
                'ball_number': game_state['balls_played'],
                'bowler': bowler,
                'batsman': batsman,
                'outcome': outcome,
                'bowling_type':bowling_type,
                'shot': shot,
                'timing': timing,
                'commentary': commentary_text,
                'target_runs': game_state['target_runs'],
                'total_wickets_in_hand': game_state['wickets']-game_state['wickets_lost']
                
            })
            # End match conditions
            if game_state['total_runs'] >= game_state['target_runs']:
                result = "India Won!"
                game_over = True
                request.session.flush()  # Clear game state at the 
            elif game_state['wickets_lost'] >= game_state['wickets']:
                result = "India Lost!"
                game_over = True
                request.session.flush()  # Clear game state at the end
            elif game_state['balls_played'] >= 6:
                result = f"India Lost!. India scored {game_state['total_runs']} runs in 6 balls."
                game_over = True
                request.session.flush()  # Clear game state at the end
            else:
                result = "Next ball..."
                game_over = False

            # Response data
            response = {
                'result': result,
                'ball_outcomes': game_state['ball_outcomes'],
                'current_ball': {
                    'bowler': bowler,
                    'batsman': batsman,
                    'outcome': outcome,

                    'commentary': commentary_text
                },
                'total_runs': game_state['total_runs'],
                'wickets_lost': game_state['wickets_lost'],
                'target_runs': game_state['target_runs'],
                'Total_wickets': game_state['wickets'],
                'play_again': game_over 
            }
            request.session.modified = True
            game_track.append(response)
            if game_over == True:   
                input_files.super_over_match_result(response)
            return JsonResponse(response)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

