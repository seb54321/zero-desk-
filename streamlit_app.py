import streamlit as st
import openai
import base64
from PIL import Image
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Use secrets if deploying

st.set_page_config(page_title="ZeroDesk – Receipt Analyzer")
st.title("🧾 ZeroDesk Receipt Analyzer")
st.write("Upload a receipt and let GPT-4 extract the key financial details.")

# Upload receipt
uploaded_file = st.file_uploader("Upload a receipt image (JPG or PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 Uploaded Receipt", use_column_width=True)
    
    # Convert image to base64
    image_bytes = uploaded_file.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    # Use GPT-4 Vision
    with st.spinner("🔍 Analyzing with GPT-4 Vision..."):
        client = openai.OpenAI()

        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that extracts and summarizes receipt data: store name, date, total amount, and category."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Please extract the receipt details from this image."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )

        result = response.choices[0].message.content
        st.subheader("📄 Extracted Info:")
        st.write(result)

