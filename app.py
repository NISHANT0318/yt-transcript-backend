from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

app = Flask(__name__)
CORS(app) 

@app.route("/")
def hello():
    return "✅ Backend is running!"

@app.route("/get-transcript", methods=["GET"])
def get_transcript():
    video_id = request.args.get("videoId")
    if not video_id:
        return jsonify({"error": "Missing videoId"}), 400

    try:
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([item["text"] for item in transcript_data])
        return jsonify({"transcript": full_text})

    except TranscriptsDisabled:
        return jsonify({"error": "Transcript disabled for this video"}), 400
    except NoTranscriptFound:
        return jsonify({"error": "No transcript available"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
