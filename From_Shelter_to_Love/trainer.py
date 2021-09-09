from From_Shelter_to_Love.data import get_data, clean_intakes, clean_outcomes, merge_data, only_dogs, only_cats
from From_Shelter_to_Love.compute_target import classifier_y, compute_days_in_shelter
from sklearn.model_selection import train_test_split
from From_Shelter_to_Love.encoders import age, group_color, neutered_animals, male_animals, breed, colors
from From_Shelter_to_Love.pipeline import pipeline


BUCKET_NAME = 'wagon-data-682-silva'
STORAGE_LOCATION_DOGS = 'models/fromsheltertolove/modeldogs.joblib'
STORAGE_LOCATION_CATS = 'models/fromsheltertolove/modelcats.joblib'


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
    # Get data
    df_intakes, df_outcomes, df_straymap = get_data()

    # Clean data
    df_intakes = clean_intakes(df_intakes)
    df_outcomes = clean_outcomes(df_outcomes)

    # Merge data
    df_merged = merge_data(df_intakes, df_outcomes)

    
    # Compute target 
    df = compute_days_in_shelter(df)
    df = classifier_y(df, 'Days in Shelter')
    
    #Converting ages 
    df['age_upon_intake_months'] = age(df['Age upon Intake'])[0]
    df['age_upon_intake_years'] = age(df['Age upon Intake'])[1]
    df['age_upon_outcome_months'] = age(df['Age upon Outcome'])[0]
    df['age_upon_outcome_years'] = age(df['Age upon Outcome'])[1]
    df.drop(columns = ['DateTime Intake', 'DateTime Outcome','Age upon Intake', 'Age upon Outcome'], inplace = True)

    # Transforming colors 
    df = group_color(df,'Color')
    df.drop(columns = ['Color'], inplace = True)

    df = neutered_animals(df,'Sex upon Outcome')
    df = male_animals(df,'Sex upon Outcome')
    df.drop(columns = ['Sex upon Outcome'], inplace = True)

    df = breed(df,'Breed')
    df.drop(columns = ['Breed'], inplace = True)

    df = colors(df,'Color')
    df.drop(columns = ['Color'], inplace = True)

    # Filter only cats
    df_onlycats = only_cats(df_merged)

    # Filter only dogs
    df_onlydogs = only_dogs(df_merged)

    y_onlycats = df_onlycats['target']
    X_onlycats = df_onlycats.drop('target', axis=1)

    y_onlydogs = df_onlydogs['target']
    X_onlydogs = df_onlydogs.drop('target', axis=1)
    
    X_train_cats, X_test_cats, y_train_cats, y_test_cats = train_test_split(X_onlycats, y_onlycats, test_size=0.3, random_state = 10)
    X_train_dogs, X_test_dogs, y_train_dogs, y_test_dogs = train_test_split(X_onlydogs, y_onlydogs, test_size=0.3, random_state = 10)

    pipe = pipeline()
    
    trained_model_dogs = pipe.fit(X_train_dogs,y_train_dogs)

    trained_model_cats = pipe.fit(X_train_cats,y_train_cats)


    # save trained model to GCP bucket (whether the training occured locally or on GCP)
    save_model(trained_model_dogs)

    save_model(trained_model_cats)

