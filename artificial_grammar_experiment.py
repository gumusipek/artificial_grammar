#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File    :   artificial_grammar_experiment.py
@Time    :   22024/12/25 16:35
@Author  :   Stine van Geet, Ipek Gumus
@Version :   Final
@Desc    :   Code for an artificial grammar learning experiment. This file is to be used prior to the analysis file, located in the same folder.
             The experiment consists of two main phases: a training phase and a test phase.

             During the **training phase**, participants are presented with nonsense words generated using a grammatical rule. Participants are tasked with
             typing each word exactly as presented. If the participant's response is incorrect, the word is shown again until typed correctly.

             During the **test phase**, participants are shown a new set of words. These words either adhere to the same grammatical rule as in the training phase
             or violate it. Participants must decide whether each word conforms to the previously learned rule.

             The main body code consists of the following parts:
             1. Initialization of the experiment and setup
             2. Participant identification and directory creation
             3. Experiment instructions screens
             4. Training phase: participants type the presented nonsense words, receiving feedback for correctness
             5. Test phase: participants classify new words as grammatical or ungrammatical
             6. Exit screen: participant is notified of the experiment's completion

             Results: A folder is created for each participant, containing three separate files:
             - **Participant information results**: Includes experiment type and participants' ID, gender, age, native language.
             - **Training phase results**: Includes accuracy, response times, and trial-level feedback.
             - **Test phase results**: Includes accuracy, response times, and classification decisions for each word.

             Data analysis can be conducted using the accompanying analysis file, located in the same folder.

             References:
             Brown, J., Aczel, B., Jiménez, L., Kaufman, S. B., & Grant, K. P. (2010). Intact implicit learning in autism spectrum conditions. Quarterly Journal of Experimental Psychology, 63(9), 1789–1812. https://doi.org/10.1080/17470210903536910 
    
"""
# %% NECESSARY MODULES

#import the submodules from psychopy
from psychopy import visual, core, event, gui
import random, os, time
import pandas as pd

# %% PROJECT SETTINGS

full = True #modify this to determine showing the experiment as full screen or not. Set True if you would like to run the experiment on full screen.

#get the current timestamp
timestamp = time.strftime("%Y%m%d")

#create a file to collect the data from the participants
os.makedirs("data", exist_ok = True) 

# %% COLLECT PERSONAL INFORMATION BEFORE START OF THE EXPERIMENT

#define participant information that we would like to receive
participant_info = {
    "Test": ["Pilot", "Experimental"],
    "ID": "",
    "Age": ["<18", "18-24", "25-34", "35-44", "45+"],
    "Gender": ["Male", "Female", "Other", "Prefer not to say"],
    "Native Language": ["Dutch", "French", "English", "German", "Other"]
}
field_order = list(participant_info.keys())

#create the first dialog box
dlg_info = gui.DlgFromDict(
    dictionary=participant_info,
    title="Participant Information",
    order = field_order
)

#check if the participant clicked OK
if dlg_info.OK:
    #if "Other" is selected for native language, ask for details
    if participant_info["Native Language"] == "Other":
        #ask for their native language
        other_language_dlg = gui.Dlg(title="Additional Information")
        other_language_dlg.addField("Please specify your native language:")
        other_language_input = other_language_dlg.show()
        
        if other_language_dlg.OK:
            #add the additional input to participant_info
            participant_info["Native Language"] = other_language_input[0]
        else:
            print("User cancelled during additional input.")
            core.quit()
    
    #print the final participant info
    print("Participant info:", participant_info)
else:
    print("User cancelled.")
    core.quit()

#create a new folder with the participant ID and timestamp
participant_folder = os.path.join("data", f"{participant_info['ID']}_{timestamp}")
os.makedirs(participant_folder, exist_ok=True)
#store the personal information
participant_info_df = pd.DataFrame([participant_info])
participant_info_df.to_csv(os.path.join(participant_folder, f'{participant_info["ID"]}_participant_info.csv'), index=False)

# %% FUNCTION - to be used on the main code later

#create a function to display the texts
def display_text(enter_text):
    """
    Creates and returns a PsychoPy TextStim object to display the given text on the screen.

    Parameters
    ----------
    enter_text : str
        The text string to be displayed in the PsychoPy window.

    Returns
    -------
    demonstrate : visual.TextStim
        A TextStim object that can be drawn to the window.

    """
    text_height = 40 #adjust the value according to the computer screen
    wrap_width = 1200 #adjust the value according to the computer screen
    demonstrate = visual.TextStim(
        win,
        text = enter_text,
        color = "black",
        height = text_height,
        wrapWidth = wrap_width
    )
    demonstrate.draw()
    win.flip()

# %% INITIALISATION

#import stimuli for training phase
with open ('training_phase.txt') as file:
    content_training_phase = file.readlines()
    
#store the training stimuli in a list
training_stimuli_list = [letter_string.strip() for letter_string in content_training_phase]

#load the text file of test phase stimuli into a DataFrame
#rationale of using DataFrame for this step unlike trial phase is stimuli file of test phase includes grammar rule per stimulus and we would like to store this information and use on later steps.
test_stimuli_df = pd.read_csv(
    'test_phase.txt',
    delim_whitespace = True,
    header = None,
    names = ['test stimulus', 'grammar rule']
    )
#shuffle the test stimuli DataFrame rows
test_stimuli_df = test_stimuli_df.sample(frac = 1, ignore_index=True)

#load the trianing and test phase instructions
with open('Training_Phase_Instructions.txt', 'r') as file:
    training_phase_instructions = file.read()
    
with open('Test_Phase_Instructions.txt', 'r') as file:
    test_phase_instructions = file.read()

#create a window
win = visual.Window(fullscr = full, color= "white", units = 'pix' )

#create an empty list to collect participants' results
results_training_phase = []
results_test_phase = []

#initialise the clock
clock = core.Clock()

# %% TRAINING PHASE

#display instructions training phase
display_text(training_phase_instructions)
event.waitKeys(keyList=["space"])

#Make the excercise go twice
for block in range(1,3):
    random.shuffle(training_stimuli_list)
    
    #presenting word and evaluate reproduction of participant
    for training_stimulus in training_stimuli_list:
        
        #reset value to start again with a stimulus
        repeat = True
        
        #repeat when participant was wrong
        while repeat:
           
           #show the stimulus word for 4 seconds 
            display_text("")
            display_text(training_stimulus)
            core.wait(4)
        
            #resetting values
            trial=[]
            participant_response = ''
            response = True
            
            accuracy = 0
            RT = None         
            
            event.clearEvents()
            clock.reset()
            
            #register pressed keys and time for RT
            while response == True:
                keys = event.getKeys(timeStamped = clock)
            
                #evaluate when special keys, to keep their function, registrate RT 
                for key, time_ in keys:
                    if key == 'return':
                        RT = time_
                        response = False
                    elif key == 'backspace':
                        if trial:
                            trial.pop()
                            
                    #add typed letters to the list in uppercase
                    elif len(key) == 1:  
                        trial.append(key.upper())
                        
                #make a string of the list and display
                participant_response = ''.join(trial)
                display_text(participant_response)
    
            #evaluate if participant was correct, if so go to next word
            if training_stimulus == participant_response.strip():
                accuracy = 1
                repeat = False
            else:   #participant is not correct, show feedback and show the word again
                accuracy = 0
                display_text("INCORRECT!\n\nPLEASE TRY AGAIN.")
                core.wait(2)               
            
            #store the necessary data
            results_training_phase.append({
                "block": block,
                "stimulus": training_stimulus,
                "participant response": participant_response,
                "accuracy": accuracy,
                "RT": RT        
            })
            
            #create a csv file to store reaction time and accuray of responses
            training_df = pd.DataFrame(results_training_phase)
            training_df.to_csv(os.path.join(participant_folder, f'{participant_info["ID"]}_training_phase.csv'), index=False)
            
#end phrase of the training phase
display_text("The training phase is complete.\nPlease press the SPACE BAR when you are ready to proceed to the next part of the experiment.")
event.waitKeys(keyList=["space"])

# %% TEST PHASE
  
#test instruction screen
display_text(test_phase_instructions)
event.waitKeys(keyList=["space"])

key_options = ["J","F"] 

#iterate through each stimulus in the DataFrame
for index, row in test_stimuli_df.iterrows():
    test_stimulus = row["test stimulus"]
    grammar_rule = row["grammar rule"]
    
    #display stimulus
    display_text(test_stimulus)
    
    #start the clock to track the time for max 6 seconds
    clock.reset()
    
    #set default values for reaction time, pressed key and accuracy
    key_pressed = None
    RT = None
    accuracy = 0
    
    #accept only J or F key responses
    #wait for a key response at most for 6 seconds
    key_response = event.waitKeys(keyList = key_options + [k.lower() for k in key_options], maxWait = 6, timeStamped = clock)

    #collect the accuracy of the key response and reaction time (RT)    
    if grammar_rule == 0:
        correct_key = key_options[0]
        if key_response:
            key_pressed, RT = key_response[0]
            key_pressed = key_pressed.upper()
            if key_pressed == key_options[0]:
                accuracy = 1   
    else:
        correct_key = key_options[1]
        if key_response:
            key_pressed, RT = key_response[0]
            key_pressed = key_pressed.upper()
            if key_pressed == key_options[1]:
                accuracy = 1
    
    #store the necessary data
    results_test_phase.append({
        "stimulus": test_stimulus,
        "grammar_rule": grammar_rule,
        "key_pressed": key_pressed,
        "correct_key": correct_key,
        "accuracy": accuracy,
        "RT": RT        
    })

#create a csv file to store reaction time and accuray of responses
test_df = pd.DataFrame(results_test_phase)
test_df.to_csv(os.path.join(participant_folder, f'{participant_info["ID"]}_test_phase.csv'), index=False)

# %% END OF THE EXPERIMENT

#end of the experiment
display_text(enter_text= "End of the experiment!\n\n Thank you for your participation.")
event.waitKeys(keyList=["space"])

#close the window after all the stimuli are shown and the experiment is ended
win.close()
core.quit()
