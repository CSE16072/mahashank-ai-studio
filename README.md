# Mahashank AI Studio

Permanent, 24/7 accessible generative AI web application built for **Mahashank Design & Technology Company**. Designed for product coordinators to instantly generate commercial mockups, smart home tech visualizations, and industrial design concepts completely free with zero paywalls, rate limits, or credit card requirements.

---

## 🚀 Live Application
* **App URL:** [Mahashank AI Studio](https://g7ydsq6cdvqum7nwz6biis.streamlit.app)
* **Access Level:** Publicly accessible 24/7 via any standard web browser (PC, tablet, mobile). No account login or setup required.

---

## 🛠️ Technical Architecture

To ensure 100% uptime and bypass legacy serverless routing deprecations (`410 Gone`, `402 Payment Required`, and DNS Name Resolution errors), the application runs on a **resilient dual-engine architecture** managed inside `app.py`:

1. **Engine 1 (Primary - Hugging Face v1 Router):** Attempts to route requests securely through the official Hugging Face v1 Inference API endpoints using an optional secret token (`HF_TOKEN`).
2. **Engine 2 (Automatic Zero-Key Fallback):** If the primary endpoint encounters high traffic, cold-start latency, or routing changes, the app **instantly and silently falls back** to a high-speed, free FLUX rendering engine (`Pollinations.ai`). This guarantees that your coordinator **never encounters error screens or failed generations**.

### Core Dependencies (`requirements.txt`)
* `streamlit` – Powers the interactive web user interface.
* `requests` – Handles secure API calls and failover routing.
* `Pillow` – Manages high-resolution image processing and display formatting.

---

## 💡 How to Use (For Coordinators)

1. Open the live application link in any browser.
2. Enter a detailed commercial description into the **Design Prompt** text area (e.g., smart home hubs, industrial casings, product mockups).
3. Click **Generate HD Image**.
4. Once rendered, preview the high-definition visual and click **⬇️ Download Full-Res Image** to save the 1024x1024 PNG asset directly to your local machine.

---

## ⚙️ Local Development & Deployment

If you ever need to clone or redeploy this repository:

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
   cd your-repo-name
