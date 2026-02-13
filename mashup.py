import sys
import os
from yt_dlp import YoutubeDL
from moviepy.editor import AudioFileClip, concatenate_audioclips
import moviepy.config as mp_config


# -------------------------------------------------
# Configure Local FFmpeg
# -------------------------------------------------
ffmpeg_path = os.path.join(os.getcwd(), "ffmpeg", "bin")
mp_config.change_settings({
    "FFMPEG_BINARY": os.path.join(ffmpeg_path, "ffmpeg.exe")
})


# -------------------------------------------------
# Mashup Function
# -------------------------------------------------
def create_mashup(singer_name, num_videos, duration, output_filename):

    temp_dir = "temp_audio"
    os.makedirs(temp_dir, exist_ok=True)

    print(f"Downloading {num_videos} songs of {singer_name}...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
        'restrictfilenames': False,
        'ffmpeg_location': ffmpeg_path,

        'js_runtimes': {'node': {}},
        'remote_components': ['ejs:github'],
        'extractor_args': {'youtube': {'player_client': ['android']}},

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }


    try:
        # ---------------- Download Audio ----------------
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"ytsearch{num_videos}:{singer_name} songs"])

        # ---------------- Process Audio ----------------
        audio_clips = []
        files = [f for f in os.listdir(temp_dir) if f.endswith('.mp3')]

        print(f"Processing {len(files)} audio files...")

        for file in files:
            path = os.path.join(temp_dir, file)

            clip = AudioFileClip(path)

            # Prevent crash if audio shorter than duration
            clip = clip.subclip(0, min(duration, clip.duration))

            audio_clips.append(clip)

        if not audio_clips:
            print("No audio files processed.")
            return

        # ---------------- Merge Audio ----------------
        print("Creating mashup...")
        final_audio = concatenate_audioclips(audio_clips)
        final_audio.write_audiofile(output_filename)

        # Close clips
        final_audio.close()
        for clip in audio_clips:
            clip.close()

        print(f"✅ Mashup saved as: {output_filename}")

    except Exception as e:
        if "Maximum number of downloads reached" in str(e):
            print("✔ Required number of videos downloaded.")
        else:
            print(f"❌ Error occurred: {e}")


    finally:
        # ---------------- Cleanup ----------------
        if os.path.exists(temp_dir):
            for f in os.listdir(temp_dir):
                try:
                    os.remove(os.path.join(temp_dir, f))
                except:
                    pass
            try:
                os.rmdir(temp_dir)
            except:
                pass


# -------------------------------------------------
# Main Driver Code
# -------------------------------------------------
if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("Usage:")
        print("python 102303655.py <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        print('Example:')
        print('python 102303655.py "Arijit Singh" 12 25 mashup.mp3')
        sys.exit(1)

    try:
        singer = sys.argv[1]
        n_videos = int(sys.argv[2])
        duration = int(sys.argv[3])
        output = sys.argv[4]

        if n_videos <= 10:
            print("Error: Number of videos must be greater than 10")
            sys.exit(1)

        if duration <= 20:
            print("Error: Duration must be greater than 20 seconds")
            sys.exit(1)

        if not output.endswith(".mp3"):
            print("Error: Output file must be .mp3")
            sys.exit(1)

        create_mashup(singer, n_videos, duration, output)

    except ValueError:
        print("Error: Number of videos and duration must be integers.")
