# set-up
from psychopy import monitors, visual, gui, core
import random
import os
import datetime
import csv


# Setup paths
test_stimuli_path = 'stimuli/gated/test/'
practice_stimuli_path = 'stimuli/gated/practice/'
results_path = 'results/'
pics_path = 'pics/'
random_path = 'randomization_lists/'


# def create_window():
#     """
#    Create and initialize the experiment window.
#
#    Returns:
#    win: A PsychoPy visual.Window object for the experiment.
#   """
#    # Create a monitor object for the second screen
#    second_monitor = monitors.Monitor(name='EA273WMi')
#    # Set the appropriate settings for the second monitor
#    second_monitor.setSizePix((1920, 1080))  # Set the desired resolution of the second screen
#
#    # Create and return a window for the experiment on the second monitor
#    return visual.Window(monitor=second_monitor,  # Use the second monitor
#                         size=(1920, 1080),
#                         screen=1,  # Specify the index of the second screen (0 for the first screen, 1 for the second, etc.)
#                         allowGUI=True,
#                         fullscr=True,
#                         color=(255, 255, 255)
#                         )


# to use for testing on laptop
def create_window():
   """
   Create and initialize the experiment window.
   Returns:
   win : A PsychoPy visual.Window object for the experiment.
   """
   # Create a monitor object
   currentMonitor = monitors.Monitor(name='testMonitor')
   # Create and return a window for the experiment
   return visual.Window(monitors.Monitor.getSizePix(currentMonitor),
                        monitor="testMonitor",
                        allowGUI=True,
                        fullscr=True,
                        color=(255, 255, 255)
                        )


def initialize_stimuli(window):
    """
    Initialize textstim, pics and fixation cross.

    Parameters:
    window : A PsychoPy visual.Window object where the stimuli will be displayed.

    Returns:
    fixation_cross : A PsychoPy visual.ShapeStim object, a fixation cross.
    bracket_pic, nobracket_pic : PsychoPy visual.ImageStim objects, the pictograms.
    bracket_pos_label, nobracket_pos_label : Labels for the positions of the pictograms.
    pictograms_order : The order of the pictograms.
    """
    # Define the possible positions and corresponding labels for the pictograms
    positions = [(-0.5, 0), (0.5, 0)]  # left and right positions
    labels = ['left', 'right']  # corresponding labels

    # Randomize the order - this will be randomized between participants
    # Positions and labels are shuffled in the same order
    indices = list(range(len(positions)))
    random.shuffle(indices)
    positions = [positions[i] for i in indices]
    labels = [labels[i] for i in indices]

    # Pictograms order
    pictograms_order = [os.path.join(pics_path, 'no_bracket.png'), os.path.join(pics_path, 'bracket.png')]

    # Create fixation cross
    fixation_cross = visual.ShapeStim(window,
                                      vertices=((0, -0.13), (0, 0.13), (0, 0), (-0.09, 0), (0.09, 0)),
                                      lineWidth=15,
                                      closeShape=False,
                                      lineColor="black",
                                      name='fixation'
                                      )

    # Create pictograms
    bracket_pic = visual.ImageStim(window,
                                   image=pictograms_order[1],
                                   pos=positions[1]
                                   )

    nobracket_pic = visual.ImageStim(window,
                                     image=pictograms_order[0],
                                     pos=positions[0]
                                     )

    audio_pic = visual.ImageStim(window,
                                 image=pics_path + 'audio.png',
                                 pos=(0, 0),
                                 name='audio_pic')

    # Labels for the positions
    bracket_pos_label = labels[1]
    nobracket_pos_label = labels[0]

    return fixation_cross, bracket_pic, bracket_pos_label, nobracket_pic, nobracket_pos_label, pictograms_order, audio_pic


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


# Function to append a single result to the CSV file
def append_result_to_csv(result, output_filename):
    """
    Appends the result of a trial to the appropriate CSV file (practice or test phase).

    Parameters:
    result (dict): A dictionary containing the data for a single trial.
    output_filename (str): The path of the CSV file for storing phase results.

    The function writes the trial data, including phase, stimulus, response, accuracy, and timing info, to the CSV file.
    """
    # Check if file exists to write headers
    file_exists = os.path.isfile(output_filename)

    with open(output_filename, 'a') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=result.keys())
        if not file_exists:
            writer.writeheader()  # File doesn't exist yet, so write a header
        writer.writerow(result)