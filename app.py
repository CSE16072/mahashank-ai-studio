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

# Fetch Token securely
HF_TOKEN = st.secrets.get("HF_TOKEN", os.getenv("HF_TOKEN", ""))

# Native Free Serverless Inference Endpoint (No third-party provider billing)
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

def query_free_api(payload, retries=5, delay=10):
    """Queries Hugging Face free serverless API with cold-start 503 handling."""
    for attempt in range(retries):
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        
        if response.status_code == 200:
            return response.content, None
            
        if response.status_code == 503:
            st.warning(f"⏳ Model is waking up on free serverless tier... Retrying ({attempt + 1}/{retries})...")
            time.sleep(delay)
            continue
            
        return None, f"Error {response.status_code}: {response.text}"
        
    return None, "Model loading timed out. Please try clicking 'Generate HD Image' again."

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
            with st.spinner("⚡ Generating design via Free Serverless API..."):
                try:
                    enhanced_prompt = f"{prompt}, high definition, 8k resolution, crisp commercial texture, professional studio lighting, Mahashank design aesthetic"
                    
                    image_bytes, err = query_free_api({"inputs": enhanced_prompt})
                    
                    if err:
                        st.error(err)
                    else:
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
