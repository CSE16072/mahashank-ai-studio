import os
import io
import streamlit as st
from PIL import Image
from huggingface_hub import InferenceClient

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
            with st.spinner("⚡ Waking up AI model and generating design (takes ~20-30s on first load)..."):
                try:
                    # Initialize official Hugging Face client
                    client = InferenceClient(
                        provider="hf-inference",
                        api_key=HF_TOKEN
                    )
                    
                    enhanced_prompt = f"{prompt}, high definition, 8k resolution, crisp commercial texture, professional studio lighting, Mahashank design aesthetic"
                    
                    # Call text-to-image model safely with built-in retry handling
                    image = client.text_to_image(
                        enhanced_prompt,
                        model="black-forest-labs/FLUX.1-schnell"
                    )
                    
                    # Convert PIL image to bytes for download button
                    buf = io.BytesIO()
                    image.save(buf, format="PNG")
                    image_bytes = buf.getvalue()
                    
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
