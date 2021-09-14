import pandas as pd
import numpy as np
import re 

# Transforming ages in string to integer in months

def age(df):
    months_age = []
    years_age = []
    for age in df:
        if 'years' in age or 'year' in age:
            years = int(re.findall('(-?\d+)',age)[0])
            if years < 0:
                months_age.append(np.nan)
                years_age.append(np.nan)
            else:
                months_age.append(years*12)
                years_age.append(years)
        elif 'months' in age or 'month' in age:
            months = int(re.findall('(-?\d+)',age)[0])
            years = int(re.findall('(-?\d+)',age)[0])
            if months < 0:
                months_age.append(np.nan)
            else:
                months_age.append(months)
                years_age.append(1)
        else:
            weeks_or_days = int(re.findall('(-?\d+)',age)[0])
            if weeks_or_days < 0:
                months_age.append(np.nan)
            else:
                months_age.append(1)
                years_age.append(1)
    
    return [months_age, years_age]

# Defining functions to see if the animal is neutered/spayed or not and if the animal is male or female

def neutered_animals(df,column):
    animal_neutered = []
    for animal in df.loc[:,column]:
        if 'Neutered' in animal or 'Spayed' in animal:
            animal_neutered.append(1)
        elif 'Unkown' in animal:
            animal_neutered.append(np.nan)
        else:
            animal_neutered.append(0)
    df['neutered_or_spayed_intake'] = animal_neutered
    return df.reset_index(drop=True)

def male_animals(df,column):
    male_animal = []
    for animal in df.loc[:,column]:
        if 'Male' in animal:
            male_animal.append(1)
        elif 'Female' in animal:
            male_animal.append(0)
        else:
            male_animal.append(np.nan)
    df['male_or_female_intake'] = male_animal
    return df.reset_index(drop=True)

# Defining a function to reduce the number of breeds to mixed and pure

def breed(df, column):
    breeds = []
    for breed in df.loc[:,column]:
        if 'Mix' in breed or '/' in breed or 'Domestic' in breed:
            breeds.append('Mixed')
        else:
            breeds.append('Pure')
    df['Breed'] = breeds
    return df.reset_index(drop=True)

# Defining a function to reduce the number of colors to Tricolor, Bicolor, Dark and Light

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

# Defining a function to reduce the number of intake Normal and not normal

def condition(df, column):
    conditions = []
    for cond in df.loc[:,column]:
        if 'Normal' in cond:
            conditions.append('Normal')
        else:
            conditions.append('Not-Normal')
    df['Intake Condition'] = conditions
    return df.reset_index(drop=True)

# Compute age_upon_intake with date of birth 

def compute_age_upon_intake(df):
    df['age_upon_intake_number_months_number'] = np.ceil((df['DateTime Intake'] - df['Date of Birth'])/np.timedelta64(1, 'M'))
    df = df[df['age_upon_intake_number_months_number'] > 0].copy()
    df.dropna(inplace = True)
    return df