import requests
import pandas as pd
from re import search
import json
import random
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model



# model
def load_my_model(path):
    model = load_model(path)
    return model

def get_proc(path):
    width = 75
    height = 150

    img = Image.open(path)
    img = img.resize((width, height), resample=1)
    img = img_to_array(img)
    img = img/255
    img = img.astype('float32')
    img = np.expand_dims(img, axis=0)

    return img

# prediction
def get_pred(img, model):
    return model.predict(img)[0,0]


# post_process
def post_process(pred):
    labels = ['good', 'kyphosis']
    threshold = 0.5

    if pred >= threshold:
        index = 1

    else:
        index = 0

    return labels[index]


def pipe(path, model):
    img = get_proc(path)
    pred = get_pred(img, model)
    label = post_process(pred)

    return label


# get exercises with API

def get_token(username,password):
    response = requests.post('http://204.235.60.194/consumer/login', data={'username':username, 'password':password})
    token =response.json()
    return token


def request(param, token, n_exercise):
    url = 'http://204.235.60.194/exrxapi/v1/allinclusive/exercises?'
    keys_to_extract = ['Apparatus_Name','Exercise_Name_Complete_Abbreviation','Small_Img_1','Small_Img_2','Larg_Img_1','Larg_Img_2',\
                       'Instructions_Preparation','Instructions_Execution','video_src','GIF_Img']

    response = requests.get(url, params=param, headers={'Authorization': "Bearer "+token['token']})
    response = json.loads(response.text)['exercises']

    exercices = np.random.choice(response,n_exercise,replace=False)
    ex_list = [dict((key, value) for (key, value) in exercice.items() if key in keys_to_extract) for exercice in exercices]

    return ex_list


def main(apparatus, part_of_body):
    token = get_token('raneenaexrx','StKhg6Zu')
    stretch_params = {'stretch':'', 'bodypart':[part_of_body]}
    strength_params = {'bodypart':[part_of_body], 'apparatus':[apparatus]}

    response_stretch = request(stretch_params, token,1)
    response_strength = request(strength_params, token,2)

    return response_stretch, response_strength


def get_pictures(exercices):
    my_list_full = []
    for exercice in exercices:
        my_list = []
        for k, v in exercice.items():
            if search("Img", k) and v.endswith(".jpg"):
                my_list.append(v)
        my_list_full.append(my_list)
    return my_list_full


# get exercises with csv

def get_exercises(apparatus, body_part):
    # get csv
    df = pd.read_csv('Exercises - Sheet1.csv')

    # get stretch exercise
    stretchs = df[(df['Exercise_type'] == 'Stretch')\
                   & (df['Body_part'] == body_part)]
    stretch = stretchs.loc[np.random.choice(stretchs.index,1,replace=False)].reset_index(drop=True)

    # get strength exercise
    strengths = df[(df['Exercise_type'] == 'Strength')\
                   & (df['Body_part'] == body_part)\
                   & (df['Apparatus'] == apparatus)]
    strength = strengths.loc[np.random.choice(strengths.index,2,replace=False)].reset_index(drop=True)

    return stretch.loc[0], strength.loc[0], strength.loc[1]


if __name__ == "__main__":
    path_to_img = "../notebooks/img 5 K.jpg"
    path_to_model = "../models/rv1-VGG16-test"
    apparatus = "Bodyweight"
    part_of_body = "Shoulders"
    stretch, strength = activate(path_to_img, apparatus, part_of_body, load_my_model(path_to_model))
    print(stretch)
    print(strength)

