"""
Instructions for an understanding experiment.

This module contains strings that are displayed at the start, middle, and end
of an understanding experiment, guiding the participants through the process.
These instructions are displayed in the experiment window and participants
interact via keyboard.

Strings:
----------
begin: A string displayed at the beginning of the experiment. It introduces the
       experiment and instructs participants about the task, including how to
       interpret stimuli and how to respond using the keyboard.

test: A string displayed after practice trials. It indicates the beginning of
      the actual experiment and provides further details about its structure.

end: A string displayed at the end of the experiment, signalling its completion.

Usage:
----------
These strings are typically displayed in a psychopy.visual.Window object using
the psychopy.visual.TextStim method.

Example:
    >>> from psychopy import visual, core
    >>> win = visual.Window(size=[800, 600])
    >>> text = visual.TextStim(win, text=begin)
    >>> text.draw()
    >>> win.flip()
    >>> core.wait(5)
"""

# Instructions
begin = """
Willkommen zum Verständnis-Experiment \n
Sie hören unterschiedlich lange Aufnahmen der Ihnen bekannten Namenssequenzen.
Sie hören zum Beispiel: "Mimmi" oder Sie hören "Mimmi und Mo" etc..
Gleich danach sehen Sie zwei Piktogramme:
1. Drei Figuren zusammen - alle drei kommen gemeinsam.
2. Zwei Figuren zusammen, eine allein - zwei kommen gemeinsam, eine allein.
Bitte entscheiden Sie, welches Piktogramm am besten zur Sequenz passt.
Drücken Sie den Pfeil nach links auf der Tastatur, für das linke Piktogramm.
Drücken Sie den Pfeil nach rechts auf der Tastatur, für das rechte Piktogramm. \n  
Drücken Sie die Eingabetaste (Enter), um mit den Übungsbeispielen zu beginnen.
"""

test = """
Das waren die Übungsbeispiele. \n
Falls Sie noch Fragen haben, geben Sie bitte der Versuchsleiterin Bescheid.
Es gibt vier Blöcke und jeder Block dauert ca. 4 Minuten.  \n
Sie können nach jedem Block eine Pause machen, wenn Sie das wünschen. \n
Drücken Sie die Eingabetaste (Enter), um mit dem Experiment zu starten.
"""

end = """
Geschafft!\n
Drücken Sie die Eingabetaste (Enter), um das Experiment zu beenden.
"""
