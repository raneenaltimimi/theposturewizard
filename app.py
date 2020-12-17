from SessionState import get
import streamlit as st
from theposturewizard import utils
import os
from io import BytesIO
from PIL import Image
import requests
import pandas as pd



PATH_TO_MODEL = "models/rv1-VGG16-test"


model = utils.load_my_model(PATH_TO_MODEL)


def get_video(exercice):
    if 'https://player' in exercice['video_src']:
        return exercice['video_src']


def info(exercice):
    # name
    st.markdown(f"""### {exercice.exercise_name}""")

    # instruction
    st.markdown(f"""
        **Instructions And Preparation:**\n
        {exercice.Exercise_description}""")

    # reps
    st.markdown(f"""
        **Repetitions:**\n
        {exercice.Reps}""")

    # pictures
    #   gif
    width = 300
    html_string = f'<a href="url"><img src="{exercice.img}" align="left" width="{width}" ></a>'
    #   target muscle
    url = exercice.target_muscle
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert('RGB')

    cols = st.beta_columns(2)
    with cols[0]:
        st.markdown(html_string, unsafe_allow_html=True)
    with cols[1]:
        st.image(img, use_column_width=True)



def get_input_img():
    uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg'])

    if uploaded_file:
        pos = Image.open(uploaded_file)
        cols = st.beta_columns(5)
        with cols[2]:
            st.image(pos, use_column_width=True)
    return uploaded_file


# STREAMLIT PAGE
params = {'get_prediction':False, 'file_name':''}
session_state = get(**params)


'''
# The Posture Wizard
'''
st.markdown(""" Find the best exercises to fix your upper body part posture """)

st.markdown("""
            - Upload a side picture of yourself
            - Our wizard will then determine your posture
            - Finally you will be suggested exercises based on your posture
            """ )
st.markdown(""" # Step One """)
st.markdown("""Upload a side view of your posture""")

uploaded_file = get_input_img()

if uploaded_file:
    if uploaded_file.name != session_state.file_name:
        session_state.get_prediction = False
        session_state.file_name = uploaded_file.name


if st.button('Wizard evaluation') or session_state.get_prediction:
    session_state.get_prediction = True

    if uploaded_file:

        pred = utils.pipe(uploaded_file, model)
        st.write(f"The Wizard classified your posture as {pred}")

        if pred == "kyphosis":
            st.write("**Customize your plan! : **")

            bodypart = st.selectbox('Select a bodypart you want to work on', ['Shoulder', 'Neck'])

            if bodypart == 'Shoulder':
                apparatus = st.selectbox('Select an equipement', ['Bodyweight', 'Dumbbells', 'Bands'])

            else:
                apparatus = 'Bodyweight'

            if st.button('Get your plan!'):
                stretch, strength1, strength2 = utils.get_exercises(apparatus, bodypart)

                # stretch
                st.markdown(f"""## 1. Stretching Exercise""")

                info(stretch)
                st.markdown("""


                    """)


                # strength
                st.markdown(f"""## 2. Strengthening Exercises""")

                # strength 1
                info(strength1)
                st.markdown("""


                    """)

                # strength 2
                info(strength2)
            else:
                st.markdown(""" # Step Three """)
                st.write('Hit `Get your plan` to start working on your posture!')

        else:
            st.markdown("#### Fantastic Posture! :raised_hands: :fire:\n The Posture Wizard is proud of you :male_mage: Keep up the good work!")

    else:
        st.write("Make sure you upload your picture!")

else:
    st.markdown(""" # Step Two """)
    st.write('Hit `Wizard evaluation` to classify your posture!!')


