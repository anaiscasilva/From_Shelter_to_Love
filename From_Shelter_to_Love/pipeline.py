from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler , OneHotEncoder
from sklearn.compose import make_column_selector, ColumnTransformer

def preprocessor():
    # Impute then Scale for numerical variables
    num_transformer = Pipeline([
        ('imputer', SimpleImputer()),
        ('scaler', MinMaxScaler())])

    # Encode categorical varibles 
    cat_transformer = OneHotEncoder(handle_unknown='ignore',sparse=False)

    # Apply transformations to desired features
    preprocessor = ColumnTransformer([
        ('num_transformer', num_transformer, make_column_selector(dtype_include=['int64',"float64"])),
        ('cat_transformer', cat_transformer, make_column_selector(dtype_include=["object"]))])

    #or

    #cat_bi_transformer = OneHotEncoder(drop='if_binary', sparse = False)
    # Apply transformations to desired features
    #preprocessor = ColumnTransformer([
        #('num_transformer', num_transformer, ['age_upon_intake_months', 'neutered_or_spayed_intake', 'male_or_female_intake']),
        #('cat_bi_transformer', cat_bi_transformer, ['Breed', 'Intake Condition']),
        #('cat_transformer', cat_transformer, ['color', 'Intake Type'])],
        #remainder='passthrough')

    return preprocessor