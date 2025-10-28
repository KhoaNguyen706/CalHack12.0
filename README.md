# Hungry Flow - CalHack12.0

Hungry Flow is your AI-powered multi-agent assistant for generating recipes from images and text. Upload a food photo and describe your cravings in plain English—Hungry Flow will detect ingredients, summarize your request, cook up a recipe, and advise on its quality, all with visible step-by-step progress.

## Features
- **Image-to-Recipe AI**: Upload a food image and get a custom recipe generated using advanced AI agents.
- **Multi-Agent System**: Detect, summarize, cook, and advise—each step handled by a dedicated agent for transparency and modularity.
- **Step-by-Step Progress**: See each stage of the recipe creation process in real time, with retry logic for quality improvement.
- **Sponsor Image Integration**: Easily fetch and display sponsor images using Google API, Bright Data, or Gemini-generated images.
- **Frontend/Backend Separation**: Modern React frontend and FastAPI/uAgents backend for scalability and clarity.

## Diagram
```
[User Uploads Image/Text]
        |
   [Detect Ingredients]
        |
   [Summarize Request]
        |
   [Cook Recipe]
        |
   [Advisor Quality Check]
        |
   [Retry (if needed)]
        |
   [Final Result]
```

## Instructions

### Frontend
1. Install Node.js and npm.
2. Change directory to `frontend` and run:
   ```powershell
   npm install
   npm run dev
   ```
3. Access the app at `http://localhost:5173` (or as shown in your terminal).

### Backend
1. Install Python (minimum version 3.10).
2. Change directory to `backend` and set up your environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Add your API keys to a `.env` file (see below).
4. Open two terminals:
   - Terminal 1: Run the agent system:
     ```powershell
     python agents.py
     ```
   - Terminal 2: Start the FastAPI server:
     ```powershell
     python server.py
     ```

### Environment Variables
Create a `.env` file in `backend/` with your API keys:
```
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key

```

### Use Cases
- Generate recipes from food images and text descriptions
- Visualize each step of the agent workflow in real time
- Fetch and display sponsor images for demo or branding
- Retry recipe generation for improved quality

### Audience
Anyone who wants to turn food photos and cravings into actionable recipes—home cooks, food bloggers, hackathon teams, and more. No technical expertise required!

## Demo
Watch a demo: https://www.youtube.com/watch?v=O6Mta3VZrSQ

## Quick Troubleshooting
- If you see connection errors, make sure both backend terminals are running and ports are not blocked.
- If sponsor images do not appear, check your API keys and backend logs.
- For step-by-step progress, ensure the frontend is polling the backend and delays are set for visibility.

---
For more details, see the code and comments in `frontend/` and `backend/`. Contributions and feedback welcome!
