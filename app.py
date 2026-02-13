from flask import Flask, request, render_template_string
import threading
import os
import yagmail
import mashup

app = Flask(__name__)

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

HTML = """
<h2>Mashup Generator</h2>
<form method="POST">
Artist:<br>
<input name="artist"><br><br>

Number of Songs:<br>
<input name="num"><br><br>

Duration:<br>
<input name="duration"><br><br>

Email:<br>
<input name="email"><br><br>

<button type="submit">Generate</button>
</form>
"""

def background_task(artist, num, duration, email):

    output_file = "102303655-output.mp3"

    mashup.create_mashup(artist, int(num), int(duration), output_file)

    yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)
    yag.send(to=email, subject="Mashup Ready", attachments=output_file)

@app.route("/", methods=["GET","POST"])
def home():

    if request.method == "POST":
        artist = request.form["artist"]
        num = request.form["num"]
        duration = request.form["duration"]
        email = request.form["email"]

        threading.Thread(
            target=background_task,
            args=(artist,num,duration,email)
        ).start()

        return "Mashup started. Check email."

    return render_template_string(HTML)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
