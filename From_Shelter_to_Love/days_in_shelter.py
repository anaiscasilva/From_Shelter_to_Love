import numpy as np

def compute_days_in_shelter(df):
    df['Days in Shelter'] = np.ceil((df['DateTime Outcome'] - df['DateTime Intake']) / np.timedelta64(24,'h'))
    df = df[df['Days in Shelter'] > 0]
    df.dropna(inplace = True)
    return df