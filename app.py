# app.py
from flask import Flask, render_template, request
from youtube_dl import YoutubeDL
from datetime import timedelta

app = Flask(__name__)

def get_playlist_info(playlist_url):
    ydl_opts = {'quiet': True, 'extract_flat': True}

    with YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)
        entries = playlist_info.get('entries', [])

        total_duration = sum(entry.get('duration', 0) for entry in entries)
        average_duration = total_duration / len(entries) if len(entries) > 0 else 0

        return {
            'length': len(entries),
            'total_duration': format_duration(total_duration),
            'average_duration': format_duration(round(average_duration))
        }

def format_duration(seconds):
    return str(timedelta(seconds=seconds))

@app.route('/', methods=['GET', 'POST'])
def index():
    playlist_info = None
    error_message = None

    if request.method == 'POST':
        playlist_url = request.form.get('playlist_url')

        try:
            playlist_info = get_playlist_info(playlist_url)
        except Exception as e:
            error_message = str(e)

        # Pass the playlist_url to the template
        return render_template('index.html', playlist_url=playlist_url, playlist_info=playlist_info, error_message=error_message)

    return render_template('index.html', playlist_url='', playlist_info=None, error_message=None)

if __name__ == "__main__":
    app.run(debug=True)
