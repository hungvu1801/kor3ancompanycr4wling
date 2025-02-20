from src.crew_test.crewdemo import CrewAIDemo
from dotenv import load_dotenv
import agentops
import os
load_dotenv()

if __name__ == "__main__":
    agentops.init(os.getenv('AGENTOPS_API_KEY'))
    inputs = {
        "company_name_kor": "주식회사 일상의친구",
        "company_name_eng": "a daily friend"
    }
    CrewAIDemo().crew().kickoff(inputs=inputs)