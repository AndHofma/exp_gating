"""
gating_configuration.py

This module contains all the setup paths and several important functions required to run a gating experiment.

It initializes the experiment window using PsychoPy and sets up the necessary visual stimuli, such as fixation cross
and pictograms.

It also provides a function to get participant information via a dialog box, including the date and time of the
experiment, subjectID and the experiment name.

Finally, it includes a function to write the results of a single trial to a CSV file, creating the file if it doesn't
exist and appending to it if it does.

Setup Paths:
    - test_stimuli_path: Path to the test stimuli.
    - practice_stimuli_path: Path to the practice stimuli.
    - results_path: Path to the directory where results are stored.
    - pics_path: Path to the directory where pictures are stored.
    - random_path: Path to the directory where randomization lists are stored.

Functions:
    - create_window: Creates and initializes the experiment window.
    - initialize_stimuli: Initializes textstim, pics, and fixation cross.
    - get_participant_info: Opens a dialog box to get participant information.
    - append_result_to_csv: Appends the result of a trial to a CSV file.
"""

from psychopy import monitors, visual, gui, core
import random
import os
import datetime
import sys


def resource_path(relative_path):
    """Determine and return the absolute path to the resource."""

    # Check if the application is frozen (compiled)
    if getattr(sys, 'frozen', False):
        # If we're running as a bundled exe, set the base path as one level above the executable
        base_path = os.path.join(os.path.dirname(sys.executable), "..")
    else:
        # If we're running in a normal Python environment
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)


# Setup paths
test_stimuli_path = resource_path('stimuli/gated/test/')
practice_stimuli_path = resource_path('stimuli/gated/practice/')
results_path = resource_path('results/')
pics_path = resource_path('pics/')
random_path = resource_path('randomization/')


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
    current_monitor = monitors.Monitor(name='testMonitor')

    # Create and return a window for the experiment
    return visual.Window(monitors.Monitor.getSizePix(current_monitor),
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

    return fixation_cross, bracket_pic, bracket_pos_label, nobracket_pic, nobracket_pos_label, pictograms_order, \
        audio_pic


def get_participant_info():
    """
    Open a dialogue box with 3 fields: current date and time, subjectID and experiment name.
    Returns a dictionary with the entered information.
    """
    exp_data = {
        'experiment': 'gating_experiment',
        'cur_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        'subject': 'subjectID'
    }
    # Dialogue box to get participant information
    info_dialog = gui.DlgFromDict(dictionary=exp_data,
                                  title='Gating Experiment',
                                  fixed=['experiment', 'cur_date']
                                  )

    if info_dialog.OK:
        return exp_data
    else:
        core.quit()


# Function to append a single result to the CSV file
def append_result_to_csv(writer, result, file_exists, output_file):
    """
    Appends the result of a trial to the appropriate CSV file (practice or test phase).

    Parameters:
    writer (csv.DictWriter): The CSV writer object to use for writing.
    result (dict): A dictionary containing the data for a single trial.
    file_exists (bool): Whether the CSV file exists already.
    output_file (File object): The CSV file object to use for writing.

    The function writes the trial data, including phase, stimulus, response, accuracy, and timing info, to the CSV file.
    """
    if not file_exists:
        writer.writeheader()  # File doesn't exist yet, so write a header
    writer.writerow(result)
    output_file.flush()  # Flush Python's write buffer
    os.fsync(output_file.fileno())  # Tell the OS to flush its buffers to disk
