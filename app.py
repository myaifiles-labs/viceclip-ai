import os, json, re, uuid, shutil, subprocess, traceback, requests
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from faster_whisper import WhisperModel
from google import genai

app = FastAPI(title="ViceClip AI by MyAIFiles")
os.makedirs("sessions", exist_ok=True)
os.makedirs("fonts", exist_ok=True)

app.mount("/sessions", StaticFiles(directory="sessions"), name="sessions")

whisper_model = WhisperModel("base", device="auto", compute_type="int8")

GOOGLE_FONTS = {
    "Montserrat": "https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf",
    "Anton": "https://github.com/google/fonts/raw/main/ofl/anton/Anton-Regular.ttf",
    "Baloo 2": "https://github.com/google/fonts/raw/main/ofl/baloo2/Baloo2%5Bwght%5D.ttf",
    "Poppins": "https://github.com/google/fonts/raw/main/ofl/poppins/Poppins-Bold.ttf",
    "Oswald": "https://github.com/google/fonts/raw/main/ofl/oswald/Oswald%5Bwght%5D.ttf",
    "Bebas Neue": "https://github.com/google/fonts/raw/main/ofl/bebasneue/BebasNeue-Regular.ttf",
}

def ensure_font(font_name: str) -> str:
    safe_name = font_name.replace(" ", "_")
    font_path = f"fonts/{safe_name}.ttf"
    if not os.path.exists(font_path):
        url = GOOGLE_FONTS.get(font_name, GOOGLE_FONTS["Montserrat"])
        r = requests.get(url, timeout=15)
        with open(font_path, "wb") as f:
            f.write(r.content)
    return font_path

def hex_to_ass(hex_color: str, alpha: str = "00") -> str:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        hex_color = "FFFFFF"
    r, g, b = hex_color[0:2], hex_color[2:4], hex_color[4:6]
    return f"&H{alpha}{b}{g}{r}".upper()

def fmt_ass_time(sec: float) -> str:
    sec = max(0.0, sec)
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        s += 1
        cs = 0
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def build_ass_subtitles(words, clip_start, clip_end, style_mode, font_name, text_col, hi_col, bg_col, ass_path):
    c_primary = hex_to_ass(text_col, "00")
    c_highlight = hex_to_ass(hi_col, "00")
    c_bg = hex_to_ass(bg_col, "40")
    border_style = "3" if style_mode == "Karaoke Pill Box" else "1"
    outline_size = "10" if style_mode == "Karaoke Pill Box" else ("5" if style_mode == "Neon Vice Glow" else "4")
    shadow_size = "3" if style_mode == "Neon Vice Glow" else "1"
    back_col = c_bg if style_mode == "Karaoke Pill Box" else "&H80000000"

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{font_name},74,{c_primary},{c_highlight},&H00000000,{back_col},-1,0,0,0,100,100,0,0,{border_style},{outline_size},{shadow_size},2,60,60,340,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    clip_words = [w for w in words if w["end"] > clip_start and w["start"] < clip_end]
    chunks = [clip_words[i:i+3] for i in range(0, len(clip_words), 3)]
    events = []

    for chunk in chunks:
        if not chunk:
            continue
        if style_mode in ["Hormozi Pop (Word Highlight)", "Karaoke Pill Box"]:
            for idx, active_w in enumerate(chunk):
                st = fmt_ass_time(active_w["start"] - clip_start)
                en = fmt_ass_time(active_w["end"] - clip_start)
                parts = []
                for j, w in enumerate(chunk):
                    word_txt = re.sub(r"[^\w\s'!?.,-]", "", w["word"]).strip().upper()
                    if j == idx:
                        parts.append(f"{{\\c{c_highlight}\\fscx112\\fscy112}}{word_txt}{{\\c{c_primary}\\fscx100\\fscy100}}")
                    else:
                        parts.append(word_txt)
                events.append(f"Dialogue: 0,{st},{en},Default,,0,0,0,,{' '.join(parts)}")
        else:
            st = fmt_ass_time(chunk[0]["start"] - clip_start)
            en = fmt_ass_time(chunk[-1]["end"] - clip_start)
            line_txt = " ".join([re.sub(r"[^\w\s'!?.,-]", "", w["word"]).strip().upper() for w in chunk])
            events.append(f"Dialogue: 0,{st},{en},Default,,0,0,0,,{line_txt}")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events))

@app.post("/api/preview")
async def fetch_preview(yt_url: str = Form(""), video_file: UploadFile = File(None)):
    try:
        sid = uuid.uuid4().hex[:10]
        sdir = f"sessions/{sid}"
        os.makedirs(sdir, exist_ok=True)
        input_video = f"{sdir}/source.mp4"
        preview_img = f"{sdir}/preview.jpg"

        if yt_url and yt_url.strip():
            cmd = [
                "yt-dlp",
                "--extractor-args", "youtube:player_client=android,ios",
                "-f", "best[height<=720][ext=mp4]/best[ext=mp4]/best",
                "-o", input_video,
                yt_url.strip()
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0 or not os.path.exists(input_video):
                return JSONResponse({"ok": False, "error": f"YouTube fetch failed: {res.stderr[-300:]}"})
        elif video_file is not None:
            with open(input_video, "wb") as f:
                f.write(await video_file.read())
        else:
            return JSONResponse({"ok": False, "error": "Please enter a YouTube URL or upload an MP4 video."})

        subprocess.run(["ffmpeg", "-y", "-ss", "00:00:05", "-i", input_video, "-vframes", "1", "-q:v", "2", preview_img], check=True)
        probe = subprocess.check_output([
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height", "-of", "json", input_video
        ]).decode()
        dims = json.loads(probe)["streams"][0]
        return JSONResponse({
            "ok": True,
            "session_id": sid,
            "preview_url": f"/{preview_img}",
            "width": dims["width"],
            "height": dims["height"]
        })
    except Exception:
        return JSONResponse({"ok": False, "error": traceback.format_exc()[-400:]})

@app.post("/api/generate")
async def generate_clips(
    session_id: str = Form(...),
    api_key: str = Form(...),
    num_clips: int = Form(3),
    min_dur: int = Form(25),
    max_dur: int = Form(55),
    vibe: str = Form("Viral Hooks & High Retention"),
    layout_mode: str = Form("single"),
    game_box: str = Form("{}"),
    face_box: str = Form("{}"),
    cap_enabled: str = Form("true"),
    cap_style: str = Form("Hormozi Pop (Word Highlight)"),
    font_family: str = Form("Montserrat"),
    text_color: str = Form("#FFFFFF"),
    highlight_color: str = Form("#FFE600"),
    bg_color: str = Form("#FF2A85")
):
    try:
        safe_sid = re.sub(r"[^a-zA-Z0-9]", "", session_id)
        sdir = f"sessions/{safe_sid}"
        input_video = f"{sdir}/source.mp4"
        input_audio = f"{sdir}/audio.wav"
        if not os.path.exists(input_video):
            return JSONResponse({"ok": False, "error": "Session expired or video not loaded. Please fetch video in Step 1 first."})

        subprocess.run(["ffmpeg", "-y", "-i", input_video, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", input_audio], check=True)
        segments, _ = whisper_model.transcribe(input_audio, word_timestamps=True)
        all_words = []
        transcript_lines = []
        for seg in segments:
            transcript_lines.append(f"[{seg.start:.1f}s - {seg.end:.1f}s]: {seg.text}")
            if seg.words:
                for w in seg.words:
                    all_words.append({"word": w.word, "start": w.start, "end": w.end})

        full_transcript = "\n".join(transcript_lines)
        client = genai.Client(api_key=api_key.strip())
        prompt = f"""
        You are an expert viral Shorts/Reels editor.
        Analyze the transcript below and extract the top {num_clips} viral clips.
        - Focus style: {vibe}
        - Each clip MUST be between {min_dur} and {max_dur} seconds long.
        - Never cut mid-sentence; start on a strong hook and end on a punchline.
        Return ONLY valid JSON list: [{{"title": "Hook Title", "start": 12.0, "end": 42.5, "reason": "Why it goes viral"}}]

        Transcript:
        {full_transcript[:28000]}
        """
        ai_res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
        clean_json = ai_res.text.strip().removeprefix("```json").removesuffix("```").strip()
        clips_data = json.loads(clean_json)

        ensure_font(font_family)
        g_box = json.loads(game_box)
        f_box = json.loads(face_box)
        results = []

        for idx, c in enumerate(clips_data, 1):
            st = float(c["start"])
            en = float(c["end"])
            dur = max(5.0, en - st)
            out_file = f"{sdir}/vice_clip_{idx}.mp4"
            ass_file = f"{sdir}/sub_{idx}.ass"

            if layout_mode == "split" and g_box and f_box:
                vf_base = (
                    f"[0:v]crop=iw*{g_box['w']}:ih*{g_box['h']}:iw*{g_box['x']}:ih*{g_box['y']},scale=1080:1152:force_original_aspect_ratio=increase,crop=1080:1152[top];"
                    f"[0:v]crop=iw*{f_box['w']}:ih*{f_box['h']}:iw*{f_box['x']}:ih*{f_box['y']},scale=1080:768:force_original_aspect_ratio=increase,crop=1080:768[bot];"
                    f"[top][bot]vstack=inputs=2[vout]"
                )
            else:
                vf_base = "[0:v]crop=ih*9/16:ih,scale=1080:1920[vout]"

            if cap_enabled == "true" and all_words:
                build_ass_subtitles(all_words, st, en, cap_style, font_family, text_color
