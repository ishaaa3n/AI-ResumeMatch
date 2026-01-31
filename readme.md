# Resume → Live Jobs Matcher 
A cool little web app that takes your resume (PDF), reads it with local AI (no cloud needed!), and shows you real, live job postings that match your skills — right now in Pune and around!


### What it does
1. You upload your resume (PDF only)
2. Local AI (Ollama + Llama3) reads it and pulls out your skills, job title, experience, etc.
3. Searches live jobs on Jooble API (focused on Pune/Maharashtra/India)
4. Shows you matching jobs with company name, location, salary (if shown), and direct apply links

All runs on your laptop — your resume never goes to any server 😎

### Tech Stack (what I used)
- **Streamlit** → super easy web app in Python
- **Ollama** (Llama3) → local AI, no API keys or money needed
- **LangChain** → helps talk to Ollama nicely
- **PyPDF2** → reads PDF resumes
- **RAPID API** → gets real job listings (free developer key)
- Python + dotenv for secrets

### How to Run It (Step by Step)

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/resume-job-matcher.git
   cd resume-job-matcher

Create virtual environment (optional but good)
python -m venv myenv
myenv\Scripts\activate   # Windows

### Install packagesBash
pip install streamlit langchain langchain-community langchain-core langchain-classic ollama pypdf2 python-dotenv requests

### Install & run Ollama
Download from: https://ollama.com
Run in terminal:Bashollama pull llama3
ollama run llama3

### Get RAPID API key
Go to: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
Fill form → copy your key
Create file called .env in project folder:textJOOBLE_API_KEY=your-long-key-here

### Run the app!
streamlit run app.py
Open http://localhost:8501 in browser → upload your resume → wait a bit → see jobs!