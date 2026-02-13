import streamlit as st
import threading
import yagmail
from mashup import create_mashup


EMAIL_USER = st.secrets["EMAIL_USER"]
EMAIL_PASS = st.secrets["EMAIL_PASS"]

st.title("🎵 Mashup Generator")

artist = st.text_input("Artist Name")
num_songs = st.number_input("Number of Songs (>10)", min_value=11)
duration = st.number_input("Duration (>20 sec)", min_value=21)
email = st.text_input("Email ID")

# session states
if "status" not in st.session_state:
    st.session_state.status = "Idle"

if "progress" not in st.session_state:
    st.session_state.progress = 0


def run_process():
    st.session_state.status = "Downloading and processing songs..."
    st.session_state.progress = 20

    file = create_mashup(artist, num_songs, duration)

    st.session_state.status = "Sending Email..."
    st.session_state.progress = 80

    yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)
    yag.send(
        to=email,
        subject="Your Mashup 🎶",
        contents="Here is your mashup",
        attachments=file
    )

    st.session_state.status = "Completed ✅"
    st.session_state.progress = 100


if st.button("Generate Mashup"):

    if artist and email:

        thread = threading.Thread(target=run_process)
        thread.start()

    else:
        st.error("Please fill all fields.")


# -------- UI DISPLAY --------
st.write(st.session_state.status)
st.progress(st.session_state.progress)
