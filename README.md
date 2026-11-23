<div align="center">

  <h1>🎬 VICECLIP AI</h1>
  <p><strong>Free, Open-Source AI YouTube Shorts & Reels Clipper (Zero Watermark)</strong></p>
  <p>Turn long-form YouTube videos or MP4s into viral 9:16 vertical clips with AI hook detection, dynamic word-by-word captions, and split-screen gaming/reaction framing.</p>

  <!-- Clickable Badges -->
  <p>
    <a href="https://colab.research.google.com/github/myaifiles-labs/viceclip-ai/blob/main/ViceClip_AI.ipynb" target="_blank">
      <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" height="28"/>
    </a>
    <a href="https://github.com/myaifiles-labs/viceclip-ai/stargazers">
      <img src="https://img.shields.io/github/stars/myaifiles-labs/viceclip-ai?style=for-the-badge&color=ff2a85&labelColor=0d0714" alt="GitHub Stars" height="28"/>
    </a>
    <a href="https://github.com/myaifiles-labs/viceclip-ai/blob/main/LICENSE">
      <img src="https://img.shields.io/badge/License-MIT-00f0ff?style=for-the-badge&labelColor=0d0714" alt="MIT License" height="28"/>
    </a>
    <a href="https://myaifiles.in">
      <img src="https://img.shields.io/badge/Website-myaifiles.in-ff9e00?style=for-the-badge&labelColor=0d0714" alt="MyAIFiles" height="28"/>
    </a>
  </p>

  <br/>

  <!-- App UI Mockup Preview -->
  <img src="assets/preview.png" alt="ViceClip AI Mobile & Desktop UI Preview" width="720" style="border-radius: 16px;" />

</div>

---

## 🔥 Why ViceClip AI vs Paid Tools?

| Feature | **ViceClip AI (Free)** | **Paid AI Clippers (\$19–\$49/mo)** |
| :--- | :---: | :---: |
| **Watermark** | ❌ **Zero Watermark** | ⚠️ Watermark on Free Plan |
| **Monthly Subscription** | ✅ **₹0 / \$0 Forever** | ❌ \$19 – \$49 / month |
| **AI Viral Hook Detection** | ✅ **Gemini 2.5 Flash** | ✅ Proprietary |
| **Word-by-Word Captions** | ✅ **Hormozi, Karaoke Pill, Neon** | ✅ Paid Tier Only |
| **Google Fonts & Colors** | ✅ **Full Live Customizer** | ⚠️ Limited on Free |
| **Gaming + Facecam Split** | ✅ **Drag & Drop Dual Boxes** | ❌ Paid Pro Feature |
| **Runs On** | 📱 **Android, iOS, Windows, macOS** | 🌐 Web Only |

---

## ⚡ 1-Click Launch (No Installation Required)

Run **ViceClip AI** directly in your browser using Google Colab's free cloud runtime:

1. Click the **`Open In Colab`** badge above (or open [Google Colab](https://colab.research.google.com/)).
2. Run the single cell (`▶`) and click the generated link to open the **ViceClip AI Studio**:

```python
!git clone [https://github.com/myaifiles-labs/viceclip-ai.git](https://github.com/myaifiles-labs/viceclip-ai.git) && cd viceclip-ai && pip install -q -r requirements.txt && python -c "from google.colab.output import eval_js; print('👉 Launch ViceClip AI:', eval_js('google.colab.kernel.proxyPort(8000)'))" && uvicorn app:app --host 0.0.0.0 --port 8000
