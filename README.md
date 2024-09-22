# Everest Challenge Cricket Game 
## Project Overview

This is a Django-based web application that serves as a basic tool for predicting the outcomes of cricket balls. Users can simulate various scenarios by selecting parameters like bowling type, shot, and timing. The application dynamically calculates outcomes such as runs and wickets while providing commentary for each ball played.

In addition to its core functionality, users can also engage in a Super Over match simulation, allowing them to play through 6 balls with predefined rules. This makes the application not only a predictive tool but also an interactive cricket experience.

## Directory Structure

```bash
cricket_game/
│
├── cricket_game/            # Project settings and configuration
│   ├── __init__.py          # Marks the directory as a Python package
│   ├── __pycache__/         # Compiled Python files for performance
│   ├── asgi.py              # ASGI configuration for asynchronous deployments
│   ├── settings.py          # Main settings for the Django project
│   ├── urls.py              # URL routing for the entire project
│   └── wsgi.py              # WSGI configuration for deploying the application
│
|
│
├── game/                    # Django app directory containing game logic
│   ├── __init__.py          # Marks the directory as a Python package
│   ├── __pycache__/         # Compiled Python files for performance
│   ├── admin.py             # Admin configuration for the app
│   ├── apps.py              # App configuration class
│   ├── env/                 # Virtual environment directory (not typically included in version control)
│   ├── migrations/          # Database migrations for the app
│   ├── models.py            # This is not used in the application at present as the game is generating the json file for the tracking of the super over match 
│   ├── tests.py             # Tests for the application
│   ├── urls.py              # URL routing for the app
│   ├── utils.py             # Utility functions used in the app
│   └── views.py             # Views for handling requests and returning responses
│
├── input_data/                       # JSON input files for game configuration
│   ├── bowling_shot_mapping.json     # Mapping between bowling types and shots
│   ├── commentary.json               # Commentary texts for game events
│   ├── shot_timing_outcome.json      # Timing-based outcomes for shots
│   └── teams.json                    # Team configuration data
│
├── output_data/             # Directory for output data
│   └── super_over_match.json # Results of the Super Over match
│
├── static/                  # Static files (CSS, JS, images)
│   ├── css/                 # CSS files for styling
│   │   ├── style.css        # Main stylesheet
│   │   ├── style.css.bkup2  # Backup of the main stylesheet
│   │   └── super_over.css   # Stylesheet for Super Over
│   └── js/                  # JavaScript files for client-side logic
│       ├── script.js        # Main JavaScript file
│       └── super_over.js    # JavaScript for Super Over functionality
│
├── templates/               # HTML templates for rendering views
│   ├── index.html           # Home page template
│   └── super_over.html      # Template for the Super Over feature
│
└── manage.py                # Django management script for running commands
```
## **CHALLENGE #1: PREDICTING OUTCOME**
## **CHALLENGE #2: PREDICTING OUTCOME WITH COMMENTARY**

## **Required Data**
- **Bowl Types:** List of different bowling types available in the game.
- **Shot Types:** Collection of various shots that players can choose to play.
- **Shot Timings:** Timings associated with each shot that affect the outcome.

## **Assumptions Made**
1. **Mapping of Shots:** Each shot type is mapped to specific bowling types.
2. **Outcome Determination:** Runs depend on the timing of the shot.
3. **Commentary Mapping:** Commentary is generated based on the runs scored.
4. **Game Dynamics:** 
   - The simulation uses random choice for dynamic outcomes.
   - Users can select bowling types, shot types, and timings.
5. **User Interaction:** 
   - The interface is user-friendly.
   - Instructions are clearly provided for each step.


## **CHALLENGE #3: SUPER OVER PREDICTION**

### **Required Data**
- **Bowl Types:** List of different bowling types available in the game.
- **Shot Types:** Collection of various shots that players can choose to play.
- **Shot Timings:** Timings associated with each shot that affect the outcome.
- **Batsman:** Players participating in the Super Over.
- **Bowler:** The bowler delivering the balls in the Super Over.

### **Assumptions Made**
1. **Target Score:** Australia has scored 20 runs, and the target for the user is 21 runs with 2 wickets in hand.
2. **Mapping of Shots:** Each shot type is mapped to specific bowling types.
3. **Outcome Determination:** Runs depend on the timing of the shot.
4. **Commentary Mapping:** Commentary is generated based on the runs scored.


### **Points to Note**
- **Ball Tracking:** Each ball played in the Super Over will be tracked and displayed.
- **User Interaction:** The interface is user-friendly, and instructions are clearly provided for each step.
- **Match Results Storage:** The results of the match will be stored in an output file for future reference.
-------------------------------------------------------------------------------------------------------------------------

## **Installation and Running the Game**

### **Prerequisites**
- Ensure Python (version 3.6 or later) is installed on your machine.
- Have pip (Python package installer) available.

### **Installing Django**
1. Open your terminal or command prompt.
2. Install Django using pip:
   ```bash
   pip install django
   ```
3. Cloning repository
   git clone https://github.com/MANJUNATH12342/Everest_challenge_cricket_game/tree/development
4. Navigate into the project directory
5. Navigate into the project directory
  
      ```bash
    python manage.py runserver
   ```
## **Playing the Game**

- To play the normal cricket game (Challenge #1 and Challenge #2), navigate to the `/` URL.
- To play the Super Over game, click on the button labeled "Play Super Over" on the homepage. This will redirect you to the Super Over game interface.
