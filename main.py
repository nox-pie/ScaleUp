import streamlit as st
from SkillModel import get_model_response
from Visualizer import create_roadmap_image

# Configure Streamlit page
st.set_page_config(page_title="📚 ScaleUp", layout="centered")
st.title("📚 ScaleUp – Your Personalized Skill Roadmap Assistant")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🟩 Define roadmap trigger keywords
roadmap_keywords = ["Phase 1", "Week 1", "Stage"]

# 🔁 Display past chat messages and roadmap buttons (if any)
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        # ✅ Show roadmap download button for past assistant messages
        if message["role"] == "assistant" and any(kw in message["content"] for kw in roadmap_keywords):
            image_path = create_roadmap_image(message["content"])
            with open(image_path, "rb") as f:
                st.download_button(
                    label="📥 Download Roadmap as Image",
                    data=f,
                    file_name=f"roadmap_{i+1}.png",
                    mime="image/png",
                    key=f"roadmap_btn_{i}"
                )

# 💬 Handle new user input
if user_input := st.chat_input("💬 What skill would you like to learn?"):

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("⚙️ Building your personalized learning roadmap..."):
            api_key = st.secrets["api_key"]
            ai_response = get_model_response(messages=st.session_state.messages, api_key=api_key)

            st.markdown(ai_response)

            # ✅ Show download button immediately if it's a roadmap
            if any(kw in ai_response for kw in roadmap_keywords):
                image_path = create_roadmap_image(ai_response)
                with open(image_path, "rb") as f:
                    st.download_button(
                        label="📥 Download Roadmap as Image",
                        data=f,
                        file_name=f"roadmap_{len(st.session_state.messages)+1}.png",
                        mime="image/png",
                        key=f"immediate_roadmap_btn_{len(st.session_state.messages)}"
                    )

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
