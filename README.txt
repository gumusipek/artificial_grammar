Artificial Grammar Learning Experiment

Description

This project consists of an Artificial Grammar Learning (AGL) Experiment, designed to investigate participants’ ability to learn and identify grammatical rules in nonsense word sequences. The experiment includes two phases: a Training Phase and a Test Phase, with results saved in structured CSV files for subsequent analysis.

Experiment Phases
1.Training Phase:
•Participants are presented with nonsense words following a grammatical rule.
•They type the words as presented. Incorrect responses result in repetition until the word is typed correctly.
•Accuracy and response times are recorded.

2.Test Phase:
•Participants evaluate new nonsense words, classifying them as grammatical or ungrammatical.
•Responses (key presses), accuracy, and reaction times are recorded.

Files

Experiment Code
•artificial_grammar_experiment.py: Main script for running the experiment.

Stimuli Files
•training_phase.txt: List of nonsense words for the training phase.
•test_phase.txt: List of nonsense words for the test phase, along with their grammatical status.

Instruction Files
•Training_Phase_Instructions.txt: Text for training phase instructions.
•Test_Phase_Instructions.txt: Text for test phase instructions.

Analysis Code
•analysis_code.py: Script for analyzing the data collected during the experiment.

Output Files
•Results are saved in a data folder, with one subfolder per participant containing:
1.participant_info.csv: Participant demographics and experiment type.
2.training_phase.csv: Training phase data (accuracy, response times, feedback).
3.test_phase.csv: Test phase data (response classifications, reaction times, accuracy).

Running the Experiment
1.Preparation:
•Ensure all required Python packages are installed (e.g., psychopy, pandas).
•Place all necessary files (.txt files and .py scripts) in the same folder.
2.Execution:
•Run artificial_grammar_experiment.py to start the experiment.
•Follow on-screen instructions to complete the training and test phases.
3.Output:
•Results are automatically saved in the data folder under a timestamped subfolder for each participant.

Analysis
1.Purpose:
•Evaluate participants’ implicit learning of grammatical rules.
•Compare reaction times and accuracy between grammatical and ungrammatical stimuli.
2.Steps:
•Run analysis_code.py to process and visualize the data.
•Check generated statistics, plots, and comparisons for insights.

Credits

Authors: Stine van Geet, Ipek Gumus

Contact:
For any issues or questions, please reach out to the authors.

References:
Brown, J., Aczel, B., Jiménez, L., Kaufman, S. B., & Grant, K. P. (2010). Intact implicit learning in autism spectrum conditions. Quarterly Journal of Experimental Psychology, 63(9), 1789–1812. https://doi.org/10.1080/17470210903536910