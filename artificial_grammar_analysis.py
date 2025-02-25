#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@File    :   artificial_grammar_analysis.py
@Time    :   2024/12/25
@Author  :   Ipek Gumus, Stine van Geet
@Version :   Final
@Desc    :   Analysis script for the artificial grammar learning experiment. This file processes and analyzes data collected during 
             the training and test phases of the experiment, as generated by the associated experiment script.

             The main body of this code consists of the following parts:
             1. Data loading: Reads participant data stored in the 'data' folder. Each participant's data is divided into training and test phases.
             2. Individual-level analysis:
                - Computes accuracy and reaction times (RT) for each participant during both phases.
                - Produces visualizations for each participant, including:
                  - Accuracy trend over trials
                  - Reaction time trend over trials
             3. Group-level analysis:
                - Aggregates data across all participants.
                - Analyzes overall trends in accuracy and RT for both training and test phases.
                - Generates group-level visualizations, such as:
                  - Average accuracy per trial
                  - Reaction time distributions
             4. Output: Saves processed data, visualizations, and summary statistics for further reporting or publication.

             Prerequisites:
             - All participant data must be stored in a folder named 'data' with separate subfolders for training and test phase results.
             - Required Python libraries: pandas, matplotlib, seaborn.

"""
# %% IMPORT NECESSARY MODULES
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %% LOAD DATA
# Initialize empty DataFrames for storing combined data
all_training_data = pd.DataFrame()
all_test_data = pd.DataFrame()

# Base directory where participant folders are stored
base_dir = "data"

# Walk through the directory and gather training and test data
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith("_training_phase.csv"):
            training_file_path = os.path.join(root, file)
            training_data = pd.read_csv(training_file_path)
            
            # Add participant ID based on folder name
            participant_id = os.path.basename(root)
            training_data["Participant_ID"] = participant_id
            
            all_training_data = pd.concat([all_training_data, training_data], ignore_index=True)

        elif file.endswith("_test_phase.csv"):
            test_file_path = os.path.join(root, file)
            test_data = pd.read_csv(test_file_path)
            
            # Add participant ID based on folder name
            participant_id = os.path.basename(root)
            test_data["Participant_ID"] = participant_id
            
            all_test_data = pd.concat([all_test_data, test_data], ignore_index=True)

# %% INDIVIDUAL-LEVEL ANALYSIS
# Analyze each participant's performance in training and test phases
for participant_id in all_training_data["Participant_ID"].unique():
    participant_training_data = all_training_data[all_training_data["Participant_ID"] == participant_id]
    participant_test_data = all_test_data[all_test_data["Participant_ID"] == participant_id]
    
    # Training Phase: Accuracy and Reaction Time
    training_accuracy = participant_training_data["accuracy"].mean() * 100
    training_rt_correct = participant_training_data[participant_training_data["accuracy"] == 1]["RT"].mean()
    print(f"Participant {participant_id} Training Phase Accuracy: {training_accuracy:.2f}%")
    print(f"Participant {participant_id} Training Phase RT (Correct): {training_rt_correct:.2f} seconds")
    
    # Test Phase: Accuracy and Reaction Time
    test_accuracy = participant_test_data["accuracy"].mean() * 100
    test_rt_correct = participant_test_data[participant_test_data["accuracy"] == 1]["RT"].mean()
    print(f"Participant {participant_id} Test Phase Accuracy: {test_accuracy:.2f}%")
    print(f"Participant {participant_id} Test Phase RT (Correct): {test_rt_correct:.2f} seconds")
    
    # Plot Individual Training Phase Reaction Times
    sns.lineplot(data=participant_training_data, x=participant_training_data.index, y="RT", label="Training RT")
    plt.title(f"Participant {participant_id} Training Reaction Times")
    plt.ylabel("Reaction Time (s)")
    plt.xlabel("Trial")
    plt.legend()
    plt.show()
    
    # Plot Individual Test Phase Accuracy
    # Create a DataFrame for plotting
    test_accuracy_df = participant_test_data.reset_index()
    sns.barplot(data=test_accuracy_df, x="index", y="accuracy", ci=None)
    plt.title(f"Participant {participant_id} Test Accuracy")
    plt.ylabel("Accuracy")
    plt.xlabel("Trial")
    plt.show()

# %% GROUP-LEVEL ANALYSIS
# Training Phase: Group-Level Accuracy and Reaction Time
group_training_accuracy = all_training_data.groupby("Participant_ID")["accuracy"].mean() * 100
group_training_rt_correct = all_training_data[all_training_data["accuracy"] == 1].groupby("Participant_ID")["RT"].mean()

# Test Phase: Group-Level Accuracy and Reaction Time
group_test_accuracy = all_test_data.groupby("Participant_ID")["accuracy"].mean() * 100
group_test_rt_correct = all_test_data[all_test_data["accuracy"] == 1].groupby("Participant_ID")["RT"].mean()

# Group-Level Summary
print("Group-Level Training Phase Accuracy:\n", group_training_accuracy)
print("Group-Level Training Phase RT (Correct):\n", group_training_rt_correct)
print("Group-Level Test Phase Accuracy:\n", group_test_accuracy)
print("Group-Level Test Phase RT (Correct):\n", group_test_rt_correct)

# Group-Level Plots
# Accuracy Across Phases for All Participants
sns.barplot(x=group_training_accuracy.index, y=group_training_accuracy.values)
plt.title("Group Training Phase Accuracy Rate")
plt.ylabel("Accuracy (%)")
plt.xlabel("Participant")
plt.show()

sns.barplot(x=group_test_accuracy.index, y=group_test_accuracy.values)
plt.title("Group Test Phase Accuracy Rate")
plt.ylabel("Accuracy (%)")
plt.xlabel("Participant")
plt.show()

# Reaction Times Across Phases for All Participants
sns.lineplot(data=all_training_data, x=all_training_data.index, y="RT", label="Training RT")
sns.lineplot(data=all_test_data, x=all_test_data.index, y="RT", label="Test RT")
plt.title("Reaction Times Across Phases (All Participants)")
plt.ylabel("Reaction Time (s)")
plt.xlabel("Trial")
plt.legend()
plt.show()

# %% OVERALL AVERAGES
# Calculate overall averages for training and test phases
overall_training_accuracy = all_training_data["accuracy"].mean() * 100
overall_training_rt = all_training_data["RT"].mean()

overall_test_accuracy = all_test_data["accuracy"].mean() * 100
overall_test_rt = all_test_data["RT"].mean()

# Print overall results
print(f"Overall Training Phase Accuracy: {overall_training_accuracy:.2f}%")
print(f"Overall Training Phase RT: {overall_training_rt:.2f} seconds")

print(f"Overall Test Phase Accuracy: {overall_test_accuracy:.2f}%")
print(f"Overall Test Phase RT: {overall_test_rt:.2f} seconds")

# %% VISUALIZE OVERALL AVERAGES
# Combine data for visualization
overall_summary = pd.DataFrame({
    "Phase": ["Training", "Training", "Test", "Test"],
    "Metric": ["Accuracy", "RT", "Accuracy", "RT"],
    "Value": [overall_training_accuracy, overall_training_rt, overall_test_accuracy, overall_test_rt]
})

# Plot overall averages
sns.barplot(data=overall_summary, x="Phase", y="Value", hue="Metric")
plt.title("Overall Averages for Accuracy and Reaction Times")
plt.ylabel("Value")
plt.xlabel("Phase")
plt.legend(title="Metric")
plt.show()
