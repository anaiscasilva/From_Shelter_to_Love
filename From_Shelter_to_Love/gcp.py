from google.cloud import storage
from From_Shelter_to_Love.trainer import * 


def download_model_to_gcp(animal_type):
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)
    
    if animal_type == 'Cat':
        blob = bucket.blob(STORAGE_LOCATION_MODELCATS)
        blob.download_to_filename('catsmodel.joblib')
        blob = bucket.blob(STORAGE_LOCATION_PREPROCCATS)
        blob.download_to_filename('catspreproc.joblib')

    elif animal_type == 'Dog':
        blob = bucket.blob(STORAGE_LOCATION_MODELDOGS)
        blob.download_to_filename('dogsmodel.joblib')
        blob = bucket.blob(STORAGE_LOCATION_PREPROCDOGS)
        blob.download_to_filename('dogspreproc.joblib')