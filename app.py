from flask import Flask, request, render_template_string
import threading
import yagmail
import os
import mashup   # importing your original file

app = Flask(__name__)

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

HTML = """
<h2>YouTube Mashup Generator</h2>
<form method="POST">
Artist Name:<br>
<input type="text" name="artist" required><br><br>

Number of Songs (>10):<br>
<input type="number" name="num_songs" min="11" required><br><br>

Duration (>20 sec):<br>
<input type="number" name="duration" min="21" required><br><br>

Email:<br>
<input type="email" name="email" required><br><br>

<button type="submit">Generate Mashup</button>
</form>
"""

def background_task(artist, num_songs, duration, email):

    output_file = "102303655-output.mp3"

    mashup.create_mashup(artist, int(num_songs), int(duration), output_file)

    yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)
    yag.send(
        to=email,
        subject="Your Mashup 🎵",
        contents="Here is your mashup file.",
        attachments=output_file
    )

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        artist = request.form["artist"]
        num_songs = request.form["num_songs"]
        duration = request.form["duration"]
        email = request.form["email"]

        thread = threading.Thread(
            target=background_task,
            args=(artist, num_songs, duration, email)
        )
        thread.start()

        return "Mashup started! You will receive email soon."

    return render_template_string(HTML)

if __name__ == "__main__":
    app.run()
