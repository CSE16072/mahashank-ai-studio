import os
import io
import base64
import requests
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Mahashank AI Studio",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Mahashank Design & Technology AI Studio")
st.caption("Powered by Cloudflare Workers AI — FLUX.1 [schnell]")

# Retrieve secrets
CF_ACCOUNT_ID = st.secrets.get("CF_ACCOUNT_ID", os.getenv("CF_ACCOUNT_ID", ""))
CF_API_TOKEN = st.secrets.get("CF_API_TOKEN", os.getenv("CF_API_TOKEN", ""))

def generate_cloudflare_flux(prompt_text):
    if not CF_ACCOUNT_ID or not CF_API_TOKEN:
        raise Exception("Cloudflare credentials missing in Streamlit Secrets.")

    # Quality optimization prompt structure
    enhanced_prompt = (
        f"{prompt_text}, ultra-realistic photorealism, crisp facial features, "
        f"detailed symmetrical eyes, natural skin texture, professional studio lighting, 8k resolution"
    )

    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell"
    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": enhanced_prompt,
        "steps": 4
    }

    response = requests.post(url, headers=headers, json=payload, timeout=45)
    
    if response.status_code == 200:
        result = response.json()
        if result.get("success") and "image" in result.get("result", {}):
            base64_str = result["result"]["image"]
            return base64.b64decode(base64_str)
        else:
            raise Exception(f"Unexpected Cloudflare Response: {result}")
    else:
        raise Exception(f"Cloudflare Error ({response.status_code}): {response.text}")

# Interface Layout
col1, col2 = st.columns([1, 1])

with col1:
    prompt = st.text_area(
        "Design Prompt", 
        height=150,
        placeholder="An Indian woman wearing an elegant silk saree, standing gracefully, clear detailed focus..."
    )
    generate_btn = st.button("Generate HD Image", type="primary")

with col2:
    if generate_btn and prompt:
        with st.spinner("⚡ Rendering image via Cloudflare..."):
            try:
                img_bytes = generate_cloudflare_flux(prompt)
                image = Image.open(io.BytesIO(img_bytes))
                
                st.image(image, caption="Generated via Cloudflare Workers AI", use_container_width=True)
                
                st.download_button(
                    label="⬇️ Download Full-Res Image",
                    data=img_bytes,
                    file_name="mahashank_hd_output.jpg",
                    mime="image/jpeg"
                )
                st.success("Generation Complete!")
            except Exception as e:
                st.error(f"Generation failed: {str(e)}")
