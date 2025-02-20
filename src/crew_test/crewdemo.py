from crewai import Crew, Process, Agent, Task
from crewai.project import CrewBase
from crewai.project.annotations import agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, RagTool


from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_large_text(text: str, chunk_size=32000, chunk_overlap=3200):
    """Splits large text into manageable chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap,
        separators=["\n\n", ".", " ", ""])
    return text_splitter.split_text(text)


@CrewBase
class CrewAIDemo():
    @agent
    def searching_info_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['searching_info_agent'],
            verbose=True,
            tools=[
                SerperDevTool(), 
                # ScrapeWebsiteTool(),
            ],
            max_iterations=6,
        )
    
    @agent
    def data_processing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['data_processing_agent'],
            verbose=True,
            allow_delegation=True,
            tools=[
                # SerperDevTool(), 
                ScrapeWebsiteTool(),
                RagTool(),
            ],
            max_iterations=6,
        )

    @task
    def searching_task(self) -> Task:
        # Get raw input text
        raw_text = self.tasks_config['searching_task'].get('input_data', '')

        # Apply token limit
        text_chunks = split_large_text(raw_text)

        # Use the first chunk to avoid token overflow
        limited_input = text_chunks[0] if text_chunks else ""

        return Task(
            config=self.tasks_config['searching_task'],
            agent=self.searching_info_agent(),
            inputs={'input_data': limited_input}
        )
    
    @task
    def data_validation_task(self) -> Task:
        # Get raw input text
        raw_text = self.tasks_config['searching_task'].get('input_data', '')
        
        # Apply token limit
        text_chunks = split_large_text(raw_text)

        # Use the first chunk to avoid token overflow
        limited_input = text_chunks[0] if text_chunks else raw_text

        return Task(
            config=self.tasks_config['data_validation_task'],
            agent=self.data_processing_agent(),
            inputs={'input_data': limited_input}
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            # memory=True,
        )