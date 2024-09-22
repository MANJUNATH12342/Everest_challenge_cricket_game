$(document).ready(function() {
    // Fetch mapping data from the API and populate dropdowns
    $.ajax({
        url: '/get_mapping_data/',  // URL for fetching mapping data
        method: 'GET',
        success: function(data) {
            // Populate bowling types
            const bowlingTypes = data.bowling_shot_mapping;
            const bowlingSelect = $('#bowling-type');
            for (let type in bowlingTypes) {
                bowlingSelect.append(new Option(type, type));
            }

            // Populate timing
            const timingData = data.shot_timing_outcome.timing;
            const timingSelect = $('#timing');
            for (let timing in timingData) {
                timingSelect.append(new Option(timing, timing));
            }

            // Populate teams and players for bowler and batsman
            const teamsData = data.Team_players.teams;
            const bowlerSelect = $('#bowler');
            const batsmanSelect = $('#batsman');

            // Clear existing options
            bowlerSelect.empty();
            batsmanSelect.empty();

            // Filter and populate bowler select with Australian players
            const australiaTeam = teamsData.find(team => team.team_name === 'Australia');
            if (australiaTeam) {
                australiaTeam.players.forEach(player => {
                    bowlerSelect.append(new Option(player, player));
                });
            }

            // Filter and populate batsman select with Indian players
            const indiaTeam = teamsData.find(team => team.team_name === 'India');
            if (indiaTeam) {
                indiaTeam.players.forEach(player => {
                    batsmanSelect.append(new Option(player, player));
                });
            }

            // Update shot dropdown based on selected bowling type
            $('#bowling-type').on('change', function() {
                const selectedBowlingType = $(this).val();
                const shots = bowlingTypes[selectedBowlingType] || [];
                const shotSelect = $('#shot');
                shotSelect.empty();
                shots.forEach(shot => {
                    shotSelect.append(new Option(shot, shot));
                });
            });
        },
        error: function(error) {
            console.log('Error fetching mapping data:', error);
        }
    });

    // Super Over form submission handler
    $('#superOverForm').on('submit', function(e) {
        e.preventDefault();  // Prevent default form submission
        const formData = $(this).serializeArray();  // Serialize form data

        // Convert serialized array to JSON
        const data = {};
        formData.forEach(item => {
            data[item.name] = item.value;
        });

        // Make AJAX call to play the Super Over
        $.ajax({
            url: '/play_super_over/',  // URL for form submission
            method: 'POST',
            contentType: 'application/json',  // Set content type to JSON
            data: JSON.stringify(data),  // Convert data to JSON
            success: function(response) {
                // Update the response box with the ball outcomes
                const responseBox = $('#response');
                responseBox.empty();  // Clear the previous outcomes

                if (response.ball_outcomes && response.ball_outcomes.length) {
                    response.ball_outcomes.forEach(outcome => {
                        let outcomeText = outcome.outcome === "wicket" ? 'Wicket' : outcome.bowler + ' bowled ' +  outcome.bowling_type + ' ball, '+ outcome.batsman + ' played '+ outcome.timing + ' '+ outcome.shot + ' shot ' + outcome.commentary + ' - '+ outcome.outcome + ' runs'  ;
                        responseBox.append(`<p><strong>Ball ${outcome.ball_number}:</strong> ${outcomeText}</p>`);
                    });
                }
                
                // Display total runs and wickets lost
                if (response.total_runs !== undefined) {
                    responseBox.append(`<p><strong>Total Runs: ${response.total_runs}:</strong> </p>`);
                    responseBox.append(`<p><strong>Target Rus: ${response.target_runs}:</strong> </p>`);
                    
                }
                
                if (response.wickets_lost !== undefined) {
                    responseBox.append(`<p><strong>Wickets Lost: ${response.wickets_lost}:</strong> </p>`);
                    responseBox.append(`<p><strong>Total wickets in hand: ${response.total_wickets_in_hand}:</strong> </p>`);
                }

                responseBox.append('<p>' + response.result + '</p>');
                console.log(response)
                // Check if the game is over and prompt the user
                if (response.play_again) {
                    $('#play-again-container').show(); // Show the play again button
                    // Disable input elements
                    $('#superOverForm input, #superOverForm select, #superOverForm button').prop('disabled', true);

                    $('#play-again-button').off('click').on('click', function() {
                        location.reload();  // Refresh the page to restart the game
                    });
                    $('#go-to-home-page').off('click').on('click', function() {
                        window.location.href = '/'; // Redirect to a specific link
                    });
                }
            },
            error: function(error) {
                console.log('Error submitting form:', error);
            }
        });
    });
});