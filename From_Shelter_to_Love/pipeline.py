from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler , OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier


def preprocessor():
    # Impute then Scale for numerical variables
    num_transformer = Pipeline([
        ('imputer', SimpleImputer()),
        ('scaler', MinMaxScaler())])

    # Encode categorical varibles 
    cat_transformer = OneHotEncoder(handle_unknown='ignore',sparse=False)

    cat_bi_transformer = OneHotEncoder(drop='if_binary', sparse = False)

    # Apply transformations to desired features
    preprocessor = ColumnTransformer([
        ('num_transformer', num_transformer, ['age_upon_intake_months', 'neutered_or_spayed_intake', 'male_or_female_intake']),
        ('cat_bi_transformer', cat_bi_transformer, ['Breed', ]),
        ('cat_transformer', cat_transformer, ['color', 'Intake Condition', 'Intake Type'])],
        remainder='passthrough')
    
    return preprocessor

def pipeline_cats():
    pipe_cats = Pipeline([
    ('preprocessing', preprocessor()),
    ('classifier', RandomForestClassifier())])
    return pipe_cats 

def pipeline_dogs():
    pipe_dogs = Pipeline([
    ('preprocessing', preprocessor()),
    ('classifier', RandomForestClassifier())])
    return pipe_dogs 

