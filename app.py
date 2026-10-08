import os
import io
import requests
import streamlit as st
from PIL import Image

# Page Setup
st.set_page_config(
    page_title="Mahashank AI Studio",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Mahashank Design & Technology AI Generator")
st.caption("Permanent, Free 24/7 Generative AI Studio")

# Fetch Token securely
HF_TOKEN = st.secrets.get("HF_TOKEN", os.getenv("HF_TOKEN", ""))

# Hugging Face Free Inference API Endpoint
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

col1, col2 = st.columns([1, 1])

with col1:
    prompt = st.text_area(
        "Design Prompt", 
        placeholder="e.g., A minimalist smart home device mockup, sleek matte black finish..."
    )
    generate_btn = st.button("Generate HD Image", type="primary")

with col2:
    if generate_btn and prompt:
        if not HF_TOKEN:
            st.error("⚠️ HF_TOKEN is missing. Please add your free token in Streamlit Secrets.")
        else:
            with st.spinner("⚡ Generating design via Hugging Face Free API (takes ~10–15s)..."):
                try:
                    enhanced_prompt = f"{prompt}, high definition, 8k resolution, crisp commercial texture, professional studio lighting, Mahashank design aesthetic"
                    
                    response = requests.post(
                        API_URL,
                        headers=headers,
                        json={"inputs": enhanced_prompt},
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        image_bytes = response.content
                        image = Image.open(io.BytesIO(image_bytes))
                        
                        st.image(image, caption="Generated Output", use_container_width=True)
                        
                        # Direct Download Button
                        st.download_button(
                            label="⬇️ Download Full-Res Image",
                            data=image_bytes,
                            file_name="mahashank_design.png",
                            mime="image/png"
                        )
                        st.success("Generation Complete!")
                    else:
                        st.error(f"Generation Error ({response.status_code}): {response.text}")
                        
                except Exception as e:
                    st.error(f"Generation failed: {str(e)}")
