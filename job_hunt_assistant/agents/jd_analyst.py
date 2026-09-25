from crewai import Agent, Task

from utils.config import GEMINI_API_KEY



def get_jd_analyst_agent(llm):
    print("MY EDIT IS RUNNING")
    return Agent(
        role="JD Analyst",
        goal="Understand and summarize government job postings",
        backstory="You're an expert in job market analysis with a focus on US federal job listings.",
        llm=llm,
        verbose=True
    )

def create_jd_analysis_task(agent, job_description):
    return Task(
        description=f"""
        Analyze the following USAJobs job posting and extract:
        - A summary of the role
        - Key skills required
        - Any specific qualifications or eligibility
        \n\nJob Description:\n{job_description}
        """,
        expected_output="A structured markdown summary containing sections for Qualifications, Required Skills, and Responsibilities.",
        agent=agent,
        output_file='/data/report.md'
    )