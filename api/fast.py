from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from From_Shelter_to_Love.gcp import download_model_to_gcp
import joblib
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def index():
    return {"greeting": "Hello, welcome to shelter world! Thank you for saving me!woof-woof"}

@app.get("/predict")
def predict(intake_type, animal_type, intake_condition,
            breed, age_upon_intake_months, neutered_or_spayed_intake,
            male_or_female_intake, color):

    dic = {"intake_type": [intake_type],
            "intake_condition": [intake_condition],
            "breed": [breed],
            "age_upon_intake_months": [float(age_upon_intake_months)],
            "neutered_or_spayed_intake": [int(neutered_or_spayed_intake)],
            "male_or_female_intake": [float(male_or_female_intake)],
            "color": [color] 
            }

    X_pred = pd.DataFrame.from_dict(dic)
    
    if animal_type == "Cat":

        download_model_to_gcp('Cat')

        PATH_TO_LOCAL_PREPROC = 'catspreproc.joblib'
    
        prep = joblib.load(PATH_TO_LOCAL_PREPROC)
        X_pred_t = prep.transform(X_pred)

        PATH_TO_LOCAL_MODEL = 'catsmodel.joblib'
    
        model = joblib.load(PATH_TO_LOCAL_MODEL)
        y_pred = int(model.predict(X_pred_t)[0])

        return {"prediction": y_pred}

    elif animal_type == "Dog":

        download_model_to_gcp('Dog')

        PATH_TO_LOCAL_PREPROC = 'dogspreproc.joblib'

        prep = joblib.load(PATH_TO_LOCAL_PREPROC)
        X_pred_t = prep.transform(X_pred)
        
        PATH_TO_LOCAL_MODEL = 'dogsmodel.joblib'
    
        model = joblib.load(PATH_TO_LOCAL_MODEL)
        y_pred = int(model.predict(X_pred_t)[0])

        return {"prediction": y_pred}

