import os
import streamlit as st
import fal_client

# Page Setup
st.set_page_config(
    page_title="Mahashank AI Studio",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Mahashank Design & Technology AI Generator")
st.caption("High-Definition (1024x1024) Generative AI Studio")

# Fetch API Key securely
FAL_KEY = st.secrets.get("FAL_KEY", os.getenv("FAL_KEY", ""))

col1, col2 = st.columns([1, 1])

with col1:
    prompt = st.text_area(
        "Design Prompt", 
        placeholder="e.g., A minimalist smart home device mockup, sleek matte black finish..."
    )
    negative_prompt = st.text_input(
        "Negative Prompt", 
        value="blurry, distorted, noise, text, low resolution"
    )
    generate_btn = st.button("Generate HD Image", type="primary")

with col2:
    if generate_btn and prompt:
        if not FAL_KEY:
            st.error("⚠️ FAL_KEY is missing. Please add FAL_KEY in Streamlit Secrets.")
        else:
            with st.spinner("⚡ Generating high-definition design with SDXL-Lightning..."):
                try:
                    os.environ["FAL_KEY"] = FAL_KEY
                    
                    enhanced_prompt = f"{prompt}, high definition, 8k resolution, crisp commercial texture, professional studio lighting, Mahashank design aesthetic"
                    
                    result = fal_client.subscribe(
                        "fal-ai/fast-sdxl",
                        arguments={
                            "prompt": enhanced_prompt,
                            "negative_prompt": negative_prompt,
                            "image_size": "square_hd",
                            "num_inference_steps": 4,
                            "guidance_scale": 1.0
                        }
                    )
                    
                    image_url = result["images"][0]["url"]

                    st.image(image_url, caption="Generated 1024x1024 Output", use_container_width=True)
                    st.markdown(f"[⬇️ Download Full-Res HD Image]({image_url})")
                    st.success("Generation Complete!")
                    
                except Exception as e:
                    st.error(f"Generation failed: {str(e)}")
