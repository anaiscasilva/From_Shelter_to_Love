import numpy as np

def compute_days_in_shelter(df):
    df['Days in Shelter'] = np.ceil((df_filtered['DateTimeOutcome'] - df_filtered['DateTimeIntake']) / np.timedelta64(24,'h'))
    df = df[df.days_in_shelter > 0]
    df.dropna(inplace = True)
    return df