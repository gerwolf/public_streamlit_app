import streamlit as st
from streamlit.components.v1 import html
import joblib
from io import BytesIO
import requests
import pandas as pd
import spotipy
import spotipy.oauth2 as oauth2

CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]

credentials = oauth2.SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET)

spotify = spotipy.Spotify(client_credentials_manager=credentials)

#model download-link
download_link = "https://drive.google.com/u/0/uc?id=1-9AQpKetdu_7Wkag6yMPMmeKUDII237b&export=download"
response = requests.get(download_link)
model = joblib.load(BytesIO(response.content))

var_order =  ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']

with st.form("spotify_form", clear_on_submit=True):

  track_id = st.text_input(label = "Track ID", value="0OInqhDtfYPcSpEQNtJx3n", max_chars=22, help="Enter a valid 22 characters Track ID...")
  # try a different track id: 084VIjlHRPMiHPlrfca65S
  submit = st.form_submit_button("Submit")

  if submit:
    # st.write(submit)
    
    if track_id:
      st.success(f"Selected Track ID is: {track_id}")
      # st.write('Selected Track ID is ', f"{track_id}")
      iframe_text = f'<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/{track_id}?utm_source=generator" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>'
      st.components.v1.html(iframe_text, height = 160) # or height = 352

      res = spotify.audio_features(track_id)[0]
      sorted_dict = [{key: res[key] for key in var_order}] # need to provide a list for pd.DataFrame()
      X = pd.DataFrame(sorted_dict)

      pred = model.predict(X)[0]

      if pred == 'winner':
        st.write('This track could be the next *ESC winner*! :grinning_face_with_star_eyes:')
        st.balloons()
        
      else:
        st.write('This track is probably not going to win the ESC...')

    else:
      st.warning("Please enter a valid Track ID.")
