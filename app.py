import os
import streamlit as st
import replicate

# Page Configuration
st.set_page_config(
    page_title="Mahashank AI Studio",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 Mahashank Design & Technology AI Generator")
st.caption("High-Definition (1024x1024) Generative AI Studio")

# Fetch API token
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
                    # Set token in environment explicitly
                    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
                    
                    enhanced_prompt = f"{prompt}, high definition, 8k resolution, crisp commercial texture, professional studio lighting, Mahashank design aesthetic"
                    
                    # Call standard model slug directly without hash string
                    output = replicate.run(
                        "bytedance/sdxl-lightning-4step",
                        input={
                            "prompt": enhanced_prompt,
                            "negative_prompt": negative_prompt,
                            "width": 1024,
                            "height": 1024,
                            "scheduler": "K_EULER",
                            "num_inference_steps": 4
                        }
                    )
                    
                    # Handle response
                    image_url = output[0] if isinstance(output, list) else str(output)
                    st.image(image_url, caption="Generated 1024x1024 Output", use_container_width=True)
                    st.markdown(f"[⬇️ Download Full-Res HD Image]({image_url})")
                    st.success("Generation Complete!")
                    
                except Exception as e:
                    st.error(f"Generation failed: {str(e)}")
