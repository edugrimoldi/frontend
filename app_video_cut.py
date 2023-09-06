import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd
from moviepy.editor import VideoFileClip

st.set_page_config(
            page_title="Quick reference", # => Quick reference - Streamlit
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

st.markdown("Choose a video from your computer 👇")

st.set_option('deprecation.showfileUploaderEncoding', False)
# Create a file upload input
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
            res = requests.post(url + "/upload_video", files={'video': video_bytes})

            if res.status_code == 200:
                ### Display the clip returned by the API
                st.write('Processed successfully 🎉')
                
                # Show processed video          
                @st.cache
                def generate_clips(res, video):
                    """Take the HTTP response and the video and returns the resulting clips"""
                    results = pd.DataFrame(res, columns=["Number_of_shoots", "Sec"])
                    
                    ## Simulate the process 
                    video_file = 'video_used_in_the_post_process.mp4'
                    videoclip = VideoFileClip(video_file)
                    
                    step_size = 1
                    clip_list = {}
                    set_start = 0
                    counter = 0
                    set_end = 0

                    for index, row in results.iterrows():
                        if row['Number_of_shoots'] > 0:
                            if set_start == 0:
                                set_start = index
                            else:
                                set_end = index
                        else:
                            if counter <= step_size:
                                counter +=1
                            else:
                                counter = 0
                                clip_list[set_start]=set_end
                                set_start = 0
                                set_end = 0
                        
                    for start, end in clip_list.items():
                        final_clip = videoclip.subclip(start, end)
                        final_clip.write_videofile(f"output/{start}sec-{end}sec.mp4", fps=60)

                clips = generate_clips(res, uploaded_file)

                st.download_button(
                    label="Download the clips",
                    data=clips,
                    file_name='auto_edit_clips.zip',
                    mime='application/zip')
            else:
                st.markdown("**Oops**, something went wrong 😓 Please try again.")
                print(res.status_code, res.content)
        

st.markdown("---")
  
st.markdown('''
            > **What's here:**

            > * [Streamlit](https://docs.streamlit.io/) on the frontend
            > * [FastAPI](https://fastapi.tiangolo.com/) on the backend
            > * TO CHANGE -> [PIL/pillow](https://pillow.readthedocs.io/en/stable/) and [opencv-python](https://github.com/opencv/opencv-python) for working with images
            > * **Visit** our [repo](http://github.com/edugrimoldi/frontend) in Github
            ''')
        




    
    