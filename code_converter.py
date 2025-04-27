import streamlit as st
from autogen import ConversableAgent
import shutil
import os
import re
from config import config

def delete_cache_folder():
    cache_path = ".cache"
    try:
        if os.path.exists(cache_path):
            shutil.rmtree(cache_path)
    except Exception as e:
        st.error(f"Error deleting cache folder: {e}")

# OpenAI Agent Config


# Initialize AI Agent
try:
    code_converter_agent = ConversableAgent(
        name="code_converter_agent",
        llm_config=config,
        code_execution_config=False,
        human_input_mode="NEVER",
        system_message="You are a code converter. Your task is to convert the given code from the source language to the target language as accurately as possible. Do not explain, just provide the translated code.",
    )
except Exception as e:
    st.error(f"Error initializing AI agent: {e}")

# Function to call the agent for code conversion
def convert_code(source_code, source_language, target_language):
    try:
        prompt = (
            f"Convert the following code from {source_language} to {target_language}.\n\n"
            f"Source Code:\n```{source_language}\n{source_code}\n```"
        )
        message = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]
        response = code_converter_agent.generate_reply(messages=message)
        if not response:
            raise ValueError("Empty response from code converter agent.")
        return response
    except Exception as e:
        st.error(f"Error during code conversion: {e}")
        return None

def extract_code_from_response(response):
    """Extract code content from a markdown code block."""
    code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", response, re.DOTALL)
    if code_blocks:
        return code_blocks[0].strip()
    return response.strip()

# Virtual compiler to test syntax
def virtual_compile(code, language):
    try:
        if language.lower() == "python":
            compile(code, "<string>", "exec")
            return "✅ Python code compiled successfully. No syntax errors."
        
        else:
            return "⚠️ Virtual compilation is only available for Python ."
    except Exception as e:
        return f"❌ Compilation error: {str(e)}"

# Streamlit UI
def main():
    st.title("🔄 Code Converter + Virtual Compiler (Only for Python)")

    try:
        st.subheader("Enter your source code:")
        source_code = st.text_area("Source Code", height=200)

        st.subheader("Select Source and Target Languages:")
        col1, col2 = st.columns(2)
        with col1:
            source_language = st.selectbox("Source Language", ["Python","C"])
        with col2:
            target_language = st.selectbox("Target Language", ["Python", "C", "C++", "C#", "Java", "JavaScript", "PHP", "Ruby", "Go","Dart", "Assembly langauge", "Shell (Bash)"," Rust", "Swift", "Kotlin","Node"])

        converted_code = None

        if st.button("Convert Code"):
            if not source_code.strip():
                st.error("⚠️ Please enter some source code to convert.")
                return
            if source_language == target_language:
                st.warning("⚠️ Source and target languages are the same. Please choose different languages.")
                return
            
            with st.spinner("Converting code..."):
                converted_code = convert_code(source_code, source_language, target_language)
                if not converted_code:
                    return

            st.subheader("🔧 Converted Code:")
            st.code(converted_code, language=target_language.lower())

            # Store converted code in session state for testing
            st.session_state['converted_code'] = extract_code_from_response(converted_code)
            st.session_state['converted_code']=st.session_state['converted_code'].replace('`','"')
            st.session_state['target_language'] = target_language

        # Test Compilation Section
        if 'converted_code' in st.session_state and st.button("Test Compilation"):
            with st.spinner("Testing compilation..."):
                result = virtual_compile(st.session_state['converted_code'], st.session_state['target_language'])
                st.info(result)

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
    delete_cache_folder()
