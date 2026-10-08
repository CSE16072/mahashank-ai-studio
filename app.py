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

# Fetch API token securely from Streamlit secrets
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
                    # Pass token to environment for Replicate client
                    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
                    
                    enhanced_prompt = f"{prompt}, high definition, 8k resolution, crisp commercial texture, professional studio lighting, Mahashank design aesthetic"
                    
                    # Full model identifier with active version hash
                    model_version = "bytedance/sdxl-lightning-4step:5579f57372338770025516b31c30248384282a54e954546c24389146197fa37c"
                    
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
                    
                    # Parse image output URL
                    if isinstance(output, list) and len(output) > 0:
                        image_url = str(output[0])
                    else:
                        image_url = str(output)

                    st.image(image_url, caption="Generated 1024x1024 Output", use_container_width=True)
                    st.markdown(f"[⬇️ Download Full-Res HD Image]({image_url})")
                    st.success("Generation Complete!")
                    
                except Exception as e:
                    st.error(f"Generation failed: {str(e)}")
