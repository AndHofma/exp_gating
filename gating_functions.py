# Import necessary libraries
from psychopy import prefs
# Set the audio library preference
prefs.hardware['audioLib'] = ['ptb', 'sounddevice', 'pygame', 'pyo']
# Now, import sound
from psychopy import sound, core, event, visual
import os
import datetime
import time
from configuration import append_result_to_csv
from randomization import get_stimulus_data
from psychopy.hardware import keyboard


def present_trial(window, fixation_cross, bracket_pic, nobracket_pic, gated_stimulus, kb, audio_pic):
    """
    Present a trial with the given gated stimulus and pictograms order.

    Parameters:
    gated_stimulus (psychopy.sound.Sound): The gated stimulus sound.
    pictograms_order (list): The order of the pictograms ['no_bracket.png', 'bracket.png'] or vice versa.

    Returns:
    str: The response key ('left' or 'right').
    float: The reaction time in seconds.
    """
    fixation_cross.draw()
    window.flip()
    core.wait(1.0)
    window.flip()

    audio_pic.draw()
    gated_stimulus.play()
    window.flip()

    core.wait(gated_stimulus.getDuration() + 0.5)  # wait for the duration of the sound + 500ms

    bracket_pic.draw()
    nobracket_pic.draw()
    window.flip()
    kb.clearEvents()  # clear the keyboard buffer
    kb.clock.reset()  # reset the clock
    keys = kb.waitKeys(keyList=['left', 'right'])  # wait until a key is pressed

    # Since waitKeys() waits for a key press, we can be sure that there is at least one key press
    response_key = keys[0].name  # get the name of the key that was pressed
    reaction_time = keys[0].rt  # get the reaction time

    window.flip()
    core.wait(1)

    return response_key, reaction_time


def show_message(window, message, wait_for_keypress=True, duration=1, text_height=0.1):
    """
    Show a message on the screen.

    Parameters:
    message (str): The message to display.
    wait_for_keypress (bool, optional): Whether to wait for a keypress. Defaults to True.
    duration (float, optional): Time in seconds to wait if wait_for_keypress is False. Defaults to 1.
    text_height (float, optional): The height of the text. Defaults to 0.1.
    """
    text_stim = visual.TextStim(window, text=message, wrapWidth=2, height=text_height, color="black")
    text_stim.draw()
    window.flip()
    if wait_for_keypress:
        event.waitKeys(keyList=['return'])
    else:
        core.wait(duration)


def run_trial_phase(stimuli_files, phase, participant_info, stimuli_path, fixation_cross, bracket_pic, nobracket_pic,
                    window, nobracket_pos_label, bracket_pos_label, audio_pic):

    results = []

    kb = keyboard.Keyboard()  # Initialize the keyboard

    # path setup results per participant
    # Define the path in results for each subject
    subj_path_results = os.path.join('results', participant_info['subject'])
    # Create the directory if it doesn't exist
    if not os.path.exists(subj_path_results):
        os.makedirs(subj_path_results)

    start_time = time.time()
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%H:%M:%S')
    trial_counter = 1
    block_counter = 1
    current_speaker = None

    for stimulus_file in stimuli_files:
        stimulus = get_stimulus_data(stimulus_file)

        if phase == 'test' and current_speaker and current_speaker != stimulus['speaker']:
            # Speaker has changed, therefore one block has ended
            remaining_blocks = 4 - block_counter
            show_message(window, f"Block {block_counter} geschafft - noch {remaining_blocks} Block(s) übrig. \n Drücken Sie die Eingabetaste (Enter), um weiterzumachen.")
            block_counter += 1
        current_speaker = stimulus['speaker']

        gated_stimulus = sound.Sound(os.path.join(stimuli_path, stimulus_file))
        response_key, reaction_time = present_trial(window, fixation_cross, bracket_pic, nobracket_pic, gated_stimulus, kb, audio_pic)

        # Determine correct answer and accuracy
        correct_answer = 'left' if (stimulus['condition'] == 'nob' and nobracket_pos_label == 'left') or (
                    stimulus['condition'] == 'bra' and bracket_pos_label == 'left') else 'right'
        accuracy = 1 if response_key == correct_answer else 0

        if phase == 'practice':
            feedback = "Richtig!" if response_key == correct_answer else "Falsch!"
            show_message(window, feedback, wait_for_keypress=False, text_height=0.3)

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
            'block': block_counter,
            'phase': phase,
            'stimulus': stimulus_file,
            'response': response_key,
            'reaction_time': reaction_time,
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

        # Increment trial counter
        trial_counter += 1

    # generate the base_filename based on task_name and phase
    output_filename = f"{subj_path_results}/{phase}_{participant_info['experiment']}_{participant_info['subject']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    for result in results:
        append_result_to_csv(result, output_filename)

    return results
