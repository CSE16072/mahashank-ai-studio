import os
import io
import time
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

# Fetch Token securely from Streamlit Secrets
HF_TOKEN = st.secrets.get("HF_TOKEN", os.getenv("HF_TOKEN", ""))

# Primary and Fallback Endpoints for Free Serverless Inference
ENDPOINTS = [
    "https://router.huggingface.co/models/stabilityai/stable-diffusion-3.5-large",
    "https://router.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
]

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def query_huggingface(payload, retries=3, delay=6):
    """Queries HF API using router endpoints with warm-up retry handling."""
    for api_url in ENDPOINTS:
        for attempt in range(retries):
            try:
                response = requests.post(api_url, headers=headers, json=payload, timeout=90)
                
                # Success
                if response.status_code == 200:
                    return response.content, None
                
                # Cold start (Model loading)
                if response.status_code == 503:
                    st.warning(f"⏳ Model warming up... Retrying attempt {attempt + 1}/{retries}...")
                    time.sleep(delay)
                    continue
                    
            except requests.exceptions.RequestException:
                break # Move to fallback endpoint if DNS/Connection fails
                
    return None, "Server response delayed. Please click 'Generate HD Image' again in a few seconds."

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
            with st.spinner("⚡ Generating high-definition design..."):
                try:
                    enhanced_prompt = f"{prompt}, high definition, 8k resolution, crisp commercial texture, professional studio lighting, Mahashank design aesthetic"
                    
                    image_bytes, err = query_huggingface({"inputs": enhanced_prompt})
                    
                    if err:
                        st.error(err)
                    else:
                        image = Image.open(io.BytesIO(image_bytes))
                        
                        st.image(image, caption="Generated Output", use_container_width=True)
                        
                        st.download_button(
                            label="⬇️ Download Full-Res Image",
                            data=image_bytes,
                            file_name="mahashank_design.png",
                            mime="image/png"
                        )
                        st.success("Generation Complete!")
                        
                except Exception as e:
                    st.error(f"Generation failed: {str(e)}")
