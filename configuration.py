# set-up
from psychopy import monitors, visual
import random
import os


# Setup paths
test_stimuli_path = 'stimuli/gated/test/'
practice_stimuli_path = 'stimuli/gated/practice/'
results_path = 'results/'
pics_path = 'pics/'
random_path = 'randomization_lists/'

# Results list
results = []


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


def initialize_stimuli(win):
    """
    Initialize textstim, pics and fixation cross.

    Parameters:
    win : A PsychoPy visual.Window object where the stimuli will be displayed.

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
    fixation_cross = visual.ShapeStim(win,
                                      vertices=((0, -0.13), (0, 0.13), (0, 0), (-0.09, 0), (0.09, 0)),
                                      lineWidth=15,
                                      closeShape=False,
                                      lineColor="black",
                                      name='fixation'
                                      )

    # Create pictograms
    bracket_pic = visual.ImageStim(win,
                                   image=pictograms_order[1],
                                   pos=positions[1]
                                   )

    nobracket_pic = visual.ImageStim(win,
                                     image=pictograms_order[0],
                                     pos=positions[0]
                                     )

    # Labels for the positions
    bracket_pos_label = labels[1]
    nobracket_pos_label = labels[0]

    return fixation_cross, bracket_pic, bracket_pos_label, nobracket_pic, nobracket_pos_label, pictograms_order
