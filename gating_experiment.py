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

import os
import datetime
import time
import pickle
import csv
from psychopy import core, sound
from path_check import check_config_paths
from configuration import create_window, initialize_stimuli, practice_stimuli_path, test_stimuli_path, results_path, pics_path, random_path, results
from gating_functions import get_participant_info, present_trial, show_message, append_result_to_csv, get_stimulus_data
from instructions import begin, test, halftime, end
from randomization import load_stimuli, create_randomized_stimuli

# Check if input and output paths exist
check_config_paths(test_stimuli_path, practice_stimuli_path, results_path, pics_path, random_path)  # make sure that in and out paths exist

randomized_practice_file = os.path.join(random_path, 'randomized_practice_stimuli.pkl')
randomized_test_file = os.path.join(random_path, 'randomized_test_stimuli.pkl')

practice_stimuli = load_stimuli(practice_stimuli_path)

# Load or generate randomized practice stimuli
if os.path.isfile(randomized_practice_file):
    with open(randomized_practice_file, 'rb') as f:
        randomized_practice_stimuli = pickle.load(f)
else:
    randomized_practice_stimuli = create_randomized_stimuli(practice_stimuli_path)
    with open(randomized_practice_file, 'wb') as f:
        pickle.dump(randomized_practice_stimuli, f)

# Write the data to a CSV file if it is not there
if not os.path.isfile(os.path.join(random_path, 'randomized_practice_stimuli.csv')):
    with open(os.path.join(random_path, 'randomized_practice_stimuli.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        for row in randomized_practice_stimuli:
            writer.writerow([row])  # write each item in a new row

# Convert both practice lists to sets and compare
original_practice_set = set(practice_stimuli)
randomized_practice_set = set(randomized_practice_stimuli)
assert original_practice_set == randomized_practice_set, "The original and randomized practice stimuli are not the same"

test_stimuli = load_stimuli(test_stimuli_path)

# Load or generate randomized test stimuli
if os.path.isfile(randomized_test_file):
    with open(randomized_test_file, 'rb') as f:
        randomized_test_stimuli = pickle.load(f)
else:
    randomized_test_stimuli = create_randomized_stimuli(test_stimuli_path)
    with open(randomized_test_file, 'wb') as f:
        pickle.dump(randomized_test_stimuli, f)

# Write the data to a CSV file
if not os.path.isfile(os.path.join(random_path, 'randomized_test_stimuli.csv')):
    with open(os.path.join(random_path, 'randomized_test_stimuli.csv'), 'w', newline='') as f:
        writer = csv.writer(f)
        for row in randomized_test_stimuli:
            writer.writerow([row])  # write each item in a new row

# Convert both test lists to sets and compare
original_test_set = set(test_stimuli)
randomized_test_set = set(randomized_test_stimuli)
assert original_test_set == randomized_test_set, "The original and randomized test stimuli are not the same"


# Get participant information
participant_info = get_participant_info()
# Create the window
win = create_window()

# Initialize screen
fixation_cross, bracket_pic, bracket_pos_label, nobracket_pic, nobracket_pos_label, pictograms_order = initialize_stimuli(win)

# path setup - results per participant
# Define the path in results for each subject
subj_path_results = os.path.join('results', participant_info['subject'])
# Create the directory if it doesn't exist
if not os.path.exists(subj_path_results):
    os.makedirs(subj_path_results)
# Create the output files with headers and save them in results/
practice_output_filename = os.path.join(subj_path_results,
                                        f"gating_practice_results_{participant_info['subject']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
test_output_filename = os.path.join(subj_path_results,
                                    f"gating_test_results_{participant_info['subject']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

for output_file in [practice_output_filename, test_output_filename]:
    with open(output_file, 'w') as file:
        file.write(
            'experiment,subject_ID,date,trial,phase,stimulus,response,accuracy,speaker,gate,name_stim,condition,bracket_pic_position,nobracket_pic_position,start_time,end_time,duration \n'
        )

# Show instructions
show_message(win, begin)
win.flip()

start_time = time.time()
start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%H:%M:%S')

trial_counter = 1
# Present practice phase
for stimulus_file in randomized_practice_stimuli:
    stimulus = get_stimulus_data(stimulus_file)
    gated_stimulus = sound.Sound(os.path.join(practice_stimuli_path, stimulus_file))
    response_key = present_trial(win, fixation_cross, bracket_pic, nobracket_pic, gated_stimulus)

    # Provide feedback
    correct_answer = 'left' if (stimulus_file[-10:-7] == 'nob' and nobracket_pos_label == 'left') or (stimulus_file[-10:-7] == 'bra' and bracket_pos_label == 'left') else 'right'
    accuracy = 1 if response_key == correct_answer else 0
    feedback = "Richtig!" if response_key == correct_answer else "Falsch!"
    show_message(win, feedback, wait_for_keypress=False)

    # Record end time and duration
    end_time = time.time()
    end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
    duration = end_time - start_time
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

    # Store trial data
    results.append({
        'experiment': participant_info['experiment'],
        'subject_ID': participant_info['subject'],
        'date': participant_info['cur_date'],
        'trial': trial_counter,
        'phase': 'practice',
        'stimulus': stimulus_file,
        'response': response_key,
        'accuracy': accuracy,
        'speaker': stimulus['speaker'],
        'gate': stimulus['gate'],
        'name_stim': stimulus['name_stim'],
        'condition': stimulus['condition'],
        'bracket_pic_position': bracket_pos_label,
        'nobracket_pic_position': nobracket_pos_label,
        'start_time': start_time_str,
        'end_time': end_time_str,
        'duration': duration_str
    })
    append_result_to_csv(results[-1], practice_output_filename, test_output_filename, participant_info)

    # Increment trial counter
    trial_counter += 1

# Show test start instructions
show_message(win, test)

trial_counter = 1
# Present main experiment
for stimulus_file in randomized_test_stimuli:
    stimulus = get_stimulus_data(stimulus_file)

    gated_stimulus = sound.Sound(os.path.join(test_stimuli_path, stimulus_file))
    response_key = present_trial(win, fixation_cross, bracket_pic, nobracket_pic, gated_stimulus)

    # Determine accuracy
    correct_answer = 'left' if (stimulus['condition'] == 'nob' and nobracket_pos_label == 'left') or (stimulus['condition'] == 'bra' and bracket_pos_label == 'left') else 'right'
    accuracy = 1 if response_key == correct_answer else 0

    # Record end time and duration
    end_time = time.time()
    end_time_str = datetime.datetime.fromtimestamp(end_time).strftime('%H:%M:%S')
    duration = end_time - start_time
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    duration_str = '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))

    # Store trial data
    results.append({
        'experiment': participant_info['experiment'],
        'subject_ID': participant_info['subject'],
        'date': participant_info['cur_date'],
        'trial': trial_counter,
        'phase': 'test',
        'stimulus': stimulus_file,
        'response': response_key,
        'accuracy': accuracy,
        'speaker': stimulus['speaker'],
        'gate': stimulus['gate'],
        'name_stim': stimulus['name_stim'],
        'condition': stimulus['condition'],
        'bracket_pic_position': bracket_pos_label,
        'nobracket_pic_position': nobracket_pos_label,
        'start_time': start_time_str,
        'end_time': end_time_str,
        'duration': duration_str
    })
    append_result_to_csv(results[-1], practice_output_filename, test_output_filename, participant_info)

    # Increment trial counter
    trial_counter += 1

    # Show break screen after half of the trials
    if trial_counter == (len(randomized_test_stimuli) // 2) + 1:
        show_message(win, halftime)

# Show end screen
show_message(win, end)

# Close the window and exit
win.close()
core.quit()
