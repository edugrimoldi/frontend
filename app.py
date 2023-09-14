import streamlit as st
import requests
#from dotenv import load_dotenv
import json
import pandas as pd
import shutil
import base64

st.set_page_config(
            page_title="Gameplay Video Auto Edit",
            #page_icon="",
            layout="centered")

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Chakra+Petch&display=swap');
* {
    font-family: 'Chakra Petch', monospace, helvetica;
    font-weight: bold;
}

h1 {
    color: white;
    text-shadow: 4px 2px 6px #9aa19b;
}

.stApp {
    background-color: #021f06;
}
"""

st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

#load_dotenv()
url = 'https://auto-edit-vkmckhunoq-uc.a.run.app'

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
                    st.markdown("File processed succesfully! ✅")
                    response = res.json()
                    test_dict = json.loads(response)
                    df = pd.DataFrame.from_dict(test_dict)
                    csv = df.to_csv(header=False)
                    
                    st.markdown("---")

                    st.write("Your csv is ready!")

                    st.download_button(
                    "Download",
                    csv,
                    "file.csv",
                    "text/csv",
                    key='download-csv'
                    )

                else:
                    st.markdown("**Oops**, something went wrong 😓 Please try again.")
                    print(res.status_code, res.content)


st.markdown("---")
st.markdown('''


            > * **Visit** our [repo](http://github.com/edugrimoldi/auto-edit) in Github
            ''')
