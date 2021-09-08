from From_Shelter_to_Love.data import get_data, clean_intakes, clean_outcomes, merge_data, cats_and_dogs
from From_Shelter_to_Love.days_in_shelter import compute_days_in_shelter
from sklearn.model_selection import train_test_split
from From_Shelter_to_Love.encoders import age, group_color, neutered_animals, male_animals, breed







#if __name__ == "__main__":
def get_data_2():    
    # Get data
    df_intakes, df_outcomes, df_straymap = get_data()

    # Clean data
    df_intakes = clean_intakes(df_intakes)
    df_outcomes = clean_outcomes(df_outcomes)

    # Merge data
    df_merged = merge_data(df_intakes, df_outcomes)


    # Filter only cats and dogs
    df_filtered = cats_and_dogs(df_merged)
    df = compute_days_in_shelter(df_filtered)
    
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


    y = df["Days in Shelter"]
    X = df.drop("Days in Shelter", axis=1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state = 10)

    return df

    # Train and save model, locally and
    #trainer = Trainer(X=X_train, y=y_train)
    #trainer.set_experiment_name('xp2')
    #trainer.run()
    #rmse = trainer.evaluate(X_test, y_test)
    #print(f"rmse: {rmse}")
    #trainer.save_model()