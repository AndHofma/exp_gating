"""
Gating-Experiment

This script conducts a gating experiment using the PsychoPy library.
The experiment involves presenting auditory stimuli to the participant,
who is required to respond in real-time.
The stimuli are separated into practice and test phases, each with their own randomization protocols.

The script handles:

Preparation: It imports necessary libraries, checks the paths for input and output data,
loads or generates randomized stimuli, and prepares the experiment window.

Participant Interaction: Collects participant's demographic information, presents instructions,
and manages user interface during the practice and test phases.

Data Collection: Records participant responses, computes performance metrics, and stores
the data in a structured CSV format for future analysis.
"""

from psychopy import core
from path_check import check_config_paths
from configuration import create_window, initialize_stimuli, get_participant_info,  practice_stimuli_path, test_stimuli_path, results_path, pics_path, random_path
from gating_functions import show_message, run_trial_phase
from instructions import begin, test, end
from randomization import load_and_randomize

# Check if input and output paths exist
check_config_paths(test_stimuli_path, practice_stimuli_path, results_path, pics_path, random_path)  # make sure that in and out paths exist

# Get participant information
participant_info = get_participant_info()

practice_stimuli = load_and_randomize(practice_stimuli_path, participant_info)
test_stimuli = load_and_randomize(test_stimuli_path, participant_info)

# Create the window
window = create_window()

# Initialize screen
fixation_cross, bracket_pic, bracket_pos_label, nobracket_pic, nobracket_pos_label, pictograms_order, audio_pic = initialize_stimuli(window)

# Show instructions
show_message(window, begin)
window.flip()

# Run practice phase
run_trial_phase(practice_stimuli, 'practice', participant_info, practice_stimuli_path, fixation_cross, bracket_pic, nobracket_pic, window, nobracket_pos_label, bracket_pos_label, audio_pic)

# Show test start instructions
show_message(window, test)

# Run test phase
run_trial_phase(test_stimuli, 'test', participant_info, test_stimuli_path, fixation_cross, bracket_pic, nobracket_pic, window, nobracket_pos_label, bracket_pos_label, audio_pic)

# Show end screen
show_message(window, end)

# Close the window and exit
window.close()
core.quit()
