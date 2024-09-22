$(document).ready(function() {
    // Load data for Bowling Types
    $.get('/get_mapping_data/', function(data) {
        var bowlingTypeSelect = $('#bowling-type');
        var timingSelect = $('#timing');

        // Populate Bowling Types
        $.each(data.bowling_shot_mapping, function(key, value) {
            bowlingTypeSelect.append($('<option>', {
                value: key,
                text: key
            }));
        });

        // Populate Timing Options
        timingSelect.empty(); // Clear existing options
        timingSelect.append($('<option>', {
            value: '',
            text: 'Select Timing'
        }));
        $.each(data.shot_timing_outcome.timing, function(timing, values) {
            timingSelect.append($('<option>', {
                value: timing,
                text: timing
            }));
        });
    });
    // Handle form submission
    $('#inputForm').on('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission

        var data = {
            'bowling-type': $('#bowling-type').val(),
            'shot': $('#shot').val(),
            'timing': $('#timing').val()
        };
        console.log("Sending data:", data);
        $.ajax({
            url: '/process_input/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                $('#response').html(`<p>Outcome: ${response.outcome}</p><p>Commentary: ${response.commentary}</p>`);
            },
            error: function(xhr) {
                $('#response').html(`<p>Error: ${xhr.responseJSON.error}</p>`);
            }
        });
    });

    // Update Shot options based on selected Bowling Type
    $('#bowling-type').on('change', function() {
        var selectedBowlingType = $(this).val();
        var shotSelect = $('#shot');
        shotSelect.empty();
        shotSelect.append($('<option>', {
            value: '',
            text: 'Select Shot'
        }));

        if (selectedBowlingType) {
            $.get('/get_mapping_data/', function(data) {
                var shots = data.bowling_shot_mapping[selectedBowlingType] || [];
                $.each(shots, function(index, shot) {
                    shotSelect.append($('<option>', {
                        value: shot,
                        text: shot
                    }));
                });
            });
        }
    });
});
