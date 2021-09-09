import pandas as pd
import numpy as np
import re


def get_data():
    # Read CSV
    df_intakes = pd.read_csv('../raw_data/Austin_Animal_Center_Intakes.csv', parse_dates=['DateTime'])
    df_outcomes = pd.read_csv('../raw_data/Austin_Animal_Center_Outcomes.csv', parse_dates=['DateTime'])
    df_straymap = pd.read_csv('../raw_data/Austin_Animal_Center_Stray_Map.csv')

    # Drop Duplicates
    df_intakes.drop_duplicates(inplace = True)
    df_outcomes.drop_duplicates(inplace = True)

    #Dropping Irrelevant Features
    df_intakes.drop(columns = ['Name','MonthYear','Found Location'], inplace = True)
    df_intakes.rename(columns = {'DateTime':'DateTimeIntake'}, inplace = True)
    df_outcomes.drop(columns = ['Name','MonthYear','Date of Birth','Breed','Color','Animal Type', 'Outcome Subtype'], inplace = True)
    df_outcomes.rename(columns = {'DateTime':'DateTimeOutcome'}, inplace = True)

    # Sorting all the intakes and outcomes based on Animal ID and DateTime
    df_intakes.sort_values(by = ['Animal ID', 'DateTimeIntake'], ascending = [True, True], inplace = True)
    df_outcomes.sort_values(by = ['Animal ID','DateTimeOutcome'], ascending = [True,True], inplace = True) 

    # Dropping all the animals that were more than one time in the shelter
    df_intakes.drop_duplicates(subset = 'Animal ID', inplace = True)
    df_outcomes.drop_duplicates(subset = 'Animal ID', inplace = True)
    
    # Merging the datasets
    df_merged = pd.merge(left = df_intakes, right = df_outcomes, how = 'left', on = ['Animal ID'])

    # Filtering only dogs
    df_filtered = df_merged[(df_merged['Animal Type'] == 'Dog') | (df_merged['Animal Type'] == 'Cat')].copy()

    # Calculating the number of days a dog stays in shelter
    df_filtered['days_in_shelter'] = np.ceil((df_filtered['DateTimeOutcome'] - df_filtered['DateTimeIntake']) / np.timedelta64(24,'h'))

    # Dropping all the the negatives values (errors in merging datasets) and null values (dogs that are still in shelter)
    df_filtered = df_filtered[df_filtered.days_in_shelter > 0]

    #Dropping rows with NaNs
    df_filtered.dropna(inplace = True)

    # Transforming ages in string to integer in months
    def dog_age(df):
        dog_months = []
        dog_years = []
        for age in df:
            if 'years' in age or 'year' in age:
                years = int(re.findall('(-?\d+)',age)[0])
                if years < 0:
                    dog_months.append(np.nan)
                    dog_years.append(np.nan)
                else:
                    dog_months.append(years*12)
                    dog_years.append(years)
            elif 'months' in age or 'month' in age:
                months = int(re.findall('(-?\d+)',age)[0])
                years = int(re.findall('(-?\d+)',age)[0])
                if months < 0:
                    dog_months.append(np.nan)
                else:
                    dog_months.append(months)
                    dog_years.append(1)
            else:
                weeks_or_days = int(re.findall('(-?\d+)',age)[0])
                if weeks_or_days < 0:
                    dog_months.append(np.nan)
                else:
                    dog_months.append(1)
                    dog_years.append(1)
        return [dog_months, dog_years]

    df_filtered['age_upon_intake_months'] = dog_age(df_filtered['Age upon Intake'])[0]
    df_filtered['age_upon_intake_years'] = dog_age(df_filtered['Age upon Intake'])[1]
    df_filtered['age_upon_outcome_months'] = dog_age(df_filtered['Age upon Outcome'])[0]
    df_filtered['age_upon_outcome_years'] = dog_age(df_filtered['Age upon Outcome'])[1]
    df_filtered.drop(columns = ['DateTimeIntake', 'DateTimeOutcome','Age upon Intake', 'Age upon Outcome'], inplace = True)

    # Defining functions to see if the animal is neutered/spayed
    def neutered_animals(df):
        animal_neutered = []
        for animal in df:
            if 'Neutered' in animal or 'Spayed' in animal:
                animal_neutered.append(1)
            elif 'Unkown' in animal:
                animal_neutered.append(np.nan)
            else:
                animal_neutered.append(0)
        return animal_neutered

    # or not and if the animal is male or female
    def male_animals(df):
        male_animal = []
        for animal in df:
            if 'Male' in animal:
                male_animal.append(1)
            elif 'Female' in animal:
                male_animal.append(0)
            else:
                male_animal.append(np.nan)
        return male_animal

    df_filtered['neutered_or_spayed_outcome'] = neutered_animals(df_filtered['Sex upon Outcome'])
    df_filtered['male_or_female_outcome'] = male_animals(df_filtered['Sex upon Outcome'])
    df_filtered['neutered_or_spayed_intake'] = neutered_animals(df_filtered['Sex upon Intake'])
    df_filtered['male_or_female_intake'] = male_animals(df_filtered['Sex upon Intake'])
    df_filtered.drop(columns = ['Sex upon Outcome', 'Sex upon Intake'], inplace = True)

    # Defining a function to reduce the number of breeds to mixed and pure
    def breed(df):
        breeds = []
        for breed in df:
            if 'Mix' in breed or '/' in breed or 'Domestic' in breed:
                breeds.append('Mixed')
            else:
                breeds.append('Pure')
        return breeds

    df_filtered['Breed'] = breed(df_filtered['Breed'])

    # Defining a function to reduce the number of colors
    def colors(df):
        colors = []
        for color in df:
            if '/' in color:
                colors.append('Bicolor')
            elif 'Tricolor' in color or 'Calico' in color or 'Torbie' in color or 'Tortie' in color:
                colors.append('Tricolor')
            elif 'Agouti' in color or 'Black' in color or 'Blue' in color or 'Buff' in color or 'Brown' in color \
            or 'Chocolate' in color or 'Orange' in color or 'Gray' in color or 'Lilac' in color or 'Liver' in color \
            or 'Orange' in color or 'Red' in color or 'Sable' in color:
                colors.append('Dark')
            elif 'Apricot' in color or 'Cream' in color or 'Fawn' in color or 'Flame' in color or 'Gold' in color \
            or 'Lynx' in color or 'Pink' in color or 'Seal' in color or 'Silver' in color or 'Tan' in color \
            or 'White' in color or 'Yellow' in color:
                colors.append('Light')
        return colors
  
    df_filtered['color'] = colors(df_filtered['Color'])
    df_filtered.drop(columns = 'Color', inplace = True)
    return df_filtered
