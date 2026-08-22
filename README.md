# 🎬 GABRIEL'S WORK Text to Subtitles MP4 v2.0.0

Create Full HD (16:9) and Vertical (9:16) green-screen MP4 subtitle videos from plain text in 76 languages with automated reading speed calculations.

Text-to-Subtitles MP4 Generator automatically calculates reading time from your text, lets you adjust the reading pace by **±50%**, provides a live preview, and exports **Full HD 1920×1080** and **Vertical 9:16** MP4 videos ready for use in video editors.

The green-screen output can be used with **Clipchamp, CapCut, Premiere Pro, DaVinci Resolve**, and other video editing software.

---

## 📋 Overview

**Text-to-Subtitles MP4 Generator** is a free Windows desktop application designed to automate subtitle video creation.

Unlike traditional subtitle tools that require pre-recorded audio to synchronize text, this application calculates the subtitle timeline directly from a plain text file (`.txt`).

It generates a **30 FPS MP4 video** in:

* **Full HD 1920×1080 (16:9)**
* **Vertical 9:16**

The video uses a green chroma-key background (`#126e47`), allowing you to remove the background quickly in your preferred video editor.

---

## ✨ Key Features

### 🌍 Multilingual Support — 76 Languages

Supports **76 languages** and multiple writing systems, including:

* Latin
* Cyrillic
* Chinese
* Japanese
* Korean
* Arabic
* Persian
* Urdu
* Indic scripts
* Thai
* Lao
* Burmese
* Hebrew
* Georgian
* Armenian
* Amharic

The application automatically selects the appropriate Windows font configuration for the selected writing system.

---

### 🎚️ Dynamic Time Adjustment

Adjust the overall reading pace by **±50%** using the speed slider.

This allows you to adapt subtitle timing to different voiceovers and video formats without modifying the original text.

---

### 👀 Live Preview

Preview your subtitle blocks before exporting.

The application includes:

* Live preview
* Play
* Pause
* Resume
* Reset
* Timeline navigation
* Progress indicator

---

### 🧠 Automatic Reading Pace

The application automatically calculates reading time based on the text and provides additional pauses for:

* Punctuation
* Line breaks

---

### 🎬 Full HD & Vertical MP4 Export

Export your subtitles locally as:

* **1920 × 1080 (16:9)**
* **Vertical (9:16)**
* **30 FPS**
* **MP4**

The generated video uses a green-screen background suitable for chroma-key workflows.

No cloud processing, subscription, watermark, or online rendering service is required.

---

### 🔤 Windows Font Verification

Different writing systems require different fonts.

Before generating an MP4, the application checks whether the required Windows font is available.

If a required font cannot be found or loaded, the application stops the export and displays an informative message instead of silently generating a defective video.

This helps prevent:

* Missing characters
* Square boxes
* Incorrectly rendered text

---

## 🛠️ How It Works

### 1. Select a language

Choose your language from the alphabetically organized list of **76 supported languages**.

The application automatically selects the appropriate typography configuration.

### 2. Load a text file

Import a plain `.txt` file.

The application automatically processes the text and divides it into subtitle blocks.

### 3. Adjust the pace

Use the **±50% speed adjustment slider** if you need to match a particular voiceover or video duration.

### 4. Preview

Use the **Live Preview** to check the subtitle sequence and timing.

### 5. Export

Click **EXPORT TO MP4 FILE** to generate your Full HD or Vertical green-screen video locally.

---

## 💻 Requirements

* Windows
* Python 3.x if running the source code directly

Install the required libraries:

```bash
pip install opencv-python numpy Pillow
```

The compiled Windows version does **not** require Python to be installed.

---

## 🔤 Font Requirements

The application relies on fonts available in Windows for different writing systems.

If a required font is missing, the application will notify you before MP4 generation and indicate the required font.

The application does **not** redistribute third-party Windows fonts.

---

## 🌐 Supported Languages

Spanish, English, Italian, French, Portuguese, German, Polish, Ukrainian, Russian, Dutch, Chinese, Japanese, Korean, Arabic, Turkish, Persian, Indonesian, Bengali, Urdu, Filipino, Vietnamese, Hindi, Swahili, Romanian, Punjabi-Pakistan, Punjabi-India, Telugu, Malay, Tamil, Hausa, Thai, Greek, Yoruba, Pashto, Sundanese, Kurdish, Burmese, Amharic, Nepali, Zulu, Afrikaans, Hungarian, Serbian, Czech, Swedish, Hebrew, Bulgarian, Albanian, Belarusian, Armenian, Croatian, Danish, Mongolian, Finnish, Slovak, Norwegian, Lombard, Bosnian, Lithuanian, Pangasinan, Macedonian, Slovenian, Galician, Irish, Estonian, Latin, Catalan, Marathi, Sinhala, Gujarati, Quechua, Georgian, Azerbaijani, Lao, Kazakh, and Malayalam.

---

## 🧪 Multilingual Testing

The application has been tested with multiple writing systems, including:

* Latin
* Cyrillic
* CJK
* Arabic / Persian / Urdu
* Indic
* Thai
* Lao
* Hebrew

Additional language testing is ongoing to ensure consistent rendering across different Windows font configurations.

---

## 📄 Copyright & Credits

© 2026 **José Galindo**. All rights reserved.

Developed as a professional tool for subtitle automation and multilingual content creation.

**Developer:** José Galindo
**Website:** GABRIELS.WORK
