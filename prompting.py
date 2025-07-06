# NOTE: This app must be run in a local Python environment with Streamlit and OpenAI installed.
# Install requirements using: pip install streamlit openai

import streamlit as st
import openai

# Streamlit page setup
st.set_page_config(page_title="Prompt Enhancer", layout="centered")
st.title("🛠️ AI Prompt Enhancer")

st.markdown("""
Enter the details below to generate an improved and more effective AI prompt.
""")

# API Key input
api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

# Input fields
context = st.text_area("Context", placeholder="What's the background or situation for your prompt?")
task = st.text_area("Task", placeholder="What do you want the AI to do?")
format = st.text_input("Preferred Format", placeholder="e.g., list, essay, code, email")
tone = st.text_input("Tone", placeholder="e.g., formal, friendly, persuasive")
example = st.text_area("Example (Optional)", placeholder="Provide an example of a good output")
word_limit = st.number_input("Word Limit (Optional)", min_value=50, max_value=1000, step=50, value=300)

if st.button("✨ Generate Enhanced Prompt"):
    if not task:
        st.warning("Please enter at least a task to generate a prompt.")
    elif not api_key:
        st.error("API key not found. Please enter your OpenAI API key above.")
    else:
        # Construct input message
        system_message = {"role": "system", "content": "You are an expert prompt engineer."}
        user_message = {"role": "user", "content": f"""
Improve and enhance the following prompt based on user inputs:

Context: {context}
Task: {task}
Preferred Format: {format}
Tone: {tone}
Example Output: {example}

Generate a more usable and detailed prompt. The output must explicitly state that the response should be approximately {word_limit} words long. Add a note at the end suggesting the user to ask clarifying questions if needed.
"""}

        with st.spinner("Thinking..."):
            try:
                client = openai.OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[system_message, user_message],
                    temperature=0.7,
                    max_tokens=400
                )
                enhanced_prompt = response.choices[0].message.content
                st.success("Here is your enhanced prompt:")
                st.text_area("Enhanced Prompt", enhanced_prompt, height=200)
            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("🚀 Built by a beginner coder exploring the power of AI with Streamlit and OpenAI ✨")
