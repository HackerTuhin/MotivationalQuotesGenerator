import streamlit as st
from autogen import ConversableAgent
import requests
from io import BytesIO
from PIL import Image
import base64
# need to chnage model in config ("model": "openrouter/optimus-alpha",)
# Define the OpenAI agent configuration
from config import config
# Define the agent
image_processor_agent = ConversableAgent(
    name="image_processor_agent",
    llm_config=config,
    code_execution_config=False,
    human_input_mode="NEVER",
    system_message="Your task is to understand the image and respond with a detailed description of the objects and emotions present in the image.",
)

# Streamlit UI
st.title("🖼️ Emotional Image Analyzer ")
st.write("Upload an image or enter an image URL to get an emotional description.")

# File uploader or URL input
upload_option = st.radio("Select Input Method", ["Upload Image", "Image URL"])

image = None
image_url = None

if upload_option == "Upload Image":
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)

        # Convert uploaded image to base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        image_url = f"data:image/png;base64,{img_str}"

elif upload_option == "Image URL":
    image_url = st.text_input("Enter image URL")
    if image_url:
        try:
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            st.image(image, caption="Image from URL", use_container_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")
            image_url = None

# Submit button
if image_url and st.button("🔍 Analyze Image"):
    with st.spinner("Analyzing image with emotions..."):
        # Prepare messages
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe the image with deep emotions"},
                    {"type": "image_url", "image_url": {"url": image_url}},
                ],
            }
        ]
        response = image_processor_agent.generate_reply(messages=messages)
        st.subheader("🧠 Emotional Description")
        st.write(response)
