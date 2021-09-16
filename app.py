import streamlit as st
import requests

st.set_page_config(
    page_title = 'From Shelter to Love',
    page_icon = '🐶',
    layout = 'wide', #centered
    initial_sidebar_state = 'auto' # collapsed
)

# ----------------------------------
#         BACKGROUND
# ----------------------------------

CSS_dog = """
.block-container {
    background-color: rgba(255, 255, 255, 0.5);
    color: rgba(0, 0, 0, 1);
}
.stApp {
    background-image: url(https://keyassets-p2.timeincuk.net/wp/prod/wp-content/uploads/sites/63/2019/06/GettyImages-980647656_304176642_559031601-scaled.jpg);
    background-size: cover;
}
"""

CSS_cat = """
.block-container {
    background-color: rgba(255, 255, 255, 0.5);
    color: rgba(0, 0, 0, 1);
}
.stApp {
    background-image: url(https://images.unsplash.com/photo-1554310212-e1d9f0d4d9be?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80);
    background-size: cover;
}
"""

#Title

'''
# 🐶 From Shelter to Love 🐱
'''

#Sub-Title

st.write(' This website helps you understand if a dog or cat will stay more than 1 week in a shelter.\
    Please enter some information to help us predicting this.'
    )

st.write('First, you need to specify if the animal is a dog or a cat.')

choose = st.radio('',('','🐶 Dog','🐱 Cat'))

if choose == '':
    pass
elif choose == '🐶 Dog':
    st.write(f'<style>{CSS_dog}</style>', unsafe_allow_html=True)
    animal_type = 'Dog'
elif choose == '🐱 Cat':
    st.write(f'<style>{CSS_cat}</style>', unsafe_allow_html=True)
    animal_type = 'Cat'

# Conditions

st.write("### In which conditions were the animal taken in?")

col1, col2, col3 = st.columns((1.5,1.5,5))

intake_type = col1.selectbox("How was the animal taken in?",\
    ('Public Assist', 'Owner Surrender', 'Stray', 'Euthanasia Request','Abandoned'))

intake_condition = col2.selectbox("In which condition?",\
    ('Normal', 'Injured', 'Aged', 'Sick', 'Other', 'Medical', 'Feral', 'Pregnant', 'Nursing', 'Behavior'))


# Animal Characteristics
st.write("### Animal Characteristics")

col1, col2, col3, col4, col5, col6 = st.columns((0.7,0.7,1,1,1,1))

years = col1.number_input('Years',min_value = 0, max_value = 28,step=1,value=0)

if years == 0:
    months = col2.number_input('Months',min_value = 1, max_value = 11,step=1,value=1)
else:
    months = col2.number_input('Months',min_value = 0, max_value = 11,step=1,value=1)

age_upon_intake_months = years * 12 + months

breed = col3.selectbox("Breed:",('Pure','Mixed'))

color = col4.selectbox("Color:",('Bicolor', 'Tricolor', 'Dark', 'Light'))

gender = ("Female", "Male")
options = list(range(len(gender)))
male_or_female_intake = col5.selectbox("Gender:", options, format_func=lambda x: gender[x])

if male_or_female_intake == 0:
    spayed = ("Intact", "Spayed")
    options = list(range(len(spayed)))
    neutered_or_spayed_intake = col6.selectbox("Status:", options, format_func=lambda x: spayed[x])
else:
    neutered = ("Intact", "Neutered")
    options = list(range(len(neutered)))
    neutered_or_spayed_intake = col6.selectbox("Status:", options, format_func=lambda x: neutered[x])

st.write(f"### Please press the button to check if the animal will stay longer than 7 days in the shelter.")

# Prediction

url = 'https://fromsheltertolove-cs45mhffva-ew.a.run.app/predict'

if st.button('Click this button'):
    if choose == '':
        st.warning('You need to specify the animal type first!')
    else:
        params = {"intake_type": intake_type,
            "animal_type": animal_type,
            "intake_condition": intake_condition,
            "breed": breed,
            "age_upon_intake_months": age_upon_intake_months,
            "neutered_or_spayed_intake": neutered_or_spayed_intake,
            "male_or_female_intake": male_or_female_intake,
            "color": color
        }

        x = requests.get(url, params=params)
        if x.json()["prediction"] == 0:
            st.success("This animal is likely to stay less than 7 days in the shelter.")
        else:
            st.info('''
            This animal is likely to stay less than 7 days in the shelter. We strongly advise the shelter to:   
            - Take this animal to adoption fairs;   
            - Do more promotion about this animal on social networks;   
            - Try to show more information about this animal;   
            - Take some pictures and show them on social networks.  
            '''
            )


st.markdown('''<style> div.row-widget.stRadio > div{flex-direction:row;} div[role="radiogroup"] >  :first-child{
                display: none !important;
            } </style>''', unsafe_allow_html=True)