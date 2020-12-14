from SessionState import get
import streamlit as st
from theposturewizard import utils
from re import search
import os
from io import BytesIO
from PIL import Image
import requests
import urllib.request


PATH_TO_IMG = "notebooks/img 5 K.jpg"
PATH_TO_MODEL = "models/rv1-VGG16-test"
APPARATUS = "Bodyweight"
PART_OF_BODY = "Shoulders"

model = utils.load_my_model(PATH_TO_MODEL)


def get_pictures(exercice):
    my_dict = {}
    for k, v in exercice.items():
        if v.endswith(".jpg"):
            my_dict[k] = v

    if 'Larg_Img_1' in my_dict.keys():
        if 'Small_Img_1' in my_dict.keys():
            del my_dict['Small_Img_1']

    if 'Larg_Img_2' in my_dict.keys():
        if 'Small_Img_2' in my_dict.keys():
            del my_dict['Small_Img_2']

    return list(my_dict.values())

def get_video(exercice):
    if 'https://player' in exercice['video_src']:
        return exercice['video_src']


def info(exercice):
    # name
    st.markdown(f"""### {exercice['Exercise_Name_Complete_Abbreviation']}""")

    # instruction
    st.markdown(f"""
        **Instructions And Preparation:**\n
        {exercice['Instructions_Preparation']}""")

    # pictures
    pictures = get_pictures(exercice)
    i
    for picture in pictures:
        url = 'http://' + picture[2:]
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        st.image(img, use_column_width=True)

    # video
    video = get_video(exercice)
    if video:
        vid = urllib.request.urlretrieve(video, 'video_name.m3u8')
        st.video(vid, format='video/m3u8', start_time=0)
        st.write(f"{video}")

def get_input_img():
    uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg'])

    if uploaded_file:
        pos = Image.open(uploaded_file)
        cols = st.beta_columns(5)
        with cols[2]:
            st.image(pos, use_column_width=True)
    return uploaded_file


# STREAMLIT PAGE
params = {'get_prediction':False, 'file_name':'hello'}
session_state = get(**params)
st.write(session_state.file_name)

'''
# The Posture Wizard
'''

st.markdown("""Upload your picture""")

uploaded_file = get_input_img()

if uploaded_file:
    if uploaded_file.name != session_state.file_name:
        session_state.get_prediction = False
        session_state.file_name = uploaded_file.name


if st.button('Get prediction') or session_state.get_prediction:
    session_state.get_prediction = True

    if uploaded_file:

        pred = utils.pipe(uploaded_file, model)
        st.write(f"Your posture: {pred}")

        if pred == "kyphosis":
            st.write("**Customize your plan! : **")

            bodypart = st.selectbox('Select a bodypart you want to work on', ['Shoulders', 'Neck'])

            if bodypart == 'Shoulders':
                apparatus = st.selectbox('Select an apparatus', ['Bodyweight', 'Dumbbell', 'Cable'])

            else:
                apparatus = 'Bodyweight'

            if st.button('Get your plan!'):
                #TODO stretch, strength = utils.main(apparatus, bodypart)

                # stretch
                st.markdown(f"""## 1. Stretching Exercise""")

                info(stretch[0])

                """


                """

                # strength
                st.markdown(f"""## 2. Strengthening Exercises""")

                # strength 1
                info(strength[0])

                """

                """

                # strength 2
                info(strength[1])
            else:
                st.write('Hit `Get your plan` to start working on your posture!')

        else:
            st.write("Do you still want to work on your posture?")

    else:
        st.write("Make sure you upload your picture!")

else:
    st.write('Hit `Get prediction` to classify your posture!!')

#st.markdown(f"""{stretch}""")

#st.markdown(f"""{strength}""")
