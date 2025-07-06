# NOTE: This app must be run in a local Python environment with Streamlit and OpenAI installed.
# Install requirements using: pip install streamlit openai
# Or create a requirements.txt file with the dependencies

import streamlit as st
import sys

# Check if openai is available
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Streamlit page setup
st.set_page_config(page_title="Prompt Enhancer", layout="centered")
st.title("🛠️ AI Prompt Enhancer")

# Check for missing dependencies
if not OPENAI_AVAILABLE:
    st.error("**Missing Dependencies!**")
    st.markdown("""
    The OpenAI library is not installed. To fix this:
    
    **For local development:**
    ```bash
    pip install streamlit openai
    ```
    
    **For Streamlit Cloud deployment:**
    Create a `requirements.txt` file with:
    ```
    streamlit>=1.28.0
    openai>=1.0.0
    ```
    """)
    st.stop()

st.markdown("""
Enter the details below to generate an improved and more effective AI prompt.
""")

# API Key input with better UX
api_key = st.text_input(
    "🔑 Enter your OpenAI API Key", 
    type="password",
    help="Your API key will not be stored. Get one from https://platform.openai.com/api-keys"
)

# Input fields with better organization
col1, col2 = st.columns(2)

with col1:
    context = st.text_area(
        "Context", 
        placeholder="What's the background or situation for your prompt?",
        help="Provide relevant background information"
    )
    
    task = st.text_area(
        "Task", 
        placeholder="What do you want the AI to do?",
        help="Be specific about what you want to achieve"
    )

with col2:
    format_type = st.text_input(
        "Preferred Format", 
        placeholder="e.g., list, essay, code, email",
        help="How should the output be structured?"
    )
    
    tone = st.text_input(
        "Tone", 
        placeholder="e.g., formal, friendly, persuasive",
        help="What tone should the AI use?"
    )

# Additional options
with st.expander("Advanced Options"):
    example = st.text_area(
        "Example (Optional)", 
        placeholder="Provide an example of a good output",
        help="This helps the AI understand your expectations"
    )
    
    word_limit = st.number_input(
        "Word Limit (Optional)", 
        min_value=50, 
        max_value=2000, 
        step=50, 
        value=300,
        help="Approximate length of the desired response"
    )

if st.button("✨ Generate Enhanced Prompt", type="primary"):
    if not task.strip():
        st.warning("Please enter at least a task to generate a prompt.")
    elif not api_key.strip():
        st.error("Please enter your OpenAI API key.")
    else:
        # Construct input message
        system_message = {
            "role": "system", 
            "content": "You are an expert prompt engineer who creates clear, effective, and well-structured prompts for AI systems."
        }
        
        user_message = {
            "role": "user", 
            "content": f"""
Create an enhanced and more effective prompt based on these specifications:

Context: {context if context.strip() else "Not specified"}
Task: {task}
Preferred Format: {format_type if format_type.strip() else "Not specified"}
Tone: {tone if tone.strip() else "Not specified"}
Example Output: {example if example.strip() else "Not provided"}

Requirements:
- Make the prompt clear, specific, and actionable
- Include proper instructions for the AI
- Specify that the response should be approximately {word_limit} words
- Add a note encouraging the user to ask clarifying questions if needed
- Structure the prompt logically with clear sections

Generate a professional, well-formatted prompt that will produce better results.
"""
        }

        with st.spinner("Generating enhanced prompt..."):
            try:
                client = openai.OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[system_message, user_message],
                    temperature=0.7,
                    max_tokens=500
                )
                enhanced_prompt = response.choices[0].message.content
                
                st.success("✅ Here is your enhanced prompt:")
                st.text_area(
                    "Enhanced Prompt", 
                    enhanced_prompt, 
                    height=250,
                    help="Copy this prompt and use it with any AI system"
                )
                
                # Option to copy to clipboard
                st.markdown("📋 **Tip:** Select all text above and copy it to use with your AI system!")
                
            except openai.AuthenticationError:
                st.error("❌ Invalid API key. Please check your OpenAI API key.")
            except openai.RateLimitError:
                st.error("❌ Rate limit exceeded. Please try again later.")
            except openai.APIError as e:
                st.error(f"❌ OpenAI API error: {str(e)}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    🚀 Built with Streamlit and OpenAI API<br>
    💡 <strong>Tip:</strong> Keep your API key secure and never share it publicly
</div>
""", unsafe_allow_html=True)