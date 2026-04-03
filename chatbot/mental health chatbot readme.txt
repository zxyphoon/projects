# ✨ Aura - An AI Mental Health Companion

> A safe, anonymous, and supportive web-based chat application designed to provide an empathetic listening ear, 24/7.

Aura is a full-stack AI chatbot project that leverages modern web technologies and a powerful low-code back-end to create a responsive and intelligent conversational agent. The primary goal of Aura is to offer a non-judgmental space for users to express their feelings, explore wellness techniques, and, in critical moments, be guided toward professional help.

This project emphasizes ethical AI design, with a robust, non-AI-driven safety system as its core feature.

---

## 📸 Screenshot

![Aura Chat Interface](https://i.imgur.com/g9JmR7W.png)
*(Replace this with a screenshot of your final application)*

---

## 🚀 Key Features

*   **Empathetic AI Conversation:** Powered by Google's Gemini API and a carefully crafted system prompt, Aura provides warm, validating, and human-like responses.
*   **Critical Safety Intervention:** The system uses a deterministic, keyword-based check to identify users in crisis. It bypasses the AI entirely to provide immediate, localized helpline information.
*   **Supportive Guidance:** Aura is designed to gently suggest well-established, low-risk wellness techniques (like mindful breathing and grounding exercises) without ever giving prescriptive advice.
*   **Modern & Calming UI:** The front-end is designed to be clean, intuitive, and visually calming, featuring a gentle animated gradient background and a real-time typing indicator for a better user experience.
*   **Privacy-Focused Architecture:** Built with n8n, the entire back-end can be self-hosted, ensuring complete control over user data and conversations.

---

## 🔧 Technology Stack

*   **Front-End:**
    *   HTML5
    *   CSS3 (with custom animations)
    *   Vanilla JavaScript (ES6+, async/await, Fetch API)
*   **Back-End:**
    *   **n8n:** A low-code automation platform used to orchestrate the entire server-side logic, from receiving requests to calling the AI API.
*   **AI Service:**
    *   **Google Gemini API:** The core Large Language Model used for generating conversational responses.

---

## 🏁 Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

*   A running **n8n** instance (self-hosted via Docker or local npm install is recommended).
*   A **Google AI API Key** from [Google AI Studio](https://ai.google.dev/).
*   **Node.js** installed on your machine (to run a local web server). The `live-server` package is recommended.

### 1. Back-End Setup (n8n)

1.  **Import the Workflow:** Copy the workflow JSON from our conversation and paste it onto your n8n canvas.
2.  **Create Gemini Credential:** In the `Google Gemini` node, create a new credential and add your Google AI API Key.
3.  **Configure CORS:** This is a critical step. You must configure your n8n instance to accept requests from the front-end's origin. Set the following environment variable for your n8n instance (e.g., in your `docker-compose.yml` or your system environment):
    ```
    N8N_CORS_ALLOWED_ORIGINS=http://127.0.0.1:5500
    ```
    *(Restart n8n after setting the variable)*
4.  **Activate the Workflow:** Click the toggle switch in the top-right of your n8n canvas to set the workflow to **"Active"**.

### 2. Front-End Setup

1.  Clone this repository or create a folder with the three front-end files: `index.html`, `style.css`, and `script.js`.
2.  Populate these files with the code provided.
3.  **Update the Webhook URL:** This is the most important step.
    *   In your n8n workflow, click the `Webhook` node and copy the **Production URL**.
    *   Open `script.js` and paste this URL into the `N8N_WEBHOOK_URL` constant.
    ```javascript
    const N8N_WEBHOOK_URL = 'YOUR_N8N_PRODUCTION_URL_GOES_HERE'; 
    ```

### 3. Running the Application

1.  Open a terminal in your project folder.
2.  If you don't have `live-server`, install it globally:
    ```bash
    npm install -g live-server
    ```
3.  Start the local server:
    ```bash
    live-server
    ```
4.  Your browser will automatically open to the correct address (e.g., `http://127.0.0.1:5500`), and you can begin chatting.

---

## 🧠 n8n Workflow Overview

The back-end logic is entirely contained within a single n8n workflow:

1.  **Webhook:** The entry point. It listens for `POST` requests from the front-end.
2.  **Check for Crisis (IF Node):** Immediately scans the incoming message for crisis-related keywords.
3.  **True Path (Crisis Detected):**
    *   **Set Crisis Response:** Loads a pre-written, static message containing localized helpline numbers.
    *   **Respond to Webhook:** Instantly sends the safe message back and terminates the workflow.
4.  **False Path (No Crisis):**
    *   **Set AI Persona:** Loads the detailed system prompt that defines Aura's personality.
    *   **Google Gemini Node:** Calls the Gemini API with the persona and the user's message.
    *   **Set AI Response:** Extracts the clean text from the nested JSON response from the API.
    *   **Respond to Webhook:** Sends the final, formatted AI response back to the user.

---

## ⚠️ Ethical Disclaimer

This project is an educational proof-of-concept and **is not a substitute for professional medical advice, diagnosis, or treatment**. Aura is an AI and lacks the ability to handle a real-world mental health crisis. The crisis detection system is based on keywords and is not foolproof.

If you or someone you know is in crisis, please contact a qualified healthcare provider or a local emergency service immediately.

---

## 🔮 Future Scope

*   **Conversation Memory:** Integrate a database (e.g., Supabase, SQLite) to provide the AI with long-term memory.
*   **User Authentication:** Add an optional login system for users to save their conversation history securely.
*   **Cloud Deployment:** Host the application on a cloud platform to make it publicly accessible.
*   **Multi-Language Support:** Expand the persona and crisis detection to support additional languages.