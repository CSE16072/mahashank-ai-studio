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

# Modern Serverless Router Endpoint
API_URL = "https://router.huggingface.co/models/stabilityai/stable-diffusion-3.5-large"
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def query_huggingface(payload, retries=5, delay=10):
    """Queries HF API with automatic retry for 503 model-loading states."""
    for attempt in range(retries):
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        
        # Success
        if response.status_code == 200:
            return response, None
        
        # Model is cold-starting / loading
        if response.status_code == 503:
            st.warning(f"⏳ Model is warming up on Hugging Face servers... Retrying ({attempt + 1}/{retries})...")
            time.sleep(delay)
            continue
            
        # Other errors
        return None, f"Error {response.status_code}: {response.text}"
        
    return None, "Model loading timed out. Please click 'Generate HD Image' again in a few seconds."

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
                    
                    response, err = query_huggingface({"inputs": enhanced_prompt})
                    
                    if err:
                        st.error(err)
                    else:
                        image_bytes = response.content
                        image = Image.open(io.BytesIO(image_bytes))
                        
                        st.image(image, caption="Generated Output (1024x1024)", use_container_width=True)
                        
                        st.download_button(
                            label="⬇️ Download Full-Res Image",
                            data=image_bytes,
                            file_name="mahashank_design.png",
                            mime="image/png"
                        )
                        st.success("Generation Complete!")
                        
                except Exception as e:
                    st.error(f"Generation failed: {str(e)}")
