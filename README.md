<div align="center">

# 🎬 VICECLIP AI

### Turn long videos into short, shareable clips — with AI.

**A free, notebook-powered video clipping studio by [My AI Files](https://myaifiles.in).**

[![Open in Google Colab](https://img.shields.io/badge/🚀_OPEN_IN_GOOGLE_COLAB-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white)](https://colab.research.google.com/github/myaifiles-labs/viceclip-ai/blob/main/ViceClip_AI.ipynb)
[![Community Beta](https://img.shields.io/badge/RELEASE-COMMUNITY_BETA-FF2E93?style=for-the-badge)](https://github.com/myaifiles-labs/viceclip-ai)
[![No Watermark Added](https://img.shields.io/badge/EXPORT-NO_ADDED_WATERMARK-19162B?style=for-the-badge)](https://github.com/myaifiles-labs/viceclip-ai)

**[Launch in Colab](https://colab.research.google.com/github/myaifiles-labs/viceclip-ai/blob/main/ViceClip_AI.ipynb)** · **[Get a Gemini API key](https://aistudio.google.com/apikey)** · **[Report an issue](https://github.com/myaifiles-labs/viceclip-ai/issues)**


[![YouTube](https://img.shields.io/badge/YouTube-Subscribe-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@myaifiles)
[![Instagram](https://img.shields.io/badge/Instagram-Follow-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/myaifiles/)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Join_Channel-128C4E?style=for-the-badge&logo=whatsapp&logoColor=white)](https://whatsapp.com/channel/0029Vb9YCE8CxoB0JLMuuW0N)

</div>

---

## ✨ What is ViceClip AI?

ViceClip AI is a browser-based editing interface launched **inside your own Google Colab runtime**. It helps you find interesting moments in longer videos, reframe them for short-form content, customize captions, and export video clips.

Your own **Gemini API key** powers AI-based clip suggestions. The current beta uses transcript analysis to suggest moments; it does **not** visually inspect gameplay to guarantee exciting highlights.

> **Free community beta:** No ViceClip subscription is required. Google Colab availability, GPU availability, Gemini quotas, and any provider charges are controlled by their respective providers.

## 🚀 Launch ViceClip AI

<div align="center">

<a href="https://colab.research.google.com/github/myaifiles-labs/viceclip-ai/blob/main/ViceClip_AI.ipynb"><img src="https://img.shields.io/badge/▶_OPEN_VICECLIP_IN_COLAB-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white" alt="Open ViceClip AI in Google Colab"></a>

</div>

1. **Open the notebook.** Tap the orange button above and sign in to Google if prompted.
2. **Select a runtime.** In Colab, use **Runtime → Change runtime type** and select a GPU if available. CPU mode may be slower.
3. **Run all cells.** Select **Runtime → Run all**. The notebook installs its dependencies and starts the studio automatically.
4. **Open the studio.** At the end of the notebook, tap the generated **ViceClip Studio** link.
5. **Connect Gemini.** In the **studio welcome screen**, choose **Get Free API Key** (opens Google AI Studio), create or copy your key, paste it into **Connect Gemini API**, and connect.
6. **Create clips.** Import a supported video or YouTube URL, generate clip suggestions, review and customize, then export.

**No API key needs to be pasted into notebook code or Colab Secrets.** The key is stored in the current Colab Python runtime memory, not intentionally saved to Google Drive or the browser. It is lost when that runtime ends.

### 📱 Using a phone?

Open the Colab link in your mobile browser. You'll still need to authorize and run the notebook in Colab before opening the mobile-responsive studio. Switching between the Colab and studio tabs is normal. Keep the Colab runtime connected while processing your videos.

## 🧰 Included in this beta

| Feature | What it does |
| :-- | :-- |
| 📥 Video input | Upload a video or import from a supported YouTube URL |
| 📝 Transcription | Faster-Whisper transcript with word timing |
| 🧠 AI moment suggestions | Gemini-assisted transcript-based clip selection |
| 🖼️ Reframing | Full screen, gaming split, dual speaker, and blur background |
| 🎨 Caption styling | Karaoke, word pop, classic, and boxed caption styles |
| 👀 Previews | Layout previews and caption previews |
| ✂️ Export | Vertical H.264/AAC clips with selectable render settings |
| 📦 Downloads | Download individual finished clips or a ZIP |
| 🔑 Frontend API setup | Enter your own Gemini key in the studio, not the notebook |

**Important:** Clip selection and framing are editing suggestions, not guarantees of virality. The beta is still under development; functionality and runtime compatibility may change.

## 🔐 Privacy & keys

- Use **your own** Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).
- ViceClip holds the key in memory for your **current Colab runtime**. When the runtime stops/restarts, reconnect it.
- Do not include personal API keys in screenshots, issues, notebook outputs, or public commits.
- Processing files are kept in the active Colab environment during the session. **Download exports before your runtime ends**; Colab storage is ephemeral.
- This project is intended for a single-user Colab session, **not a shared public production server**.

## ❓ Frequently asked questions

<details>
<summary><b>Do I need to install anything on my phone or laptop?</b></summary>

No local Python installation is required. You do need a Google account, a Colab runtime, a supported browser, and a Gemini API key.
</details>

<details>
<summary><b>Is it completely unlimited and always free?</b></summary>

No. ViceClip does not charge a subscription for this beta, but Google Colab may restrict or disconnect runtimes and Gemini API access has its own pricing and rate limits. See [Colab FAQ](https://research.google.com/colaboratory/faq.html) and [Gemini API pricing](https://ai.google.dev/gemini-api/docs/pricing).
</details>

<details>
<summary><b>Why does the generated studio link stop working?</b></summary>

The link connects to your current Colab runtime. If it disconnects, reconnect/restart the notebook and use its newly generated studio link.
</details>

<details>
<summary><b>Can I use any video I find online?</b></summary>

Only process videos you own or have permission to use. Creating clips does not remove third-party copyright obligations or guarantee YouTube monetization eligibility.
</details>

<details>
<summary><b>Can I use it without a GPU?</b></summary>

Some steps can fall back to CPU, but performance and availability vary by runtime. GPU is recommended for faster work.
</details>

## 🗺️ Community beta roadmap

The following are **planned**, not included in this release:

- Improved gallery thumbnails and mobile layouts
- More layout presets and facecam controls
- Expanded caption styles and output aspect ratios
- Runtime-session project history and multi-clip editing

## 🤝 Feedback and community

Found a bug or have a feature request? [Open an issue](https://github.com/myaifiles-labs/viceclip-ai/issues).

<div align="center">

**Built with ❤️ by My AI Files**

[![YouTube](https://img.shields.io/badge/YouTube-Subscribe-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@myaifiles)
[![Instagram](https://img.shields.io/badge/Instagram-Follow-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/myaifiles/)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-Join_Channel-128C4E?style=for-the-badge&logo=whatsapp&logoColor=white)](https://whatsapp.com/channel/0029Vb9YCE8CxoB0JLMuuW0N)

[Visit our website](https://myaifiles.in)

<sub>ViceClip AI Community Beta · Powered by your own Colab runtime and API key.</sub>

</div>
