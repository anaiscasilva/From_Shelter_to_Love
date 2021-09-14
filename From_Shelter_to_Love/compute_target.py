import numpy as np

def compute_days_in_shelter(df):
    df['days_in_shelter'] = np.ceil((df['DateTimeOutcome'] - df['DateTimeIntake']) / np.timedelta64(24,'h'))
    df = df[df['days_in_shelter'] > 0].copy()
    df.dropna(inplace = True)
    return df

def classifier_y0(df,column):
    target = []
    for days in df[column]:
        if days <= 7:
          target.append(0)
        elif days > 7:
          target.append(1)
    df['target'] = target
    return df