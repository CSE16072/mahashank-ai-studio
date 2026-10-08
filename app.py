import os
import streamlit as st
import replicate

# Page Setup
st.set_page_config(
    page_title="Mahashank AI Studio",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Mahashank Design & Technology AI Generator")
st.caption("High-Definition (1024x1024) Generative AI Studio")

# Retrieve Replicate API Token securely
REPLICATE_API_TOKEN = st.secrets.get("REPLICATE_API_TOKEN", os.getenv("REPLICATE_API_TOKEN", ""))

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
        if not REPLICATE_API_TOKEN:
            st.error("⚠️ API Token missing. Please add REPLICATE_API_TOKEN to Streamlit Secrets.")
        else:
            with st.spinner("⚡ Generating high-definition design with SDXL-Lightning..."):
                try:
                    # Explicitly attach token to runtime environment
                    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
                    
                    enhanced_prompt = f"{prompt}, high definition, 8k resolution, crisp commercial texture, professional studio lighting, Mahashank design aesthetic"
                    
                    # Correct active version hash for SDXL-Lightning 4-step
                    model_version = "bytedance/sdxl-lightning-4step:5599ed30703defd1d160a25a63321b4dec97101d98b4674bcc56e41f62f35637"
                    
                    output = replicate.run(
                        model_version,
                        input={
                            "prompt": enhanced_prompt,
                            "negative_prompt": negative_prompt,
                            "width": 1024,
                            "height": 1024,
                            "num_inference_steps": 4,
                            "guidance_scale": 0
                        }
                    )
                    
                    # Extract single or array image output URL
                    if isinstance(output, list) and len(output) > 0:
                        image_url = str(output[0])
                    else:
                        image_url = str(output)

                    st.image(image_url, caption="Generated 1024x1024 Output", use_container_width=True)
                    st.markdown(f"[⬇️ Download Full-Res HD Image]({image_url})")
                    st.success("Generation Complete!")
                    
                except Exception as e:
                    st.error(f"Generation failed: {str(e)}")
