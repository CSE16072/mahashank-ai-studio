# 🎨 Mahashank AI Studio

A 24/7 high-definition ($1024 \times 1024$) Generative AI web application tailored for commercial product designs, mockups, and visual workflows at **Mahashank Design & Technology**.

---

## 🚀 Key Features

* **Instant Generation:** Powered by **ByteDance SDXL-Lightning (4-step distilled UNet)** for 1 to 2 second image synthesis.
* **Commercial Quality Output:** Native $1024 \times 1024$ resolution with automatic prompt-engineering enhancements for studio lighting and commercial finishes.
* **24/7 Cloud Availability:** Decoupled serverless architecture hosted on Streamlit Cloud and powered by Replicate API—eliminating local GPU dependencies and server downtime.
* **Direct Download:** One-click full-resolution PNG image exporter.

---

## 🛠️ Architecture & Tech Stack

| Component | Technology |
| :--- | :--- |
| **Frontend UI** | Streamlit |
| **Model Architecture** | Stable Diffusion XL (SDXL) Base 1.0 |
| **Distillation / UNet** | ByteDance SDXL-Lightning (4-step) |
| **Inference Engine** | Replicate Serverless API |
| **Deployment Platform** | Streamlit Community Cloud |

---

## 📂 Repository Structure

```text
mahashank-ai-studio/
├── app.py              # Main application entry point & Streamlit interface
├── requirements.txt    # Production Python dependencies
└── README.md           # Project documentation
