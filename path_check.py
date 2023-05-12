import os


def check_config_paths(test_stimuli_path, practice_stimuli_path, results_path, pics_path, random_path):
    """
        Function checks the existence of specific directories and raises
        exceptions with appropriate error messages if any of the directories are not found.
    """
    # Check if the input directory for test stimuli exists
    if not os.path.exists(test_stimuli_path):
        # Raise exception if not
        raise Exception("No input folder detected. Please make sure that "
                        "'test_stimuli_path' is correctly set in the configurations")
    # Check if the input directory for test stimuli exists
    if not os.path.exists(practice_stimuli_path):
        # Raise exception if not
        raise Exception("No input folder detected. Please make sure that "
                        "'practice_stimuli_path' is correctly set in the configurations")
    # Check if the pics directory exists
    if not os.path.exists(pics_path):
        # Raise exception if not
        raise Exception("No pics folder detected. Please make sure that "
                        "'pics_path' is correctly set in the configurations")
    # Check if the output directory exists, if not, create it
    if not os.path.exists(results_path):
        os.mkdir(results_path)
    # Check if the path to randomization files exists, if not, create it
    if not os.path.exists(random_path):
        os.mkdir(random_path)
