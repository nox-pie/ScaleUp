import streamlit as st
from SkillModel import get_model_response
from Roadmap import generate_roadmap_pdf  
from streamlit_lottie import st_lottie
from PIL import Image
import requests
import os

# ---------------- PDF CLEANUP ON REFRESH ----------------
def clear_generated_pdfs(folder="generated_roadmaps"):
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            if filename.endswith(".pdf"):
                try:
                    os.remove(os.path.join(folder, filename))
                except Exception:
                    pass

clear_generated_pdfs()  # Auto-run when app starts or refreshes
# --------------------------------------------------------

# ---------------- PAGE CONFIG & HEADER ----------------
st.set_page_config(page_title="📚 ScaleUp", layout="centered")

logo = Image.open("ScaleUp_logo.png").resize((100, 120), Image.LANCZOS)
cols = st.columns([1, 8])
with cols[0]:
    st.image(logo)
with cols[1]:
    st.markdown("<h1 style='color: #FDF6E3; font-family: serif; padding-top: 35px;'>ScaleUp</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: left; color: white;'>Your Personalized Skill Roadmap Assistant</h2>", unsafe_allow_html=True)
# ------------------------------------------------------

# ---------------- SIDEBAR INFO ----------------
with st.sidebar:
    st.markdown("""
        <h2>🚀 <span style="
        background: linear-gradient(to left, lightblue, green, yellow, orange, red);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
        ">
        About ScaleUp
        </span></h2>
        """, unsafe_allow_html=True)

    st.markdown(
        "It is an **AI-powered** career guidance chatbot.\n\n"
        "It helps users get **personalized roadmaps** for learning technical and non-technical skills, including courses, tools, certifications, communities, and more."
    )
    st.markdown("— Made with ❤️ using Streamlit + Gemini API")
    st.markdown("---")
    st.markdown("📁 GitHub: https://github.com/nox-pie")  
    st.markdown("💼 LinkedIn: https://www.linkedin.com/in/prashant-k23/")
    st.markdown("📧 Gmail: prashant.k23singh@gmail.com")
# ------------------------------------------------------

# ---------------- LOTTIE ANIMATION ----------------
# Load Lottie animation
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Lottie animation URL
robot_animation = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_0yfsb3a1.json")

# Display the animation just below the title
if robot_animation:
    st_lottie(robot_animation, height=250, key="hello_bot")
else:
    st.info("👋 Welcome to ScaleUp!")
# --------------------------------------------------

# ---------------- SESSION SETUP ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
# -----------------------------------------------

# ---------------- DETECT ROADMAP ----------------
roadmap_keywords = ["Phase 1", "Week 1", "Stage"]
roadmap_trigger_phrase = "Here's a potential learning roadmap for you:"

def is_roadmap_response(content: str) -> bool:
    return any(kw in content for kw in roadmap_keywords) or roadmap_trigger_phrase in content
# -------------------------------------------------

# ---------------- ASSISTANT STYLING ----------------
st.markdown("""
<style>
.assistant-bubble {
    background-color: #e7bc91;  
    color: #1a1a1a;
    padding: 12px 16px;
    border-radius: 12px;
    margin: 8px 0;
    font-size: 15px;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)
# ---------------------------------------------------

# ---------------- RENDER CHAT HISTORY ----------------
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(f'<div class="assistant-bubble">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

        if message["role"] == "assistant" and is_roadmap_response(message["content"]):
            st.markdown("### 📄 Your roadmap is ready!")
            pdf_path = generate_roadmap_pdf(message["content"])
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📥 Download Roadmap as PDF",
                    data=f,
                    file_name=f"roadmap_{i+1}.pdf",
                    mime="application/pdf",
                    key=f"roadmap_download_{i}"
                )
# ------------------------------------------------------

# ---------------- CHAT INPUT SECTION ----------------
if user_input := st.chat_input("💬 What skill would you like to learn?"):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("⚙️ Building your personalized learning roadmap..."):
            api_key = st.secrets["api_key"]
            ai_response = get_model_response(messages=st.session_state.messages, api_key=api_key)

            st.markdown(f'<div class="assistant-bubble">{ai_response}</div>', unsafe_allow_html=True)

            if is_roadmap_response(ai_response):
                st.markdown("### 📄 Your roadmap is ready!")
                pdf_path = generate_roadmap_pdf(ai_response)
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Roadmap as PDF",
                        data=f,
                        file_name=f"roadmap_{len(st.session_state.messages)+1}.pdf",
                        mime="application/pdf",
                        key=f"instant_download_btn_{len(st.session_state.messages)}"
                    )

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
# ------------------------------------------------------

# ---------------- FOOTER ----------------
st.markdown("""
<hr style="
  border: none;
  height: 2.5px;
  background: linear-gradient(to left, violet, blue, green, yellow, orange, red);
  border-radius: 10px;
  margin-top: 10px;
  margin-bottom: 20px;
">
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; font-family: monospace; font-size: small;'>
    🔖 ScaleUp v1.0 — Built with ❤️ by Prashant Kumar
</div>
""", unsafe_allow_html=True)
# ----------------------------------------
