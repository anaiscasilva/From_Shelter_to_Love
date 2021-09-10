import numpy as np
import pandas as pd

def get_data():
    """method to get the training data (or a portion of it) from google cloud bucket"""
    df_intakes = pd.read_csv('../raw_data/Austin_Animal_Center_Intakes.csv', parse_dates=['DateTime'])
    df_outcomes = pd.read_csv('../raw_data/Austin_Animal_Center_Outcomes.csv', parse_dates=['DateTime', 'Date of Birth'])
    #df_straymap = pd.read_csv('../raw_data/Austin_Animal_Center_Stray_Map.csv')
    return df_intakes, df_outcomes


def clean_intakes(df_intakes):
    unused_column = ['Name', 'MonthYear', 'Found Location', "Sex upon Intake"]
    df_intakes.drop(unused_column, axis=1, inplace = True)
    df_intakes.rename(columns={'DateTime': 'DateTime Intake'}, inplace = True)
    df_intakes.drop_duplicates(inplace = True)
    df_intakes.dropna(how='all', inplace = True)
    return df_intakes


def clean_outcomes(df_outcomes):
    unused_column = ['Name','MonthYear','Breed','Color','Animal Type', 'Outcome Subtype']
    df_outcomes.drop(unused_column, axis=1, inplace = True)
    df_outcomes.rename(columns={'DateTime': 'DateTime Outcome'}, inplace = True)
    df_outcomes.drop_duplicates(inplace = True)
    df_outcomes.dropna(how='all', inplace = True)
    return df_outcomes


def merge_data(df_intakes, df_outcomes):
    # Sorting all the intakes and outcomes based on Animal ID and DateTime
    df_intakes.sort_values(by = ['Animal ID', 'DateTime Intake'], ascending = [True, True], inplace = True)
    df_outcomes.sort_values(by = ['Animal ID','DateTime Outcome'], ascending = [True,True], inplace = True) 
    
    # Dropping all the animals that were more than one time in the shelter
    df_intakes.drop_duplicates(subset = 'Animal ID', inplace = True)
    df_outcomes.drop_duplicates(subset = 'Animal ID', inplace = True)

    # Merging the datasets
    df_merged = df_intakes.merge(df_outcomes, on='Animal ID', how='left')
    return df_merged

def only_dogs(df):
    df_only_dogs = df[df['Animal Type'] == 'Dog']
    return df_only_dogs

def only_cats(df):  
    df_only_cats = df[df['Animal Type'] == 'Cat']
    return df_only_cats

def cats_and_dogs(df):
    df_cats_and_dogs = df[(df['Animal Type'] == 'Dog') | (df['Animal Type'] == 'Cat')]
    return df_cats_and_dogs

def compute_age_upon_intake(df):
    df['age_upon_intake_number_months_number'] = np.ceil((df['DateTime Intake'] - df['Date of Birth'])/np.timedelta64(1, 'M'))
    df = df[df['age_upon_intake_number_months_number'] > 0]
    df.dropna(inplace = True)
    return df
