import numpy as np
import pandas as pd
from From_Shelter_to_Love.compute_target import classifier_y0, compute_days_in_shelter
from From_Shelter_to_Love.encoders import age, neutered_animals, male_animals, breed, colors, compute_age_upon_intake, condition


def get_data():
    """method to get the training data (or a portion of it) from google cloud bucket"""
    df_intakes = pd.read_csv('../raw_data/Austin_Animal_Center_Intakes.csv', parse_dates=['DateTime'])
    df_outcomes = pd.read_csv('../raw_data/Austin_Animal_Center_Outcomes.csv', parse_dates=['DateTime', 'Date of Birth'])
    #df_straymap = pd.read_csv('../raw_data/Austin_Animal_Center_Stray_Map.csv')
    return df_intakes, df_outcomes


def clean_intakes(df_intakes):
    df_intakes.drop_duplicates(inplace = True)
    unused_column = ['Name', 'MonthYear', 'Found Location']
    df_intakes.drop(unused_column, axis=1, inplace = True)
    df_intakes.rename(columns={'DateTime': 'DateTimeIntake'}, inplace = True)
    return df_intakes


def clean_outcomes(df_outcomes):
    df_outcomes.drop_duplicates(inplace = True)
    unused_column = ['Name','MonthYear','Breed','Color','Animal Type', 'Outcome Subtype']
    df_outcomes.drop(unused_column, axis=1, inplace = True)
    df_outcomes.rename(columns={'DateTime': 'DateTimeOutcome'}, inplace = True)
    df_outcomes.dropna(how='all', inplace = True)
    return df_outcomes


def merge_data(df_intakes, df_outcomes):
    # Sorting all the intakes and outcomes based on Animal ID and DateTime
    df_intakes.sort_values(by = ['Animal ID', 'DateTimeIntake'], ascending = [True, True], inplace = True)
    df_outcomes.sort_values(by = ['Animal ID','DateTimeOutcome'], ascending = [True,True], inplace = True) 
    
    # Dropping all the animals that were more than one time in the shelter
    df_intakes.drop_duplicates(subset = 'Animal ID', inplace = True)
    df_outcomes.drop_duplicates(subset = 'Animal ID', inplace = True)

    # Merging the datasets
    df_merged = df_intakes.merge(df_outcomes, on='Animal ID', how='left').copy()
    return df_merged

def only_dogs(df):
    df_only_dogs = df[df['Animal Type'] == 'Dog'].copy()
    return df_only_dogs

def only_cats(df):  
    df_only_cats = df[df['Animal Type'] == 'Cat'].copy()
    return df_only_cats

def cats_and_dogs(df):
    df_cats_and_dogs = df[(df['Animal Type'] == 'Dog') | (df['Animal Type'] == 'Cat')].copy()
    return df_cats_and_dogs

def final_data():
    # Get data
    df_intakes, df_outcomes = get_data()

    # Clean data
    df_intakes = clean_intakes(df_intakes)
    df_outcomes = clean_outcomes(df_outcomes)

    # Merge data
    df_merged = merge_data(df_intakes, df_outcomes)

    #Only cats and dogs
    df = cats_and_dogs(df_merged)

    # Compute target 
    df = compute_days_in_shelter(df)
    df = classifier_y0(df, 'days_in_shelter')
    
    # Calculating the number age upon intake
    #df = compute_age_upon_intake(df)
    
    #Converting ages 
    df['age_upon_intake_months'] = age(df.loc[:,'Age upon Intake'])[0]
    df.dropna(inplace = True)

    df = neutered_animals(df,'Sex upon Intake')
    df = male_animals(df,'Sex upon Intake')
    df.drop(columns = ['Sex upon Intake'], inplace = True)

    df = breed(df,'Breed')

    # Transforming colors
    df['color'] = colors(df.loc[:,'Color'])
    df.drop(columns = 'Color', inplace = True)
    
    #df = condition(df,'Intake Condition')
 
    df = df[['Intake Type','Animal Type','Intake Condition',
            'Breed','age_upon_intake_months', 'neutered_or_spayed_intake',
            'male_or_female_intake','color']]

    return df