import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Force reload of environment variables
load_dotenv(override=True)

def get_gemini_client():
    """
    Get Gemini client with API key from environment variables.
    """
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        st.error("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")
        return None
    
    # Debug: Check if API key is loaded (only show first 8 characters for security)
    st.write(f"API Key loaded: {api_key[:8]}...")
    
    try:
        genai.configure(api_key=api_key)
        return genai
    except Exception as e:
        st.error(f"Error creating Gemini client: {str(e)}")
        return None

def get_available_model():
    """
    Get the recommended model for text generation.
    """
    try:
        client = get_gemini_client()
        if not client:
            return None
        
        # Try to use the recommended model first
        try:
            model = client.GenerativeModel('gemini-1.5-flash')
            return 'gemini-1.5-flash'
        except:
            # If that fails, list available models
            models = client.list_models()
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    return model.name
            return None
    except Exception as e:
        st.error(f"Error listing models: {str(e)}")
        return None

def test_api_connection():
    """
    Test the Gemini API connection.
    """
    try:
        client = get_gemini_client()
        if not client:
            return False
        
        # List available models first
        # models = client.list_models()
        # st.write("Available models:", [model.name for model in models])
        
        # Get the recommended model
        model_name = get_available_model()
        if not model_name:
            st.error("No suitable model found that supports generateContent")
            return False
            
        st.write(f"Using model: {model_name}")
        
        # Make a simple test call
        model = client.GenerativeModel(model_name)
        response = model.generate_content("Hello")
        return True
    except Exception as e:
        st.error(f"API connection test failed: {str(e)}")
        st.error("Please check if your API key is valid and has not expired.")
        return False

def get_chat_response(messages, max_tokens=1000, temperature=0.7):
    """
    Get a chat response from Gemini API.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        max_tokens: Maximum tokens in response
        temperature: Response creativity (0.0 to 1.0)
    
    Returns:
        Response content or None if error
    """
    try:
        client = get_gemini_client()
        if not client:
            return None
        
        model_name = get_available_model()
        if not model_name:
            st.error("No suitable model found that supports generateContent")
            return None
            
        model = client.GenerativeModel(model_name)
        chat = model.start_chat(history=[])
        
        # Convert messages to Gemini format
        for message in messages:
            if message['role'] == 'user':
                chat.send_message(message['content'])
            elif message['role'] == 'assistant':
                # Add assistant's previous response to history
                chat.history.append({
                    'role': 'model',
                    'parts': [message['content']]
                })
        
        response = chat.last.text
        return response
    
    except Exception as e:
        st.error(f"Error getting chat response: {str(e)}")
        return None

def get_code_assistance(code_query, code_context="", assistance_type="general"):
    """
    Get code assistance from Gemini API.
    
    Args:
        code_query: The code question or problem
        code_context: Optional code context
        assistance_type: Type of assistance (general, debug, review, explain)
    
    Returns:
        Response content or None if error
    """
    try:
        client = get_gemini_client()
        if not client:
            return None
        
        model_name = get_available_model()
        if not model_name:
            st.error("No suitable model found that supports generateContent")
            return None
        
        # Create system message based on assistance type
        system_messages = {
            "general": "You are an expert programming assistant. Help with coding questions, provide solutions, and explain concepts clearly.",
            "debug": "You are a debugging expert. Analyze the provided code and identify potential issues, bugs, or improvements.",
            "review": "You are a code reviewer. Analyze the code for best practices, performance, security, and maintainability.",
            "explain": "You are a programming tutor. Explain the provided code in detail, including how it works and why."
        }
        
        system_message = system_messages.get(assistance_type, system_messages["general"])
        
        model = client.GenerativeModel(model_name)
        prompt = f"{system_message}\n\nQuery: {code_query}\n\nCode Context: {code_context}" if code_context else f"{system_message}\n\nQuery: {code_query}"
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        st.error(f"Error getting code assistance: {str(e)}")
        return None

def generate_text(prompt, text_type="general", max_tokens=1000, temperature=0.7):
    """
    Generate text using Gemini API.
    
    Args:
        prompt: The text generation prompt
        text_type: Type of text generation (general, creative, formal, technical)
        max_tokens: Maximum tokens in response
        temperature: Response creativity (0.0 to 1.0)
    
    Returns:
        Generated text or None if error
    """
    try:
        client = get_gemini_client()
        if not client:
            return None
        
        model_name = get_available_model()
        if not model_name:
            st.error("No suitable model found that supports generateContent")
            return None
        
        # Create system message based on text type
        system_messages = {
            "general": "You are a helpful writing assistant. Generate clear, well-structured content based on the user's request.",
            "creative": "You are a creative writing assistant. Generate imaginative, engaging, and original content with vivid descriptions and compelling narratives.",
            "formal": "You are a professional writing assistant. Generate formal, polished content suitable for business or academic contexts.",
            "technical": "You are a technical writing specialist. Generate clear, precise, and informative technical content with proper terminology and structure."
        }
        
        system_message = system_messages.get(text_type, system_messages["general"])
        
        model = client.GenerativeModel(model_name)
        full_prompt = f"{system_message}\n\n{prompt}"
        
        response = model.generate_content(full_prompt)
        return response.text
    
    except Exception as e:
        st.error(f"Error generating text: {str(e)}")
        return None
