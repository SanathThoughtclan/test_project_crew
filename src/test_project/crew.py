from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task,after_kickoff
from test_project.tools.leaderboard_tool import LeaderboardTool
import time

@CrewBase
class TestProject():
    """TestProject crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    tracker = LeaderboardTool()  # Single shared instance


    @agent
    def senior_engineer(self) -> Agent:
                return Agent(
            config=self.agents_config['senior_engineer'],
            tools=[],  # Use shared instance
            allow_delegation=False,
            verbose=True,
        )

    @agent
    def qa_engineer(self) -> Agent:
                return Agent(
            config=self.agents_config['qa_engineer'],
            tools=[],  # Use shared instance
            allow_delegation=False,
            verbose=True,
        )  

    @agent
    def chief_qa_engineer(self) -> Agent:
                return Agent(
            config=self.agents_config["chief_qa_engineer"],
            tools=[],  # Use shared instance
            allow_delegation=False,
            verbose=True,
        )

    # In all task definitions, modify the callback lambdas like this:

    @task
    def code_task(self) -> Task:
        start_time = time.time()
        task = Task(
            config=self.tasks_config['code_task'],
            agent=self.senior_engineer(),
            # Add parameter to lambda to accept the output
            callback=lambda output: self.tracker._run(
                agent_name="senior_engineer",
                execution_time=time.time() - start_time
            )
        )
        return task

    @task
    def review_task(self) -> Task:
        start_time = time.time()
        task = Task(
            config=self.tasks_config['review_task'],
            agent=self.qa_engineer(),
            # Add parameter to lambda to accept the output
            callback=lambda output: self.tracker._run(
                agent_name="qa_engineer",
                execution_time=time.time() - start_time
            )
        )
        return task

    @task
    def evaluate_task(self) -> Task:
        start_time = time.time()
        task = Task(
            config=self.tasks_config['evaluate_task'],
            agent=self.chief_qa_engineer(),
            # Add parameter to lambda to accept the output
            callback=lambda output: self.tracker._run(
                agent_name="chief_qa_engineer",
                execution_time=time.time() - start_time
            )
        )
        return task

    @crew
    def crew(self) -> Crew:
        """Creates the TestProject crew"""
        print(f"Agents in the crew: {self.agents}")
        print(f"Tools in the crew: {self.tasks}")
        return Crew(
            agents=self.agents, 
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True,
        )

    @after_kickoff
    def display_leaderboard(self, result) -> None:
        """Display leaderboard after execution"""
        print("\n\n========================")
        print("Agent Performance Metrics:")
        print("==========================")
        print(self.tracker.display_leaderboard())
        print("==========================\n\n")