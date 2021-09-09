import numpy as np

def compute_days_in_shelter(df):
    df['Days in Shelter'] = np.ceil((df['DateTime Outcome'] - df['DateTime Intake']) / np.timedelta64(24,'h'))
    df = df[df['Days in Shelter'] > 0]
    df.dropna(inplace = True)
    return df

def classifier_y(df,column):
    target = []
    for days in df[column]:
        if days<60:
            target.append(1)
        else :
            target.append(0)
    df['target'] = target
    return df