from From_Shelter_to_Love.data import only_dogs, only_cats, final_data 
from sklearn.model_selection import train_test_split
from From_Shelter_to_Love.pipeline import preprocessor
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
import joblib
from xgboost import XGBClassifier
from google.cloud import storage

BUCKET_NAME = 'from-shelter-to-love-682-silva-roth-matos'
STORAGE_LOCATION_MODELDOGS = 'models/dogsmodel.joblib'
STORAGE_LOCATION_MODELCATS = 'models/catsmodel.joblib'
STORAGE_LOCATION_PREPROCDOGS = 'preproc/dogspreproc.joblib'
STORAGE_LOCATION_PREPROCCATS = 'preproc/catspreproc.joblib'

def split_cats():
    df = final_data()
    
    # Filter only cats
    df_onlycats = only_cats(df)
    df_onlycats.drop(columns = ['animal_type'], inplace = True)

    y_cats = df_onlycats['target']
    X_cats = df_onlycats.drop('target', axis=1)
    
    X_train_cats, X_test_cats, y_train_cats, y_test_cats = train_test_split(X_cats, y_cats, test_size=0.3, random_state = 10)
    print('split data of cats')
    return X_train_cats, y_train_cats, X_test_cats, y_test_cats

def split_dogs():
    df = final_data()

    # Filter only dogs
    df_onlydogs = only_dogs(df)
    df_onlydogs.drop(columns = ['animal_type'], inplace = True)

    y_dogs = df_onlydogs['target']
    X_dogs = df_onlydogs.drop('target', axis=1)
    
    X_train_dogs, X_test_dogs, y_train_dogs, y_test_dogs = train_test_split(X_dogs, y_dogs, test_size=0.3, random_state = 10)
    print('split data of dogs')
    return X_train_dogs, X_test_dogs, y_train_dogs, y_test_dogs

def best_model_cats():
    xgb_model = XGBClassifier(objective= 'binary:logistic', learning_rate=0.1,
                                        max_depth=5, n_estimators= 180)

    return xgb_model

def preprocessing_and_train_cats():
    X_train_cats, y_train_cats, X_test_cats, y_test_cats = split_cats()
    prep = preprocessor()
    prep.fit(X_train_cats, y_train_cats)
    X_train_cats_transf = prep.transform(X_train_cats)
    X_test_cats_transf = prep.transform(X_test_cats)
    joblib.dump(prep, 'catspreproc.joblib')

    print('preprocessing cats data')
    model = best_model_cats()
    trained_model_cats = model.fit(X_train_cats_transf, y_train_cats)
    print('trained model of cats')
    return trained_model_cats, y_test_cats, X_test_cats_transf

def best_model_dogs():
    rf_model = RandomForestClassifier(class_weight='balanced_subsample', max_depth=10,
                                    max_features='log2', min_samples_leaf=2,
                                    min_samples_split=5, n_jobs=1)

    return rf_model

def preprocessing_and_train_dogs():
    X_train_dogs, X_test_dogs, y_train_dogs, y_test_dogs = split_dogs()
    prep = preprocessor()
    prep.fit(X_train_dogs, y_train_dogs)
    X_train_dogs_transf = prep.transform(X_train_dogs)
    X_test_dogs_transf = prep.transform(X_test_dogs)
    joblib.dump(prep, 'dogspreproc.joblib')

    print('preprocessing dogs data')
    #Create an oversampled training data
    smote = SMOTE(random_state = 101)
    X_train_transf_oversample_dogs, y_train_oversample_dogs = smote.fit_resample(X_train_dogs_transf, y_train_dogs)
    
    model = best_model_dogs()
    trained_model_dogs = model.fit(X_train_transf_oversample_dogs, y_train_oversample_dogs)
    print('trained model of dogs')
    return trained_model_dogs, y_test_dogs, X_test_dogs_transf

def upload_model_to_gcp(animal_type):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    
    if animal_type == 'cats':
        blob = bucket.blob(STORAGE_LOCATION_MODELCATS)
        blob.upload_from_filename('catsmodel.joblib')
        blob = bucket.blob(STORAGE_LOCATION_PREPROCCATS)
        blob.upload_from_filename('catspreproc.joblib')

    elif animal_type == 'dogs':
        blob = bucket.blob(STORAGE_LOCATION_MODELDOGS)
        blob.upload_from_filename('dogsmodel.joblib')
        blob = bucket.blob(STORAGE_LOCATION_PREPROCDOGS)
        blob.upload_from_filename('dogspreproc.joblib')

def save_model(model, animal_type):
    """method that saves the model into a .joblib file and uploads it on Google Storage /models folder
    HINTS : use joblib library and google-cloud-storage"""

    # saving the trained model to disk is mandatory to then beeing able to upload it to storage
    # Implement here
    joblib.dump(model, f'{animal_type}model.joblib')
    print(f"saved {animal_type}model.joblib locally")

    # Implement here
    upload_model_to_gcp(animal_type)
    print(f"uploaded model.joblib to gcp cloud storage under \n => {f'STORAGE_LOCATION{animal_type}'}")


if __name__ == "__main__":

    trained_model_dogs, y_test_dogs, X_test_dogs_transf = preprocessing_and_train_dogs()  
    trained_model_cats, y_test_cats, X_test_cats_transf = preprocessing_and_train_cats()

    # save trained model to GCP bucket (whether the training occured locally or on GCP)
    save_model(trained_model_dogs, 'dogs')
    save_model(trained_model_cats, 'cats')
