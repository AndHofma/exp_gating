"""
Randomization:
1. Separate the stimuli into groups by speaker.
2. Shuffle the list of speakers.
3. For each speaker, separate their stimuli into groups by condition (bra and nob).
4. For each condition, separate their stimuli into groups by gate.
5. For each gate group, shuffle the stimuli.
6. Reassemble the stimuli for each condition, ensuring that no condition is repeated more than four times consecutively.
7. Reassemble the stimuli for each speaker, ensuring that no gate is repeated more than three times consecutively.

The constraints are handled in two stages.
First, make sure that no more than four stimuli with the same condition appear consecutively.
Then, ensure that no more than three stimuli with the same gate number appear consecutively.
Additionally, add a condition to ensure that gate 5, 6, and 7 stimuli do not appear adjacent to each other
if they are from the same speaker with the same name and condition.
"""

import os
import random
from collections import defaultdict
import csv


def load_stimuli(stimuli_path):
    """
    Loads stimuli files from a given directory.

    Parameters:
    stimuli_path (str): Path to directory containing the stimuli files.

    Returns:
    list: A list of stimuli filenames.
    """
    # Use a list comprehension to get all '.wav' files in the directory
    return [f for f in os.listdir(stimuli_path) if f.endswith('.wav')]


def randomize_stimuli(stimuli_files, practice_files=None):
    """
    Randomize a list of stimuli files given certain constraints.

    Args:
    stimuli_files (list of str): List of stimuli file names.

    Returns:
    list of str: Randomized list of stimuli files.
    """
    # If practice_files is provided, just shuffle them
    if practice_files is not None:
        random.shuffle(stimuli_files)
        randomized_stimuli = stimuli_files

    else:
        # Extract stimulus data for each file
        stimulus_data = [get_stimulus_data(file) for file in stimuli_files]

        # Group by speaker
        speakers = defaultdict(list)
        for data in stimulus_data:
            speakers[data['speaker']].append(data)

        # Randomize order of speakers
        speaker_order = list(speakers.keys())
        random.shuffle(speaker_order)

        # Initialize list to store the final order of stimuli
        randomized_stimuli_data = []

        # Iterate over speakers in randomized order
        for speaker in speaker_order:
            # Separate out gate 7 stimuli
            gate7_stimuli = [data for data in speakers[speaker] if data['gate'] == '7']
            other_stimuli = [data for data in speakers[speaker] if data['gate'] != '7']

            # Randomly order other stimuli with constraints
            other_stimuli_ordered = constraint_randomization(other_stimuli)

            # Randomly order gate 7 stimuli with constraints
            gate7_stimuli_ordered = constraint_randomization(gate7_stimuli)

            # Append stimuli to final list
            randomized_stimuli_data.extend(other_stimuli_ordered + gate7_stimuli_ordered)

        # Now, extract the filenames from the data
        randomized_stimuli = [data['filename'] for data in randomized_stimuli_data]

    return randomized_stimuli


def constraint_randomization(stimuli_files):
    """
    Apply constraint randomization: Not more than 3 of the same condition,
    name_stim or gate should be played.

    Args:
    stimuli (list of dict): List of stimuli data.

    Returns:
    list of dict: Randomized list of stimuli data.
    """
    stimuli_copy = stimuli_files.copy()
    random.shuffle(stimuli_copy)

    randomized_stimuli = []
    while stimuli_copy:
        valid_stimulus_found = False
        for stimulus in stimuli_copy:
            if (
                sum(stim['condition'] == stimulus['condition'] for stim in randomized_stimuli) < 4 and
                sum(stim['name_stim'] == stimulus['name_stim'] for stim in randomized_stimuli) < 2 and
                sum(stim['gate'] == stimulus['gate'] for stim in randomized_stimuli) < 4
            ):
                randomized_stimuli.append(stimulus)
                stimuli_copy.remove(stimulus)
                valid_stimulus_found = True
                break
        if not valid_stimulus_found:
            print(
                "Warning: Constraints cannot be satisfied for remaining stimuli. Adding remaining stimuli in random order.")
            randomized_stimuli.extend(stimuli_copy)
            break
    return randomized_stimuli


def save_randomized_stimuli(randomized_stimuli, participant_info):
    """
    Save randomized stimuli as a csv file for a participant.

    Args:
    randomized_stimuli (list of str): List of randomized stimuli file names.
    participant_info (dict): Participant information from get_participant_info().
    """
    # Create a directory for this participant if it doesn't exist
    directory = os.path.join('randomization_lists', participant_info['subject'])
    os.makedirs(directory, exist_ok=True)

    # Define file path
    filename = f"{participant_info['subject']}_{participant_info['cur_date'].replace(':', '-').replace(' ', '_')}_randomized_gating_stimuli.csv"
    filepath = os.path.join(directory, filename)

    # Write csv file
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filename"])  # header
        for row in randomized_stimuli:
            writer.writerow([row])
    print(f"Saved randomized stimuli to {filepath}")


def load_and_randomize(stimuli_path, participant_info):
    """
    Load stimuli files from a directory, randomize them,
    get participant info and save the randomized stimuli.

    Args:
    stimuli_path (str): Path to directory containing the stimuli files.
    """
    # Load stimuli files
    stimuli_files = load_stimuli(stimuli_path)

    # Randomize stimuli
    randomized_stimuli = randomize_stimuli(stimuli_files)

    # Save randomized stimuli
    save_randomized_stimuli(randomized_stimuli, participant_info)

    return randomized_stimuli


def get_stimulus_data(stimulus_file):
    """
    Extract properties from the stimulus file name.

    Args:
    stimulus_file (str): Name of the stimulus file.

    Returns:
    dict: Properties extracted from the stimulus file name.
    """
    return {
        'filename': stimulus_file,  # Include the filename in the data
        'speaker': stimulus_file[:2],
        'gate': stimulus_file[-5],
        'name_stim': stimulus_file[14:19],
        'condition': stimulus_file[-10:-7]
    }
