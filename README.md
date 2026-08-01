# ChefAI - Multimodal AI Recipe Agent 🍳🎙️📸

ChefAI is a smart cooking assistant backend that uses AI to generate recipes from voice commands or uploaded photos of ingredients. It is designed to power a cross-platform mobile app hosted on the Google Play Store.

## 🚀 Features
- **Photo-to-Recipe:** Analyzes pantry/fridge photos using Gemini 2.5 Flash Vision.
- **Voice Commands:** Processes audio inputs for hands-free cooking requests.
- **Monetization Ready:** Built-in tier check (Free vs. Premium users) for subscription models.

## 🛠️ Tech Stack
- **Language:** Python 3.10+
- **Framework:** FastAPI (High performance, async)
- **AI Engine:** Google Gemini 2.5 Flash API
- **Environment:** PowerShell / VirtualEnv

## 📋 Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd ai-recipe-agent
   ```

2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your Environment Variables (`.env`):**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```
   Open your browser at `http://127.0.0` to test the API endpoints interactively.

## 💰 Monetization Architecture
The app tracks user tiers (`free` vs `premium`). 
- **Free users:** Receive standard text-based recipes.
- **Premium users:** Receive nutritional breakdowns (macros), calorie counts, and smart ingredient substitutions. Change user status in the API request to test.
