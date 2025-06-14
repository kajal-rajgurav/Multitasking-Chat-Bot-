import streamlit as st
from utils.openai_client import generate_text

def render_text_generator():
    """
    Render the text generator interface.
    """
    st.header("✍️ Text Generator")
    st.markdown("Generate high-quality content for various purposes including creative writing, business documents, and technical content.")
    
    # Initialize text generator history
    if "text_generator_history" not in st.session_state:
        st.session_state.text_generator_history = []
    
    # Configuration section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        text_type = st.selectbox(
            "Content Type",
            ["general", "creative", "formal", "technical"],
            format_func=lambda x: {
                "general": "General Content",
                "creative": "Creative Writing",
                "formal": "Formal/Business",
                "technical": "Technical Writing"
            }[x],
            help="Select the type of content you want to generate"
        )
    
    with col2:
        if st.button("Clear History", type="secondary", key="clear_history_btn"):
            st.session_state.text_generator_history = []
            st.rerun()
    
    # Advanced settings in expander
    with st.expander("⚙️ Advanced Settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            temperature = st.slider(
                "Creativity Level",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Higher values make content more creative and varied"
            )
        
        with col2:
            max_tokens = st.slider(
                "Content Length",
                min_value=100,
                max_value=2000,
                value=800,
                step=100,
                help="Maximum length of generated content"
            )
    
    # Main input section
    st.subheader("Content Generation Prompt")
    
    # Provide example prompts based on content type
    example_prompts = {
        "general": "Write a comprehensive guide about...",
        "creative": "Write a short story about a time traveler who...",
        "formal": "Draft a professional email regarding...",
        "technical": "Explain the technical architecture of..."
    }
    
    prompt = st.text_area(
        "Describe what you want to generate:",
        height=150,
        placeholder=f"Example: {example_prompts[text_type]}",
        help="Be specific about the topic, tone, length, and any special requirements"
    )
    
    # Additional context section
    with st.expander("📝 Additional Context (Optional)"):
        context = st.text_area(
            "Provide any additional context, requirements, or constraints:",
            height=100,
            placeholder="E.g., Target audience, specific format requirements, key points to include..."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            target_audience = st.text_input(
                "Target Audience",
                placeholder="E.g., developers, students, executives"
            )
        with col2:
            tone = st.selectbox(
                "Tone",
                ["", "Professional", "Casual", "Friendly", "Authoritative", "Conversational", "Academic"],
                help="Specify the desired tone for the content"
            )
    
    # Generate button
    if st.button("Generate Content", type="primary", disabled=not prompt.strip(), key="generate_content_btn"):
        with st.spinner("Generating your content..."):
            # Enhance the prompt with additional context
            enhanced_prompt = prompt
            
            if context:
                enhanced_prompt += f"\n\nAdditional context: {context}"
            
            if target_audience:
                enhanced_prompt += f"\n\nTarget audience: {target_audience}"
            
            if tone:
                enhanced_prompt += f"\n\nTone: {tone}"
            
            # Add content type specific instructions
            type_instructions = {
                "creative": "Focus on vivid imagery, engaging narrative, and creative expression.",
                "formal": "Use professional language, clear structure, and appropriate business tone.",
                "technical": "Include technical accuracy, clear explanations, and proper terminology."
            }
            
            if text_type in type_instructions:
                enhanced_prompt += f"\n\nStyle note: {type_instructions[text_type]}"
            
            response = generate_text(
                prompt=enhanced_prompt,
                text_type=text_type,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            if response:
                # Add to history
                st.session_state.text_generator_history.append({
                    "prompt": prompt,
                    "context": context,
                    "type": text_type,
                    "audience": target_audience,
                    "tone": tone,
                    "response": response,
                    "settings": {
                        "temperature": temperature,
                        "max_tokens": max_tokens
                    }
                })
                
                # Display response
                st.success("Content generated successfully!")
                
                # Show the generated content
                st.subheader("📄 Generated Content")
                
                # Add copy button functionality
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown("**Your generated content:**")
                with col2:
                    if st.button("📋 Copy", help="Copy content to clipboard", key="copy_content_btn"):
                        st.code(response, language=None)
                
                # Display content in a nice format
                content_container = st.container()
                with content_container:
                    st.markdown(response)
                
                # Show content statistics
                word_count = len(response.split())
                char_count = len(response)
                estimated_reading_time = max(1, word_count // 200)  # Assuming 200 words per minute
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Words", word_count)
                with col2:
                    st.metric("Characters", char_count)
                with col3:
                    st.metric("Est. Reading Time", f"{estimated_reading_time} min")
                
            else:
                st.error("Failed to generate content. Please try again.")
    
    # Display generation history
    if st.session_state.text_generator_history:
        st.markdown("---")
        st.subheader("📚 Recent Generations")
        
        # Show recent generations (last 3)
        for i, generation in enumerate(reversed(st.session_state.text_generator_history[-3:])):
            with st.expander(f"Generation {len(st.session_state.text_generator_history) - i}: {generation['prompt'][:50]}..."):
                
                # Show generation details
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Type:** {generation['type'].title()}")
                with col2:
                    if generation['tone']:
                        st.markdown(f"**Tone:** {generation['tone']}")
                with col3:
                    if generation['audience']:
                        st.markdown(f"**Audience:** {generation['audience']}")
                
                # Show the generated content
                st.markdown("**Generated Content:**")
                st.markdown(generation['response'])
                
                # Show settings used
                st.markdown("**Settings Used:**")
                st.json(generation['settings'])
    
    # Usage tips and examples
    with st.sidebar:
        st.markdown("### 💡 Content Generation Tips")
        
        st.markdown("**For Better Results:**")
        st.markdown("""
        - Be specific about your requirements
        - Include context and target audience
        - Specify the desired length and format
        - Mention any constraints or requirements
        """)
        
        st.markdown("### 📝 Example Prompts")
        
        example_sections = {
            "Creative Writing": [
                "Write a short story about...",
                "Create a poem describing...",
                "Draft a creative product description for..."
            ],
            "Business Content": [
                "Write a professional proposal for...",
                "Create a press release announcing...",
                "Draft an executive summary about..."
            ],
            "Technical Writing": [
                "Explain how to implement...",
                "Write documentation for...",
                "Create a technical tutorial on..."
            ]
        }
        
        for section, examples in example_sections.items():
            with st.expander(section):
                for example in examples:
                    st.markdown(f"• {example}")
        
        st.markdown("### 📊 Session Stats")
        st.markdown(f"Content pieces generated: {len(st.session_state.text_generator_history)}")
