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
            st = fmt_ass_time(chunk[0]["start"] - clip
