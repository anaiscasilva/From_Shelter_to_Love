import pandas as pd
import numpy as np
import re 

# Transforming ages in string to integer in months

def age(df):
    months = []
    years = []
    for age in df:
        if 'years' in age or 'year' in age:
            years = int(re.findall('(-?\d+)',age)[0])
            if years < 0:
                months.append(np.nan)
                years.append(np.nan)
            else:
                months.append(years*12)
                years.append(years)
        elif 'months' in age or 'month' in age:
            months = int(re.findall('(-?\d+)',age)[0])
            years = int(re.findall('(-?\d+)',age)[0])
            if months < 0:
                months.append(np.nan)
            else:
                months.append(months)
                years.append(1)
        else:
            weeks_or_days = int(re.findall('(-?\d+)',age)[0])
            if weeks_or_days < 0:
                months.append(np.nan)
            else:
                months.append(1)
                years.append(1)
    
    return [months, years]
    
# Transforming colors in to groups

def group_color(df,column):
    group_colors = []
    for animal in df[column]:
        color_split = animal.split("/")
        group_colors.append(color_split[0])
    df["group_color"] = group_colors
    return df.reset_index(drop=True)


# Defining functions to see if the animal is neutered/spayed or not and if the animal is male or female
​
def neutered_animals(df,column):
    animal_neutered = []
    for animal in df[column]:
        if 'Neutered' in animal or 'Spayed' in animal:
            animal_neutered.append(1)
        elif 'Unkown' in animal:
            animal_neutered.append(np.nan)
        else:
            animal_neutered.append(0)
    df['neutered_or_spayed'] = animal_neutered
    return df.reset_index(drop=True)
​
def male_animals(df,column):
    male_animal = []
    for animal in df[column]:
        if 'Male' in animal:
            male_animal.append(1)
        elif 'Female' in animal:
            male_animal.append(0)
        else:
            male_animal.append(np.nan)
    df['male_or_female'] = male_animal
    return df.reset_index(drop=True)
​

# Defining a function to reduce the number of breeds to mixed and pure
​
def breed(df,column):
    breeds = []
    for breed in df[column]:
        if 'Mix' in breed or '/' in breed or 'Domestic' in breed:
            breeds.append('Mixed')
        else:
            breeds.append(breed)
    df['Breed'] = breeds
    return df.reset_index(drop=True)

