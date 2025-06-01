import streamlit as st
from components.chatbot import render_chatbot
from components.code_assistant import render_code_assistant
from components.text_generator import render_text_generator

# Configure page
st.set_page_config(
    page_title="AI Assistant Hub",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if "api_key_valid" not in st.session_state:
    st.session_state.api_key_valid = False

def main():
    st.title("🤖 AI Assistant Hub")
    st.markdown("Your comprehensive AI-powered assistant for conversations, coding, and content creation.")
    
    # API Key validation
    if not st.session_state.api_key_valid:
        st.warning("⚠️ Please ensure your OpenAI API key is configured in the environment variables.")
        if st.button("Test API Connection"):
            from utils.openai_client import test_api_connection
            if test_api_connection():
                st.session_state.api_key_valid = True
                st.success("✅ API connection successful!")
                st.rerun()
            else:
                st.error("❌ API connection failed. Please check your API key.")
        return
    
    # Create tabs for different functionalities
    tab1, tab2, tab3 = st.tabs(["💬 Chatbot", "👨‍💻 Code Assistant", "✍️ Text Generator"])
    
    with tab1:
        render_chatbot()
    
    with tab2:
        render_code_assistant()
    
    with tab3:
        render_text_generator()

if __name__ == "__main__":
    main()
