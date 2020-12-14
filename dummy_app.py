import streamlit as st
import datetime
import requests
import pandas as pd
import cv2
import numpy as np
'''
# Drafts
'''
if st.checkbox('Give me an advice'):
   st.write('Walking often is essentail for great health and a long life ;)')

def tryer(astring):
    return astring + " from streamlit"

st.write(tryer("heeyy"))

uploaded_file = st.file_uploader("Choose a image file", type="jpg")

if uploaded_file is not None:
    # Convert the file to an opencv image.
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)

    # Now do something with the image! For example, let's display it:
    st.image(opencv_image, channels="BGR")
