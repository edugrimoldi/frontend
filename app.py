import streamlit as st
import requests
#from dotenv import load_dotenv
import json
import pandas as pd
import shutil
import base64

st.set_page_config(
            page_title="Video Auto Edit",
            #page_icon="",
            layout="centered")

#load_dotenv()
url = 'http://127.0.0.1:8000'

# App title and description
st.header('Video Auto Edit')
st.markdown('''
            > This app will return the best clips of your gameplay video
            ''')

st.markdown("---")

# Create a native Streamlit file upload input
st.markdown("Choose a video from your computer 👇")

st.set_option('deprecation.showfileUploaderEncoding', False)

uploaded_file = st.file_uploader("Upload a .mp4 file", type="mp4")


@st.cache
def dataframe_to_csv(data):
    df = pd.DataFrame(data)
    return df.to_csv().encode('utf-8')

if uploaded_file is not None:
    #st.video(uploaded_file)
    st.write("Uploaded succesfully")

    if st.button('Process the video'):
        with st.spinner("Wait for it..."):
            ### Get bytes from the file buffer
            video_bytes = uploaded_file.read()

            files = {'file': video_bytes}

            ### Make request to the API
            with requests.post(url + "/predict", files=files, stream=True) as res:

                if res.status_code == 200:
                    res_string = res.json()
                    res_df = dataframe_to_csv(res_string)
                    
                    locals_filename = "markers_file.csv"

                    with open(locals_filename, 'wb') as f:
                        shutil.copyfileobj(res.json, f)


                    st.download_button(
                        label="Download markers as .CSV",
                        data=res_df,
                        file_name='markers_file.csv',
                        mime='text/csv')

                else:
                    st.markdown("**Oops**, something went wrong 😓 Please try again.")
                    print(res.status_code, res.content)

st.markdown('''
            > **What's here:**

            > * [Streamlit](https://docs.streamlit.io/) on the frontend
            > * [FastAPI](https://fastapi.tiangolo.com/) on the backend
            > * TO CHANGE -> [PIL/pillow](https://pillow.readthedocs.io/en/stable/) and [opencv-python](https://github.com/opencv/opencv-python) for working with images

            > Built with
            > * **Visit** our [repo](http://github.com/edugrimoldi/frontend) in Github
            ''')
