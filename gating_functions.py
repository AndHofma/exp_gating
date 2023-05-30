from psychopy import core, event, gui, visual
import datetime


def get_participant_info():
    """
    Open a dialogue box with 3 fields: current date and time, subject_ID and experiment name.
    Returns a dictionary with the entered information.
    """
    exp_data = {
        'experiment': 'gating_experiment',
        'cur_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'subject': 'subject_ID'
    }
    # Dialogue box to get participant information
    info_dialog = gui.DlgFromDict(dictionary=exp_data,
                                  title='Gating Experiment',
                                  fixed=['experiment','cur_date']
                                  )

    if info_dialog.OK:
        return exp_data
    else:
        core.quit()


def present_trial(win, fixation_cross, bracket_pic, nobracket_pic, gated_stimulus):
    """
    Present a trial with the given gated stimulus and pictograms order.

    Parameters:
    gated_stimulus (psychopy.sound.Sound): The gated stimulus sound.
    pictograms_order (list): The order of the pictograms ['no_bracket.png', 'bracket.png'] or vice versa.

    Returns:
    str: The response key ('left' or 'right').
    """
    fixation_cross.draw()
    gated_stimulus.play()
    win.flip()
    core.wait(gated_stimulus.getDuration()+0.2)  # wait for the duration of the sound + 200ms

    bracket_pic.draw()
    nobracket_pic.draw()
    win.flip()
    response_key = event.waitKeys(keyList=['left', 'right'])[0]
    win.flip()
    core.wait(2)

    return response_key


def show_message(win, message, wait_for_keypress=True, duration=1, text_height=0.1):
    """
    Show a message on the screen.

    Parameters:
    message (str): The message to display.
    wait_for_keypress (bool, optional): Whether to wait for a keypress. Defaults to True.
    duration (float, optional): Time in seconds to wait if wait_for_keypress is False. Defaults to 1.
    text_height (float, optional): The height of the text. Defaults to 0.1.
    """
    text_stim = visual.TextStim(win, text=message, wrapWidth=2, height=text_height, color="black")
    text_stim.draw()
    win.flip()
    if wait_for_keypress:
        event.waitKeys()
    else:
        core.wait(duration)


def get_stimulus_data(stimulus_file):
    """
    Extract properties from the stimulus file name.

    Args:
    stimulus_file (str): Name of the stimulus file.

    Returns:
    dict: Properties extracted from the stimulus file name.
    """
    return {
        'speaker': stimulus_file[:2],
        'gate': stimulus_file[-5],
        'name_stim': stimulus_file[14:19],
        'condition': stimulus_file[-10:-7]
    }


# Function to append a single result to the CSV file
def append_result_to_csv(result, practice_filename, test_filename, participant_info):
    """
    Appends the result of a trial to the appropriate CSV file (practice or test phase).

    Parameters:
    result (dict): A dictionary containing the data for a single trial.
    practice_filename (str): The path of the CSV file for storing practice phase results.
    test_filename (str): The path of the CSV file for storing test phase results.
    participant_info (dict): A dictionary containing the participant's information.

    The function writes the trial data, including phase, stimulus, response, accuracy, and timing info, to the CSV file.
    """
    output_filename = practice_filename if result['phase'] == 'practice' else test_filename

    with open(output_filename, 'a') as output_file:
        output_file.write(
            f"{participant_info['experiment']},"
            f"{participant_info['subject']},"
            f"{participant_info['cur_date']},"
            f"{result['trial']},"
            f"{result['phase']},"
            f"{result['stimulus']},"
            f"{result['response']},"
            f"{result['accuracy']},"
            f"{result['speaker']},"
            f"{result['gate']},"
            f"{result['name_stim']},"
            f"{result['condition']},"
            f"{result['bracket_pic_position']},"
            f"{result['nobracket_pic_position']},"
            f"{result['start_time']},"
            f"{result['end_time']},"
            f"{result['duration']}\n"
        )
