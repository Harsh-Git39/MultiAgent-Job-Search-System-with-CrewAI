Multi-Agent Job Search System with CrewAI 🚀

An AI-powered job search assistant built with CrewAI, Streamlit, and Google's Gemini API. It automates the tedious parts of job hunting by analyzing job descriptions, tailoring resumes, writing custom cover letters, and tracking your applications all from a simple web interface.

🛠️ What It Does (The Agent Workflow)

The system uses a multi-agent architecture where different AI roles collaborate to prep your application:

JD Analyst: Scrapes and breaks down job descriptions to highlight key requirements, skills, and keywords.
Resume & Cover Letter Agent: Matches your background against the job requirements to tailor your resume summary and draft a personalized cover letter.
Messaging Agent: Generates custom outreach messages (like networking notes or follow-ups).
Tracking System: Automatically logs your application metadata and saves generated cover letters as text files for future reference.

🗂️ Project Structure
text
job_hunt_assistant/
│
├── agents/              # Custom CrewAI agents (JD Analyst, Resume/CL Agent, etc.)
├── data/                # Application logs and saved outputs
├── utils/               # Config, tracking, and helper scripts
├── orchestrator.py      # CrewAI pipeline configuration & task coordination
└── streamlit_app.py     # Main Streamlit web UI
⚙️ Setup & Installation
bash
git clone https://github.com/Harsh-Git39/Multi-Agent-Job-Search-System-with-CrewAI.git
cd job_hunt_assistant

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate


🔑 Environment Variables

Create a .env file in the job_hunt_assistant.utils  and add your keys:

GOOGLE_API_KEY — get a free key from Google AI Studio. This powers all four agents via Gemini.
USAJOBS_API_KEY — get one from USAJOBS Developer Portal to pull live federal job listings.


▶️ Running the App
bash
streamlit run streamlit_app.py

Then open the URL Streamlit prints in your terminal (usually http://localhost:8501). Upload or edit your resume, pick a job from the results, and hit Apply to Selected Jobs to kick off the crew.
