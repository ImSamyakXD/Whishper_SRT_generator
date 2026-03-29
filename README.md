# 🎙️ Whisper SRT Generator (Local & Free)

Generate SRT subtitle files from any audio/video — runs 100% on your machine.
No API key. No cost. No internet needed after setup.

---

## ⚡ Setup (One Time)

### Step 1 — Install Python
Make sure Python 3.8+ is installed: https://www.python.org/downloads/

### Step 2 — Install dependencies
Open a terminal in this folder and run:

```bash
pip install -r requirements.txt
```

> This also installs ffmpeg bindings. If you get ffmpeg errors, install it separately:
> - **Windows**: `winget install ffmpeg`
> - **Mac**: `brew install ffmpeg`
> - **Linux**: `sudo apt install ffmpeg`

---

## ▶️ Run the App

```bash
python app.py
```

Then open your browser at: **http://localhost:5000**

---

## 🎛️ Model Guide

| Model  | Size   | Speed  | Accuracy |
|--------|--------|--------|----------|
| tiny   | 39 MB  | ⚡⚡⚡⚡ | ★★☆☆☆   |
| base   | 74 MB  | ⚡⚡⚡  | ★★★☆☆   |
| small  | 244 MB | ⚡⚡    | ★★★★☆   |
| medium | 769 MB | ⚡      | ★★★★☆   |
| large  | 1.5 GB | 🐢      | ★★★★★   |

> Models are downloaded automatically on first use and cached locally.

---

## 📁 Supported Formats
MP3, WAV, M4A, OGG, FLAC, MP4, MKV, MOV, WEBM, AVI

## ✅ Features
- Drag & drop upload
- Language selection (or auto-detect)
- SRT preview with syntax highlighting
- One-click download of `.srt` file
- Files never leave your machine
