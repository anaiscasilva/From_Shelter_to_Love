
import pandas as pd

def get_data():
    """method to get the training data (or a portion of it) from google cloud bucket"""
    df_intakes = pd.read_csv('../raw_data/Austin_Animal_Center_Intakes.csv', parse_dates=['DateTime'])
    df_outcomes = pd.read_csv('../raw_data/Austin_Animal_Center_Outcomes.csv', parse_dates=['DateTime'])
    df_straymap = pd.read_csv('../raw_data/Austin_Animal_Center_Stray_Map.csv')
    return df_intakes, df_outcomes, df_straymap, 

def get_data():
