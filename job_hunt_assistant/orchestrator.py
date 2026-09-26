import os
from crewai import Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from agents.jd_analyst import get_jd_analyst_agent, create_jd_analysis_task
from agents.resume_cl_agent import get_resume_cl_agent, create_resume_cl_task
from agents.messaging_agent import get_messaging_agent, create_messaging_task
from crewai import LLM
try:
    from utils.usajobs_api import fetch_usajobs
except ImportError:
    from usajobs_api import fetch_usajobs

from utils.tracking import log_application, save_cover_letter_file


def extract_between_markers(text, start, end=None):
    try:
        start_idx = text.index(start) + len(start)
        end_idx = text.index(end, start_idx) if end else len(text)
        return text[start_idx:end_idx].strip()
    except ValueError:
        return "Not found"


def load_resume(path="data/sample_resume.txt"):
    try:
        with open(path, "r") as file:
            return file.read()
    except FileNotFoundError:
        return "Software Developer resume"


def run_pipeline(job_data=None, resume_text=None, user_bio=""):
    # Sync API keys for Gemini / LangChain
    if "GOOGLE_API_KEY" in os.environ:
        os.environ["GEMINI_API_KEY"] = os.environ["GOOGLE_API_KEY"]

    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

    # Initialize LangChain's ChatGoogleGenerativeAI model (supports .bind())
    llm = LLM(
        model="gemini/gemini-3.5-flash-lite",
        temperature=0.7,
        api_key=api_key
    )

    # Default fallback when run directly via CLI
    if job_data is None:
        jobs = fetch_usajobs("software developer")
        job_data = jobs[0] if jobs else {}

    if isinstance(job_data, list) and len(job_data) > 0:
        job_data = job_data[0]

    if resume_text is None:
        resume_text = load_resume()

    desc = job_data.get("MatchedObjectDescriptor", {}) if isinstance(job_data, dict) else {}
    job_description = desc.get("PositionDescription", str(job_data))
    job_title = desc.get("PositionTitle", "Software Developer")
    company_name = desc.get("OrganizationName", "Federal Agency")

    analyst = get_jd_analyst_agent(llm)
    writer = get_resume_cl_agent(llm)
    messenger = get_messaging_agent(llm)

    t1 = create_jd_analysis_task(analyst, job_description)
    t2 = create_resume_cl_task(writer, resume_text, "Use job analysis output")
    t3 = create_messaging_task(messenger, job_title, company_name)

    crew = Crew(
        agents=[analyst, writer, messenger],
        tasks=[t1, t2, t3],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    # Task 12: Extract outputs and log/save files
    output_text = str(t2.output)
    resume_summary = extract_between_markers(output_text, "<<RESUME_SUMMARY>>", "<<COVER_LETTER>>")
    cover_letter = extract_between_markers(output_text, "<<COVER_LETTER>>")

    log_application(job_title, company_name, resume_summary)
    save_cover_letter_file(company_name, cover_letter)

    return result


if __name__ == "__main__":
    run_pipeline()
