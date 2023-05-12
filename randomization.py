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


def load_stimuli(path):
    """
    Loads stimuli files from a given directory.

    Parameters:
    path (str): Path to directory containing the stimuli files.

    Returns:
    list: A list of stimuli filenames.
    """
    # Use a list comprehension to get all '.wav' files in the directory
    return [f for f in os.listdir(path) if f.endswith('.wav')]


def group_stimuli(stimuli):
    """
    Groups stimuli by speaker.

    Parameters:
    stimuli (list): List of stimuli filenames.

    Returns:
    dict: A dictionary with speaker names as keys and lists of their stimuli as values.
    """
    groups = defaultdict(list)  # Use defaultdict to automatically create new keys as needed
    for stimulus in stimuli:
        speaker = stimulus[:2]  # Get speaker name from filename
        groups[speaker].append(stimulus)  # Add stimulus to the speaker's list

    return groups


def shuffle_stimuli(stimuli):
    """
    Shuffles stimuli in-place.

    Parameters:
    stimuli (list): List of stimuli filenames.

    Returns:
    list: List of shuffled stimuli filenames.
    """
    # Use random.shuffle for in-place shuffling
    random.shuffle(stimuli)
    return stimuli


def rearrange(stimuli, condition_limit=4, gate_limit=3):
    """
    Rearranges stimuli to avoid exceeding the condition limit or gate limit for consecutive stimuli.

    Parameters:
    stimuli (list): List of stimuli filenames.
    condition_limit (int): Maximum number of consecutive stimuli with the same condition.
    gate_limit (int): Maximum number of consecutive stimuli with the same gate.

    Returns:
    list: List of rearranged stimuli filenames.
    """
    rearranged = stimuli.copy()  # Create a copy of the stimuli list to rearrange

    # Stage 1: Handle condition limit
    for i in range(len(rearranged)):
        condition_count = 1  # Initialize condition count

        # Check subsequent stimuli for the same condition
        for j in range(i + 1, len(rearranged)):
            # If the current stimulus has the same condition as the previous, increment condition count
            if rearranged[j][-10:-7] == rearranged[i][-10:-7]:
                condition_count += 1
            else:
                # Reset condition count if the condition changes
                condition_count = 1

            # If the condition limit is reached, find a stimulus with a different condition to swap
            if condition_count > condition_limit:
                swapped = False  # Flag to track whether a suitable swap candidate was found
                for k in range(j + 1, len(rearranged)):
                    # If a stimulus with a different condition is found, swap it with the current stimulus
                    if rearranged[k][-10:-7] != rearranged[j][-10:-7]:
                        rearranged[j], rearranged[k] = rearranged[k], rearranged[j]
                        swapped = True
                        break  # Break out of the loop once a swap is made

                # If no suitable swap candidate is found, break out of the loop
                if not swapped:
                    break

    # Stage 2: Handle gate limit and special rule for gates 5, 6, and 7
    for i in range(len(rearranged)):
        gate_count = 1  # Initialize gate count
        prev_gate = int(rearranged[i][-5])  # Get the gate of the first stimulus

        # Check subsequent stimuli for the same gate
        for j in range(i + 1, len(rearranged)):
            curr_gate = int(rearranged[j][-5])  # Get the gate of the current stimulus
            if curr_gate == prev_gate:
                gate_count += 1  # If the current gate is the same as the previous, increment gate count
            else:
                gate_count = 1  # Reset gate count if the gate changes
                prev_gate = curr_gate

            # If the gate limit is reached or the special rule for gates 5, 6, and 7 is violated, find a stimulus with a different gate to swap
            if gate_count > gate_limit or (
                    prev_gate in {5, 6, 7} and curr_gate in {5, 6, 7} and rearranged[j][:2] == rearranged[i][:2] and
                    rearranged[j][-10:-7] == rearranged[i][-10:-7]):
                swapped = False  # Flag to track whether a suitable swap candidate was found
                for k in range(j + 1, len(rearranged)):
                    # If a stimulus with a different gate is found or a stimulus not violating the special rule is found, swap it with the current stimulus
                    if rearranged[k][-5] != rearranged[j][-5] or (
                            curr_gate in {5, 6, 7} and int(rearranged[k][-5]) not in {5, 6, 7}):
                        rearranged[j], rearranged[k] = rearranged[k], rearranged[j]
                        swapped = True
                        break  # Break out of the loop once a swap is made

                # If no suitable swap candidate is found, break out of the loop
                if not swapped:
                    break

    return rearranged


def create_randomized_stimuli(path):
    """
    Creates a randomized list of stimuli while maintaining certain constraints.

    Parameters:
    path (str): Path to directory containing the stimuli files.

    Returns:
    list: List of randomized stimuli filenames.
    """
    # Load and group stimuli by speaker
    stimuli = load_stimuli(path)
    random.seed(666)
    groups = group_stimuli(stimuli)

    randomized_stimuli = []
    # Shuffle and rearrange each speaker's stimuli
    for speaker, stimuli in groups.items():
        shuffled = shuffle_stimuli(stimuli)
        rearranged = rearrange(shuffled)
        randomized_stimuli.extend(rearranged)  # Add the rearranged stimuli to the final list

    return randomized_stimuli
