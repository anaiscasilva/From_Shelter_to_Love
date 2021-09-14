from From_Shelter_to_Love.data import only_dogs, only_cats, cats_and_dogs, final_data 
from sklearn.model_selection import train_test_split
from From_Shelter_to_Love.pipeline import preprocessor
from imblearn.over_sampling import SMOTE
import joblib 

BUCKET_NAME = '? example:wagon-data-682-silva'
STORAGE_LOCATION_DOGS = '? example:models/fromsheltertolove/modeldogs.joblib'
STORAGE_LOCATION_CATS = '? example:models/fromsheltertolove/modelcats.joblib'

def split_and_cats():
    df = final_data()
    
    # Filter only cats
    df_onlycats = only_cats(df)
    df_onlycats.drop(columns = ['Animal Type'], inplace = True)

    y_cats = df_onlycats['target']
    X_cats = df_onlycats.drop('target', axis=1)
    
    X_train_cats, X_test_cats, y_train_cats, y_test_cats = train_test_split(X_cats, y_cats, test_size=0.3, random_state = 10)

    return X_train_cats, y_train_cats, X_test_cats, y_test_cats

def split_and_dogs():
    df = final_data()

    # Filter only dogs
    df_onlydogs = only_dogs(df)
    df_onlydogs.drop(columns = ['Animal Type'], inplace = True)

    y_dogs = df_onlydogs['target']
    X_dogs = df_onlydogs.drop('target', axis=1)
    
    X_train_dogs, X_test_dogs, y_train_dogs, y_test_dogs = train_test_split(X_dogs, y_dogs, test_size=0.3, random_state = 10)
    
    #Create an oversampled training data
    smote = SMOTE(random_state = 101)
    X_train_oversample_dogs, y_train_oversample_dogs = smote.fit_resample(X_train_dogs, y_train_dogs)

    return X_train_oversample_dogs, y_train_oversample_dogs, X_test_dogs, y_test_dogs

def best_model_cats():
    pass

def preprocessing_and_train_cats():
    X_train_cats, y_train_cats, X_test_cats, y_test_cats = split_and_cats()
    preprocessor.fit(X_train_cats, y_train_cats)
    X_train_cats_transf = preprocessor.transform(X_train_cats)
    X_test_cats_transf = preprocessor.transform(X_test_cats)
    model = best_model_cats()
    trained_model_cats = model.fit(X_train_cats_transf, y_train_dogs)
    return trained_model_cats, y_test_cats, X_test_cats_transf

def best_model_dogs():
    pass

def preprocessing_and_train_dogs():
    X_train_oversample_dogs, y_train_oversample_dogs, X_test_dogs, y_test_dogs = split_and_dogs()
    preprocessor.fit(X_train_dogs, y_train_dogs)
    X_train_dogs_transf = preprocessor.transform(X_train_oversample_dogs)
    X_test_dogs_transf = preprocessor.transform(X_test_dogs)
    model = best_model_dogs()
    trained_model_dogs = model.fit(X_train_dogs_transf, y_train_oversample_dogs)
    return trained_model_dogs, y_test_dogs, X_test_dogs_transf

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

    trained_model_dogs, y_test_dogs, X_test_dogs_transf = preprocessing_and_train_dogs()  
    trained_model_cats, y_test_cats, X_test_cats_transf = preprocessing_and_train_cats()

    # save trained model to GCP bucket (whether the training occured locally or on GCP)
    save_model(trained_model_dogs)
    save_model(trained_model_cats)

