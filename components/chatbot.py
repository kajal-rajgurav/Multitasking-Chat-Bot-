import streamlit as st
from utils.openai_client import get_chat_response

def render_chatbot():
    """
    Render the chatbot interface.
    """
    st.header("💬 AI Chatbot")
    st.markdown("Have a natural conversation with the AI assistant. Ask questions, get advice, or just chat!")
    
    # Initialize chat history
    if "chatbot_messages" not in st.session_state:
        st.session_state.chatbot_messages = []
    
    # Chat configuration sidebar
    with st.sidebar:
        st.subheader("Chat Settings")
        temperature = st.slider(
            "Creativity Level",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values make responses more creative, lower values more focused"
        )
        max_tokens = st.slider(
            "Max Response Length",
            min_value=100,
            max_value=2000,
            value=1000,
            step=100,
            help="Maximum number of tokens in the response"
        )
        
        if st.button("Clear Chat History", type="secondary"):
            st.session_state.chatbot_messages = []
            st.rerun()
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chatbot_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if user_input := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.chatbot_messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Prepare messages for API call
                api_messages = []
                
                # Add system message for context
                api_messages.append({
                    "role": "system", 
                    "content": "You are a helpful, friendly, and knowledgeable AI assistant. Provide clear, accurate, and engaging responses to user questions and requests."
                })
                
                # Add conversation history (last 10 messages to manage context length)
                recent_messages = st.session_state.chatbot_messages[-10:] if len(st.session_state.chatbot_messages) > 10 else st.session_state.chatbot_messages
                for msg in recent_messages:
                    api_messages.append(msg)
                
                # Get response from OpenAI
                response = get_chat_response(
                    messages=api_messages,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                
                if response:
                    st.markdown(response)
                    # Add assistant response to chat history
                    st.session_state.chatbot_messages.append({"role": "assistant", "content": response})
                else:
                    st.error("Sorry, I couldn't generate a response. Please try again.")
    
    # Show conversation stats
    if st.session_state.chatbot_messages:
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**Conversation Stats:**")
        st.sidebar.markdown(f"Messages: {len(st.session_state.chatbot_messages)}")
        
        # Calculate token estimate (rough approximation)
        total_chars = sum(len(msg["content"]) for msg in st.session_state.chatbot_messages)
        estimated_tokens = total_chars // 4  # Rough estimate: 1 token ≈ 4 characters
        st.sidebar.markdown(f"Estimated tokens: {estimated_tokens}")
