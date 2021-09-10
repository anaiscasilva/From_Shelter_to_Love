from From_Shelter_to_Love.data import get_data, clean_intakes, clean_outcomes, merge_data, only_dogs, only_cats, compute_age_upon_intake
from From_Shelter_to_Love.compute_target import classifier_y, compute_days_in_shelter
from sklearn.model_selection import train_test_split
from From_Shelter_to_Love.encoders import age, group_color, neutered_animals, male_animals, breed, colors
from From_Shelter_to_Love.pipeline import pipeline
from imblearn.over_sampling import SMOTE

BUCKET_NAME = 'wagon-data-682-silva'
STORAGE_LOCATION_DOGS = 'models/fromsheltertolove/modeldogs.joblib'
STORAGE_LOCATION_CATS = 'models/fromsheltertolove/modelcats.joblib'

def final_data():
    # Get data
    df_intakes, df_outcomes = get_data()

    # Clean data
    df_intakes = clean_intakes(df_intakes)
    df_outcomes = clean_outcomes(df_outcomes)

    # Merge data
    df_merged = merge_data(df_intakes, df_outcomes)

    # Compute target 
    df = compute_days_in_shelter(df_merged)
    df = classifier_y(df, 'Days in Shelter')
    
    # Calculating the number age upon intake
    df = compute_age_upon_intake(df)
    
    #Converting ages 
    df['age_upon_intake_months'] = age(df['Age upon Intake'])[0]
    df['age_upon_outcome_months'] = age(df['Age upon Outcome'])[0]

    # Transforming colors 
    df = group_color(df,'Color')
    df.drop(columns = ['Color'], inplace = True)

    df = neutered_animals(df,'Sex upon Intake')
    df = male_animals(df,'Sex upon Intake')
    df.drop(columns = ['Sex upon Intake'], inplace = True)

    df = breed(df,'Breed')

    df = colors(df)
    df.drop(columns = ['Color'], inplace = True)
    
    df = colors(df,'Intake Condition')
    df.drop(columns = ['Color'], inplace = True)
 
    df = df[['Intake Type',"Animal Type",'Intake Condition',
            'Breeds','age_upon_intake_months','age_upon_intake_months_number', 'neutered_or_spayed_intake',
            'male_or_female_intake','color']]

    return df

def smote_and_split_cats():
    df = final_data()
    
    # Filter only cats
    df_onlycats = only_cats(df)
    df_onlycats.drop(columns = ['Animal Type'], inplace = True)

    y_cats = df_onlycats['target']
    X_cats = df_onlycats.drop('target', axis=1)
    
    X_train_cats, X_test_cats, y_train_cats, y_test_cats = train_test_split(X_cats, y_cats, test_size=0.3, random_state = 10)
    
    #Importing SMOTE
    #Create an oversampled training data
    smote = SMOTE(random_state = 101)
    X_train_oversample_cats, y_train_oversample_cats = smote.fit_resample(X_train_cats, y_train_cats)

    return X_train_oversample_cats, y_train_oversample_cats, X_test_cats, y_test_cats

def smote_and_split_dogs():
    df = final_data()

    # Filter only dogs
    df_onlydogs = only_dogs(df)
    df_onlydogs.drop(columns = ['Animal Type'], inplace = True)

    y_dogs = df_onlydogs['target']
    X_dogs = df_onlydogs.drop('target', axis=1)
    
    X_train_dogs, X_test_dogs, y_train_dogs, y_test_dogs = train_test_split(X_dogs, y_dogs, test_size=0.3, random_state = 10)
    
    #Importing SMOTE
    #Create an oversampled training data
    smote = SMOTE(random_state = 101)
    X_train_oversample_dogs, y_train_oversample_dogs = smote.fit_resample(X_train_dogs, y_train_dogs)

    return X_train_oversample_dogs, y_train_oversample_dogs, X_test_dogs, y_test_dogs

def preprocessing_and_train_dogs():
    pass



def upload_model_to_gcp():

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(STORAGE_LOCATION)
    blob.upload_from_filename('model.joblib')


def save_model(reg):
    """method that saves the model into a .joblib file and uploads it on Google Storage /models folder
    HINTS : use joblib library and google-cloud-storage"""

    # saving the trained model to disk is mandatory to then beeing able to upload it to storage
    # Implement here
    joblib.dump(reg, 'model.joblib')
    print("saved model.joblib locally")

    # Implement here
    upload_model_to_gcp()
    print(f"uploaded model.joblib to gcp cloud storage under \n => {STORAGE_LOCATION}")


if __name__ == "__main__":

    pipe = pipeline()
    
    trained_model_dogs = pipe.fit(X_train_dogs,y_train_dogs)

    trained_model_cats = pipe.fit(X_train_cats,y_train_cats)


    # save trained model to GCP bucket (whether the training occured locally or on GCP)
    save_model(trained_model_dogs)

    save_model(trained_model_cats)

