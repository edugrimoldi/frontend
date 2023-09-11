import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd

st.set_page_config(
            page_title="Video Auto Edit",
            #page_icon="",
            layout="centered")

# Example local Docker container URL
# url = 'http://api:8000'
# Example localhost development URL
# url = 'http://localhost:8000'
load_dotenv()
url = os.getenv('API_URL')

# App title and description
st.header('Video Auto Edit')
st.markdown('''
            > This app will return the best clips of your video
            ''')

st.markdown("---")

# Create a native Streamlit file upload input
st.markdown("Choose a video from your computer 👇")
st.set_option('deprecation.showfileUploaderEncoding', False)

# By default, uploaded files are limited to 200MB. You can configure this using the server.maxUploadSize config option

uploaded_file = st.file_uploader("Upload a .mp4 file", type="mp4")

if uploaded_file is not None:
    st.video(uploaded_file)
    st.write("Uploaded succesfully")
    
    if st.button('Process the video'):
        with st.spinner("Wait for it..."):
            ### Get bytes from the file buffer
            video_bytes = uploaded_file.getvalue()
            
            ### Make request to  API (stream=True to stream response as bytes)
            res = requests.post(url + "/predict", data=uploaded_file)

            if res.status_code == 200:
                n_shots = st.slider('Select the number of shots', 1, 10, 3)              
                
                @st.cache
                def get_dataframe_data():
                    return pd.DataFrame(res)

                df = get_dataframe_data()
                hdf = df.assign(hack='').set_index('hack')
                   
                @st.cache
                def convert_df(df):
                    return df.to_csv(index=False).encode('utf-8')

                csv = convert_df(hdf)

                st.download_button(
                    "Download the .csv file",
                    csv,
                    "file.csv",
                    "text/csv",
                    key='download-csv'
                )
                
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