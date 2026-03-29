import os
import whisper
import tempfile
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB limit

ALLOWED_EXTENSIONS = {'mp3', 'mp4', 'wav', 'm4a', 'ogg', 'webm', 'flac', 'mkv', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format: HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def segments_to_srt(segments):
    """Convert Whisper segments to SRT format."""
    srt_lines = []
    for i, seg in enumerate(segments, 1):
        start = format_timestamp(seg['start'])
        end = format_timestamp(seg['end'])
        text = seg['text'].strip()
        srt_lines.append(f"{i}\n{start} --> {end}\n{text}\n")
    return "\n".join(srt_lines)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/models')
def get_models():
    return jsonify(['tiny', 'base', 'small', 'medium', 'large'])

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Unsupported file type'}), 400

    model_name = request.form.get('model', 'base')
    language = request.form.get('language', None) or None

    # Save uploaded file to temp location
    suffix = '.' + secure_filename(file.filename).rsplit('.', 1)[-1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    try:
        print(f"[Whisper] Loading model: {model_name}")
        model = whisper.load_model(model_name)

        print(f"[Whisper] Transcribing: {file.filename}")
        options = {}
        if language:
            options['language'] = language

        result = model.transcribe(tmp_path, **options)

        srt = segments_to_srt(result['segments'])
        detected_lang = result.get('language', 'unknown')
        word_count = len(result['text'].split())
        segment_count = len(result['segments'])

        return jsonify({
            'srt': srt,
            'language': detected_lang,
            'word_count': word_count,
            'segment_count': segment_count,
            'filename': secure_filename(file.filename).rsplit('.', 1)[0]
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        os.unlink(tmp_path)

if __name__ == '__main__':
    print("\n🎙️  Whisper SRT Generator")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("✅ Open your browser at: http://localhost:5000")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    app.run(debug=False, port=5000)
