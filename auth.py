import pyrebase
import streamlit as st

firebase_config = {
    "apiKey": st.secrets["firebase_api_key"],
    "authDomain": f"{st.secrets['firebase']['project_id']}.firebaseapp.com",
    "projectId": st.secrets["firebase"]["project_id"],
    "storageBucket": f"{st.secrets['firebase']['project_id']}.appspot.com",
    "messagingSenderId": st.secrets["firebase_messaging_sender_id"],
    "appId": st.secrets["firebase_app_id"],
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()