from typing import List,  Dict, Any
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from pathlib import Path
import json

# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool, WebsiteSearchTool, FileReadTool
from pydantic import BaseModel, Field, validator
import os

class JavaSpringBoot(BaseModel):
    bash: str
    feedback: str

    @validator('bash')
    def format_bash_script(cls, v: str) -> str:
        """Ensure bash script is properly formatted"""
        # Handle JSON string input
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, dict) and 'bash' in parsed:
                    v = parsed['bash']
            except json.JSONDecodeError:
                pass  # Not JSON, treat as raw bash script

        # Normalize line endings
        v = v.replace('\r\n', '\n')
        
        # Add shebang if missing
        if not v.startswith('#!/bin/bash'):
            v = '#!/bin/bash\n' + v
        
        lines = []
        in_heredoc = False
        heredoc_marker = None
        current_indent = ""
        
        for line in v.split('\n'):
            # Preserve empty lines in heredoc
            if in_heredoc and not line.strip():
                lines.append('')
                continue
                
            # Handle heredoc start
            if 'cat << ' in line:
                in_heredoc = True
                heredoc_marker = line.split('cat << ')[-1].strip("'\"")
                lines.append(line.strip())
                continue
            
            # Handle heredoc content
            if in_heredoc:
                if line.strip() == heredoc_marker:
                    in_heredoc = False
                    lines.append(heredoc_marker)
                else:
                    # Preserve exact formatting inside heredoc
                    lines.append(line)
                continue
            
            # Handle normal bash commands
            cleaned_line = line.strip()
            if cleaned_line:
                if cleaned_line.startswith(('mkdir', 'cd', 'echo', 'mvn')):
                    lines.append(cleaned_line)
                else:
                    # Preserve indentation for other commands
                    lines.append(line)
        
        return '\n'.join(lines)

    @validator('feedback')
    def format_feedback_json(cls, v: Any) -> str:
        """Ensure feedback is valid JSON with consistent formatting"""
        try:
            # Convert to dict if string
            if isinstance(v, str):
                parsed = json.loads(v)
            else:
                parsed = v
            
            # Ensure consistent formatting
            return json.dumps(parsed, indent=2, ensure_ascii=False)
        except (json.JSONDecodeError, TypeError) as e:
            raise ValueError(f"Invalid feedback format: {e}")

# arch_tool = WebsiteSearchTool()
file_read_tool = FileReadTool(
    file_path=Path('src\\tibco_to_java\\data\\tibco_credit_maintanence_project.txt'),
    description='A tool to read the tibco project file.'
)

@CrewBase
class TibcoToJavaCrew:
    """Tibco to Java crew"""
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self) -> None:             
        try:
            # self.llm = LLM(    
            # model="gemini/gemini-2.0-pro-exp-02-05",  
            # #model="gemini/gemini-2.0-flash",     
            # api_key=os.environ.get("GEMINI_API_KEY"),
            # temperature=0.7        
            # )

            self.llm = LLM(
            model="openrouter/google/gemini-2.0-pro-exp-02-05:free",
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ.get("OPEN_ROUTE_SERVICE_API_KEY"),
)
        except KeyError:
            raise EnvironmentError("GEMINI_API_KEY environment variable not set")

    @agent
    def tibco_analyze_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['tibco_analyze_agent'],
            tools=[file_read_tool],
            llm=self.llm,            
            verbose=True,
            allow_delegation=True
            
        )
    
    @agent
    def java_architect_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['java_architect_agent'],
            llm=self.llm,
            verbose=True,
            allow_delegation=True
        )
    
    # @agent
    # def review_java_agent(self) -> Agent:
    #     return Agent(
    #         config=self.agents_config['review_java_agent'],
    #         llm=self.llm,
    #         verbose=True,
    #         allow_delegation=False
    #     )
    
    @task
    def tibco_analyze_task(self) -> Task:
        return Task(
            config=self.tasks_config['tibco_analyze_task'],
            agent=self.tibco_analyze_agent()
        )

    @task
    def create_spring_boot_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_spring_boot_task'],
            agent=self.java_architect_agent(),
            context=[self.tibco_analyze_task()],
            output_json=JavaSpringBoot
        )

    # @task
    # def review_and_edit_spring_boot_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['review_and_edit_spring_boot_task'],
    #         agent=self.java_architect_agent(),
    #         context=[self.create_spring_boot_task()],
    #         output_json=JavaSpringBoot
    #     )

    @crew
    def crew(self) -> Crew:
        """Creates the Tibco to Java Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
        )