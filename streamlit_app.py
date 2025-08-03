import streamlit as st
import openai
import os
from PIL import Image

st.set_page_config(page_title="ZeroDesk - Receipt Analyzer")

st.title("🧾 ZeroDesk Receipt Analyzer")
st.write("Upload a receipt and let GPT-4 extract the key financial details.")

# Upload image
uploaded_file = st.file_uploader("Upload a receipt image (JPG or PNG)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_column_width=True)

    image_bytes = uploaded_file.read()

    with st.spinner("Analyzing with GPT-4 Vision..."):
        response = openai.ChatCompletion.create(
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
                        {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + image_bytes.decode("latin1")}}
                    ]
                }
            ],
            max_tokens=500
        )

        result = response["choices"][0]["message"]["content"]
        st.subheader("📄 Extracted Info:")
        st.write(result)
