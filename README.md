# ScaleUp — Personalized Skill Roadmap Assistant

> 🚀 An AI-powered chatbot that generates personalized learning roadmaps for technical and non-technical skills using Google Gemini API and Streamlit.

![ScaleUp Logo](./ScaleUp_logo.png)

---

## 🔍 Overview

**ScaleUp** is your career co-pilot — a web-based AI assistant that helps users craft tailored roadmaps to upskill in any domain. Powered by Google’s Gemini model and a beautifully themed Streamlit UI, ScaleUp suggests:

* 📘 Courses & certifications
* 🧰 Tools & technologies
* 👥 Communities & platforms
* 🏗️ Project ideas
* 📄 Downloadable PDF roadmap

---

## 🛠️ Features

* ✅ Clean and elegant chat interface
* ✅ Gemini-powered skill roadmap generation
* ✅ Smart formatting of multi-phase learning plans
* ✅ Auto-generated, downloadable PDF roadmaps
* ✅ Themed UI with custom visuals
* ✅ Auto-cleans previous roadmaps on page refresh

---

## 📸 Preview

> ![Screenshot](https://github.com/user-attachments/assets/682eab6e-5795-400e-98b2-18e5e4c7fbff)

---

## 💻 Tech Stack

| Tool                  | Purpose                        |
| --------------------- | ------------------------------ |
| **Streamlit**         | Frontend & interactive chat UI |
| **Google Gemini API** | AI text generation             |
| **WeasyPrint**        | Generate styled PDF roadmap    |
| **Pillow**            | Logo image processing          |
| **streamlit-lottie**  | Lottie animation support       |

---

## 📂 Project Structure

```
ScaleUp/
├── .streamlit/              # Config + secrets
│   ├── config.toml
│   └── secrets.toml
├── generated_roadmaps/      # Temp PDF storage (auto-deleted)
├── main.py                  # Main Streamlit app
├── PromptBuilder.py         # Prompt builder for Gemini
├── Roadmap.py               # Markdown to styled PDF generator
├── SkillModel.py            # Gemini API logic
├── requirements.txt         # Dependencies
├── .gitignore               # Ignored files/folders
└── ScaleUp_logo.png         # Branding logo
```

---

## 🚀 Getting Started (Locally)

### 1. Clone the repo

```bash
git clone https://github.com/your-username/ScaleUp.git
cd ScaleUp
```

### 2. Create & activate virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up Gemini API Key

Create a `.streamlit/secrets.toml` file:

```toml
# .streamlit/secrets.toml
api_key = "your_google_gemini_api_key"
```

> 🔐 Your API key will stay private and won't be pushed to GitHub due to `.gitignore`.

### 5. Run the app

```bash
streamlit run main.py
```

---

## 🌐 Deployment

You can easily deploy this app to **Streamlit Cloud**:

1. Push your code to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo and deploy!

Make sure to add your Gemini API key in the **Secrets** section of Streamlit Cloud under `api_key`.

---

## 📦 Requirements

All required packages are listed in `requirements.txt`.
To regenerate the list after dependency updates:

```bash
pip freeze > requirements.txt
```

---

## 📄 License

This project is licensed under the **Apache License 2.0**.
See the [LICENSE](./LICENSE) file for more details.

---

## 🙌 Credits

Developed with ❤️ by **[Prashant Kumar](https://www.linkedin.com/in/prashant-k23/)**
GitHub: [nox-pie](https://github.com/nox-pie)

---
