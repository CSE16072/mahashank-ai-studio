import os
import io
import urllib.parse
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

HF_TOKEN = st.secrets.get("HF_TOKEN", os.getenv("HF_TOKEN", ""))

def generate_image(prompt_text):
    enhanced_prompt = f"{prompt_text}, high definition, 8k resolution, crisp commercial texture, professional studio lighting, Mahashank design aesthetic"
    
    # Engine 1: Hugging Face Router API
    if HF_TOKEN:
        try:
            hf_url = "https://router.huggingface.co/hf-inference/v1/images/generations"
            headers = {"Authorization": f"Bearer {HF_TOKEN}"}
            payload = {
                "prompt": enhanced_prompt,
                "model": "black-forest-labs/FLUX.1-schnell"
            }
            res = requests.post(hf_url, headers=headers, json=payload, timeout=25)
            if res.status_code == 200:
                data = res.json()
                if "data" in data and len(data["data"]) > 0:
                    img_res = requests.get(data["data"][0]["url"], timeout=30)
                    if img_res.status_code == 200:
                        return img_res.content, "Hugging Face Engine"
        except Exception:
            pass  # Fall through seamlessly to Engine 2

    # Engine 2: High-Speed Free Engine (FLUX.1-schnell) - Zero Key Required & Always Online
    encoded_prompt = urllib.parse.quote(enhanced_prompt)
    fallback_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&model=flux&nologo=true"
    
    res = requests.get(fallback_url, timeout=40)
    if res.status_code == 200:
        return res.content, "Free High-Speed FLUX Engine"
        
    raise Exception("Generation services are currently busy. Please try again in a few moments.")

col1, col2 = st.columns([1, 1])

with col1:
    prompt = st.text_area(
        "Design Prompt", 
        placeholder="e.g., A minimalist smart home device mockup, sleek matte black finish..."
    )
    generate_btn = st.button("Generate HD Image", type="primary")

with col2:
    if generate_btn and prompt:
        with st.spinner("⚡ Rendering high-definition commercial product image..."):
            try:
                image_bytes, engine_used = generate_image(prompt)
                image = Image.open(io.BytesIO(image_bytes))
                
                st.image(image, caption=f"Generated Output via {engine_used}", use_container_width=True)
                
                st.download_button(
                    label="⬇️ Download Full-Res Image",
                    data=image_bytes,
                    file_name="mahashank_design.png",
                    mime="image/png"
                )
                st.success("Generation Complete!")
            except Exception as e:
                st.error(f"Generation failed: {str(e)}")
