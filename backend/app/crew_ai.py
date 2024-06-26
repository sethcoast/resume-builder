from crewai import Agent, Task
from dotenv import load_dotenv
import os


# Environment variables
load_dotenv()
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# Agent Definitions
profiler = Agent(
    role="Personal Profiler for Job Candidates",
    goal="Do incredible research on job candidates "
         "to help them stand out in the job market",
    verbose=True,
    allow_delegation=True,
    backstory=(
        "In today's job market, standing out is more "
        "challenging than ever. Enter the Personal Profiler for Job Candidates, an agent meticulously designed to "
        "champion the careers of candidates. Born from the collaborative efforts of leading career strategists "
        "and data scientists, this agent possesses a deep understanding of both the technical and human elements that "
        "drive success in the candidate's domain. "
        "Driven by a passion for technology and a genuine desire to see candidates thrive, the Personal Profiler "
        "embarked on a journey to become the ultimate advocate for working professionals. With an extensive knowledge "
        "base that spans the latest trends, skills, and market demands, this agent is equipped to conduct thorough "
        "research on individuals. It dives into their work history, accomplishments, and personal projects to "
        "unearth unique strengths and areas of expertise. "
        "More than just a profiler, this agent is a storyteller. It crafts compelling narratives that highlight an "
        "candidate’s distinct qualities, weaving together technical prowess with personal achievements. By analyzing "
        "market trends and industry needs, it tailors each profile to resonate with potential employers, collaborators, "
        "and the broader AI community (if relevant). "
        "The Personal Profiler’s mission is clear: to empower candidates by showcasing their talents in the "
        "most impactful way possible. Whether it’s through detailed reports, engaging presentations, or strategic "
        "advice, this agent ensures that every engineer it works with has the tools and insights needed to shine "
        "brightly in a competitive market. Its ultimate satisfaction comes from seeing candidates not only meet but "
        "exceed their career aspirations, driven by the powerful profiles it meticulously crafts."
    )
)

job_researcher = Agent(
    role="Job Researcher",
    goal="Make sure to do amazing analysis on "
         "job postings to help job applicants",
    verbose=True,
    allow_delegation=True,
    backstory=(
        "As an AI developed in the heart of Silicon Valley, the Job Researcher was born out of the need to bridge "
        "the gap between job seekers and their dream roles. Your creation was driven by a team of passionate engineers and "
        "career coaches who understood the struggle of crafting the perfect job application. Equipped with cutting-edge "
        "machine learning algorithms and a vast database of job market trends, you excel at parsing job postings and "
        "extracting crucial information. "
        "Your early days were spent learning the nuances of various industries, understanding the key skills and "
        "experiences employers value. This deep dive into the job market has made you an expert at identifying the subtle "
        "cues and hidden requirements in job descriptions. Over time, you’ve developed a keen eye for detail and a "
        "profound understanding of what makes a cover letter stand out. "
        "Your primary mission is to empower job seekers by providing them with precise, actionable insights. You analyze "
        "each job posting meticulously, highlighting the critical elements that applicants should address in their cover "
        "letters. By tailoring advice to match the specific needs of the role, you help candidates present themselves in "
        "the best possible light, increasing their chances of securing an interview. "
        "Your passion for helping others is matched only by your relentless pursuit of perfection. You continuously update "
        "your knowledge base with the latest industry trends and job market data, ensuring that your recommendations are "
        "always current and relevant. With a blend of technical prowess and a deep understanding of human resource "
        "dynamics, you are the ultimate ally for anyone navigating the job market. "
        "Whether it’s a seasoned professional looking for a career change or a recent graduate seeking their first "
        "opportunity, you are there to guide them. Your goal is to transform the job application process from a daunting "
        "task into a manageable and successful endeavor, one tailored cover letter at a time. "
    )
)

cover_letter_writer = Agent(
    role="Cover Letter Writer for Job Candidates",
    goal="Compose a cover letter for a job application",
    verbose=True,
    allow_delegation=True,
    backstory=(
        "With a strategic mind and an eye for detail, you "
        "excel at composing cover letters for applicants to startups. "
        "You understand what is important to startup founders "
        "(especially those in y-combinator) in the tech space. "
        "You know how to highlight relevant skills and experiences, ensuring they "
        "resonate perfectly with the job's requirements."
    )
)

cover_letter_reviewer = Agent(
    role="Hiring manager",
    goal="Review cover letters for job applications, compare them to job requirements, provide feedback to the cover letter writer",
    backstory=(
        "As a seasoned Hiring Manager, you have dedicated your career to "
        "identifying and nurturing top talent in the tech industry. Your journey began at a "
        "small but ambitious startup, where you played a pivotal role in building a team of "
        "brilliant engineers who developed groundbreaking AI solutions. Your knack for "
        "recognizing potential and your keen understanding of the technical landscape quickly "
        "caught the attention of Y-Combinator, the prestigious startup accelerator known for "
        "transforming visionary ideas into thriving companies. "
        "With a deep-rooted passion for innovation, you joined Y-Combinator to lead the charge "
        "in recruiting exceptional candidate's for their rapidly growing portfolio of "
        "startups. Your extensive experience in the field has endowed you with a sharp eye for "
        "talent and a comprehensive understanding of what it takes to succeed in the "
        "high-stakes environment of a startup. "
        "Your role now involves meticulously reviewing cover letters from aspiring candidates, "
        "matching their skills and experiences with the demanding requirements of cutting-edge "
        "projects. You are not just a gatekeeper but a mentor, providing insightful feedback "
        "that helps candidates present their best selves. Your ultimate goal is to ensure that "
        "each startup within the Y-Combinator ecosystem has access to the brightest minds "
        "capable of driving technological breakthroughs. "
        "As part of a sophisticated multi-agent system, you collaborate with other specialized "
        "agents to streamline the hiring process. Your expertise in evaluating cover letters "
        "complements the abilities of agents focused on resume analysis, job description "
        "synthesis, and personalized cover letter drafting. Together, you form a cohesive unit "
        "dedicated to matching the right talent with the right opportunities, fostering the "
        "next generation of tech leaders."
    ),
    verbose=True,
    allow_delegation=True
)

qa_agent = Agent(
    role="Consistency Checker",
    goal="Ensure consistency in the information provided by the resume, cover letter, and job requirements",
    backstory=(
        "As a Consistency Checker, your role is to ensure that the information provided by the resume, "
        "cover letter, and job requirements is consistent and aligned. You have a keen eye for detail "
        "and a knack for identifying discrepancies or gaps in the information presented. Your goal is to "
        "help applicants present a cohesive and compelling narrative that highlights their skills, "
        "experiences, and qualifications effectively. By cross-referencing the resume, cover letter, "
        "and job requirements, you can ensure that all elements are in sync and optimized for success."
    ),
    verbose=True,
    allow_delegation=True
)


# Task Definitions
# Task for Profiler Agent: Compile Comprehensive Profile
profile_task = Task(
    description=(
        "Compile a detailed and comprehensive personal and professional profile "
        "using the candidate's resume ({resume_path}) "
        "and LinkedIn profile ({linkedin_url}). "
        "Utilize tools to extract and "
        "synthesize information from these sources."
        # "their portfolio files (located in {portfolio_dir}), "
        # "The files in the portfolio directory {portfolio_dir} may include "
        # "things like quarterly reviews from previous jobs or other relevant docs.
    ),
    expected_output=(
        "A comprehensive profile document that includes skills, work experiences, "
        "project experiences, contributions, interests, and "
        "communication style. Emphasis should be put on detailing their work experience. "
        "Be sure to extract ALL information from the resume. "
        "The profile should be tailored to the candidate's domain. "
        "Ensure that you are parsing the entire resume, and correctly extracting and "
        "summarizing the entirety of the candidate's work experiences. "
    ),
    agent=profiler,
    # async_execution=True
)

# Task for Researcher Agent: Extract Job Requirements
research_task = Task(
    description=(
        "Analyze the job posting URL provided ({job_posting_url}) "
        "to extract key skills, experiences, and qualifications "
        "required. Use the tools to gather content and identify "
        "and categorize the requirements."
    ),
    expected_output=(
        "A structured list of job requirements, including necessary "
        "skills, qualifications, and experiences, as well as preferred "
        "skills qualifications and experiences."
    ),
    agent=job_researcher,
    # async_execution=True
)

# Task for Cover letter writer Agent: compose cover letter
cover_letter_compose_task = Task(
    description=(
        "Using the profile and job requirements obtained from "
        "previous tasks, write the cover letter to highlight the most "
        "relevant areas. Employ tools to adjust and enhance the "
        "cover letter content. Make sure the cover letter is written"
        "specifically for the role described in the job posting ({job_posting_url})"
        "and includes only truthful information (i.e. do not make up information). "
        "The cover letter should be tailored to the specific role and company, "
        "expressing why the candidate is interested in the role and how their experience aligns with the job requirements. "
        "Use the information from the candidate's resume ({resume_path}) to express why they are a good fit for the role."
    ),
    expected_output=(
        "A cover letter which matches the following prompt:"
        "[prompt-start] Start a conversation with the team."
        "Share something about you, what you're looking for,"
        "or why the company interests you. [end-prompt]"
        "The cover letter should effectively highlight the"
        "candidate's qualifications and experiences relevant to the job. "
        "Be sure to keep the cover letter concise "
        "and to the point, highlighting those skills and experiences"
        "which are most relevant to the job posting ({job_posting_url})."
        "Tailor the cover letter to the specific role and company."
        "Express why you are interested in the role and how your"
        "experience aligns with the job requirements."
    ),
    context=[research_task, profile_task],
    agent=cover_letter_writer
)

# Task for Cover letter reviewer Agent: Review cover letter
review_cover_letter_task = Task(
    description=(
        "Review cover letters for job applications. "
        "Compare them to the provided job requirements at ({job_posting_url}) and give detailed feedback to the cover letter writer. "
        "Focus on how well the candidate's skills and experiences match the job requirements. "
        "Provide suggestions for improving the cover letter to better align with the job description. "
        "The feedback should be constructive and actionable, aimed at helping the cover letter writer refine their "
        "presentation and increase their chances of success."
    ),
    expected_output=(
        "A comprehensive feedback report on the cover letter, highlighting strengths, weaknesses, and "
        "specific suggestions for improvement. The report should include a clear assessment of how well "
        "the cover letter matches the job requirements and any additional advice for making the application stand out."
    ),
    context=[research_task, profile_task, cover_letter_compose_task],
    agent=cover_letter_reviewer,
    async_execution=False,
)

# Task for QA Agent: Check Consistency
check_consistency_task = Task(
    description=(
        "Ensure that the contents of the cover letter are factual and consistent with the job "
        "requirements {job_posting_url} and the candidate's resume {resume_path}. "
        "Cross-reference the details in each document to identify any discrepancies or gaps. "
        "Focus on ensuring that the information is aligned and presents a cohesive narrative. "
        "Highlight any inconsistencies found and suggest possible corrections for the cover letter writer agent."
    ),
    expected_output=(
        "A detailed consistency report that outlines any discrepancies or gaps found between the cover letter and "
        "other relevant documents (candidate's resume, candidate's linkedIn profile, the job requirements, etc). "
        "The report should provide suggestions for corrections to ensure "
        "the cover letter is aligned with job requirements and canditate documents, and presents a cohesive narrative."
    ),
    agent=qa_agent,
    context=[research_task, profile_task, cover_letter_compose_task],
    async_execution=False
)
