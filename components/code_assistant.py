import streamlit as st
from utils.openai_client import get_code_assistance

def render_code_assistant():
    """
    Render the code assistant interface.
    """
    st.header("👨‍💻 Code Assistant")
    st.markdown("Get help with programming questions, code review, debugging, and explanations.")
    
    # Initialize code assistant history
    if "code_assistant_history" not in st.session_state:
        st.session_state.code_assistant_history = []
    
    # Assistant configuration
    col1, col2 = st.columns([2, 1])
    
    with col1:
        assistance_type = st.selectbox(
            "Type of Assistance",
            ["general", "debug", "review", "explain"],
            format_func=lambda x: {
                "general": "General Help",
                "debug": "Debug Code",
                "review": "Code Review",
                "explain": "Explain Code"
            }[x],
            help="Select the type of code assistance you need"
        )
    
    with col2:
        if st.button("Clear History", type="secondary"):
            st.session_state.code_assistant_history = []
            st.rerun()
    
    # Input sections
    st.subheader("Your Code Question or Problem")
    code_query = st.text_area(
        "Describe your coding question, problem, or what you need help with:",
        height=100,
        placeholder="E.g., How do I sort a list of dictionaries by a specific key in Python?"
    )
    
    st.subheader("Code Context (Optional)")
    code_context = st.text_area(
        "Paste your code here if relevant:",
        height=200,
        placeholder="# Paste your code here\ndef my_function():\n    pass",
        help="Include any relevant code that needs review, debugging, or explanation"
    )
    
    # Programming language selection
    col1, col2 = st.columns(2)
    with col1:
        language = st.selectbox(
            "Programming Language (Optional)",
            ["", "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust", "PHP", "Ruby", "Swift", "Kotlin", "Other"],
            help="Specify the programming language for more targeted assistance"
        )
    
    # Submit button
    if st.button("Get Code Assistance", type="primary", disabled=not code_query.strip()):
        with st.spinner("Analyzing your code question..."):
            # Prepare the enhanced query
            enhanced_query = code_query
            if language:
                enhanced_query = f"[{language}] {enhanced_query}"
            
            response = get_code_assistance(
                code_query=enhanced_query,
                code_context=code_context,
                assistance_type=assistance_type
            )
            
            if response:
                # Add to history
                st.session_state.code_assistant_history.append({
                    "query": code_query,
                    "context": code_context,
                    "language": language,
                    "type": assistance_type,
                    "response": response
                })
                
                # Display response
                st.success("Code assistance generated successfully!")
                
                # Display the current response
                st.subheader("🤖 Assistant Response")
                st.markdown(response)
            else:
                st.error("Failed to get code assistance. Please try again.")
    
    # Display history
    if st.session_state.code_assistant_history:
        st.markdown("---")
        st.subheader("📚 Recent Assistance")
        
        # Show recent interactions (last 5)
        for i, interaction in enumerate(reversed(st.session_state.code_assistant_history[-5:])):
            with st.expander(f"Question {len(st.session_state.code_assistant_history) - i}: {interaction['query'][:50]}..."):
                
                # Show interaction details
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Type:** {interaction['type'].title()}")
                with col2:
                    if interaction['language']:
                        st.markdown(f"**Language:** {interaction['language']}")
                with col3:
                    st.markdown(f"**Assistance #{len(st.session_state.code_assistant_history) - i}**")
                
                # Show original query
                st.markdown("**Your Question:**")
                st.markdown(interaction['query'])
                
                # Show code context if provided
                if interaction['context'].strip():
                    st.markdown("**Code Context:**")
                    st.code(interaction['context'], language=interaction['language'].lower() if interaction['language'] else None)
                
                # Show response
                st.markdown("**Assistant Response:**")
                st.markdown(interaction['response'])
    
    # Tips and examples
    with st.sidebar:
        st.markdown("### 💡 Tips for Better Assistance")
        st.markdown("""
        **For General Help:**
        - Be specific about what you want to achieve
        - Mention the programming language
        - Include relevant context
        
        **For Debugging:**
        - Include the problematic code
        - Describe the expected vs actual behavior
        - Mention any error messages
        
        **For Code Review:**
        - Provide the complete function/class
        - Mention specific concerns (performance, security, etc.)
        
        **For Explanations:**
        - Include the code you want explained
        - Specify your experience level
        """)
        
        st.markdown("### 📊 Session Stats")
        st.markdown(f"Questions asked: {len(st.session_state.code_assistant_history)}")
