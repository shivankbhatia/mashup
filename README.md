# YouTube Mashup Generator

* Web-based application that automatically creates a mashup of songs from a specified artist by downloading audio from YouTube, trimming each track to a fixed duration, merging them into a single MP3 file, and delivering the final mashup to the user via email.

---

## Live Website

Click Here: https://mashup-esco.onrender.com/

---

## Project Overview

This project allows users to:

- Enter an artist name
- Specify number of songs (greater than 10)
- Specify duration per song (greater than 20 seconds)
- Provide an email address

The system then:

1. Searches YouTube for songs of the artist
2. Downloads audio using `yt-dlp`
3. Converts audio to MP3 using `FFmpeg`
4. Trims each song to the specified duration
5. Merges all clips into a single mashup
6. Sends the final MP3 file to the user's email

---

## Technologies Used

- **Python**
- **Flask** (Web framework)
- **yt-dlp** (YouTube downloader)
- **MoviePy** (Audio processing & merging)
- **FFmpeg** (Audio conversion backend)
- **Yagmail** (Email sending via Gmail)
- **Gunicorn** (Production WSGI server)
- **Render** (Cloud hosting platform)

---

## Working

### Step 1 – User Input
User provides:
- Artist Name
- Number of Songs (> 10)
- Duration per Song (> 20 seconds)
- Email ID

### Step 2 – YouTube Search
The application uses: `ytsearchN:<artist> songs` to fetch relevant tracks.

### Step 3 – Audio Processing
For each downloaded track:
- Convert to MP3
- Trim to specified duration
- Store temporarily

### Step 4 – Mashup Creation
All trimmed clips are concatenated using MoviePy into: `102303655-output.mp3`.

### Step 5 – Email Delivery
The final MP3 file is emailed to the provided address.

---

## Issue:
  -  Youtube does not allow to fetch video details repeatedly from the  deployed server, it treats it as a bot and  refuses.
  -  The service might not work as it should sometimes due to this issue.
  -  The hereby attached `102303655-output.mp3` is the sample output the code generated on the input:
     `python  102303655.py "Michael  Jackson" 15 30 102303655-output.mp`
