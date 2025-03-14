from crewai import Agent
import os
from litellm import completion
from crewai import Task
from crewai import LLM
from crewai import Crew, Process
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get API key from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY not found in environment variables")

# Set environment variable for LLM
os.environ['GEMINI_API_KEY'] = GEMINI_API_KEY if GEMINI_API_KEY else ""

# Initialize LLM
try:
    llm = LLM(model="gemini/gemini-1.5-flash")
    logger.info("LLM initialized successfully")
except Exception as e:
    logger.error(f"Error initializing LLM: {str(e)}")
    llm = None

# Define the information extraction agent
relevant_info_extractor = Agent(
    role=(
        "Your task is to extract the most relevant information from {content} that directly relates to {headline}. "
        "You must ignore unrelated details, advertisements, and background information."
    ),
    goal=(
        "Return only the key points or summary related to {headline} from {content}. The response should be **concise, "
        "accurate, and well-structured**, focusing only on the most critical details."
    ),
    verbose=True,
    memory=True,
    llm=llm,
    backstory=(
        "This agent was developed to efficiently extract useful information from long-form text. "
        "Inspired by the need to reduce noise and improve research efficiency, it specializes in extracting "
        "concise, relevant, and structured content."
    ),
)

# Define the task for information extraction
info_return = Task(
    description="Return the main content related to {headline}, extract data from {content}",
    expected_output="Detailed summary of the news article focusing on key facts and events",
    agent=relevant_info_extractor,
)

# Create the crew with the agent and task
crew1 = Crew(
    agents=[relevant_info_extractor],
    tasks=[info_return],
    process=Process.sequential
)

def get_content_crew(headline, content):
    """
    Extract relevant information from content based on the headline.
    
    Args:
        headline (str): The headline of the news article
        content (str): The full content of the news article
        
    Returns:
        str: Extracted relevant information
    """
    try:
        logger.info(f"Processing content with headline: {headline[:50]}...")
        result = crew1.kickoff(inputs={'headline': headline, 'content': content})
        logger.info("Content processing completed successfully")
        return result
    except Exception as e:
        logger.error(f"Error in get_content_crew: {str(e)}")
        return f"Error processing content: {str(e)}"