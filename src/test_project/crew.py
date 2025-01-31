from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task,after_kickoff
from test_project.tools.leaderboard_tool import LeaderboardTool
import time
import yaml


@CrewBase
class TestProject():
    """TestProject crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    tracker = LeaderboardTool()  # Single shared instance

    def __init__(self):
        with open('src/test_project/config/games.yaml', 'r') as file:
            self.games = yaml.safe_load(file)
        self.selected_game = 'example_snake'

    def _inject_game_instructions(self, task_config):
        """Inject game instructions into task descriptions"""
        game_content = self.games[self.selected_game]
        task_config['description'] = task_config['description'].format(game=game_content)
        return task_config

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
        task_config = self._inject_game_instructions(
            self.tasks_config['code_task'].copy()
        )
        task = Task(
            config=task_config,
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
        task_config = self._inject_game_instructions(
            self.tasks_config['review_task'].copy()
        )
        task = Task(
            config=task_config,
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
        task_config = self._inject_game_instructions(
            self.tasks_config['evaluate_task'].copy()
        )
        task = Task(
            config=task_config,
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
        """Creates the Crew with preloaded game instructions"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            inputs={
                'game': self.games[self.selected_game]
            },  # Auto-injects the game content
            verbose=True,
        )

    def set_game(self, game_name: str):
        """Optional method to change games dynamically"""
        if game_name in self.games:
            self.selected_game = game_name
        else:
            raise ValueError(f"Game '{game_name}' not found in config")
        

    @after_kickoff
    def display_leaderboard(self, result) -> None:
        """Display leaderboard after execution"""
        print("\n\n========================")
        print("Agent Performance Metrics:")
        print("==========================")
        print(self.tracker.display_leaderboard())
        print("==========================\n\n")