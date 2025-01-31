#!/usr/bin/env python
import sys
import warnings
import yaml
from test_project.crew import TestProject
from test_project.tools.leaderboard_tool import LeaderboardTool

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

# def run():
#     """
#     Run the crew.
#     """
#     inputs = {
#         'topic': 'AI LLMs'
#     }
#     TestProject().crew().kickoff(inputs=inputs)



def run():
    print("## Welcome to the Game! ##")
    # with open('src/test_project/config/games.yaml', 'r', encoding='utf-8') as file:
    #     examples = yaml.safe_load(file)

    # inputs = {'game': examples['example_snake']}
    # print("## Beginning build process ##")

    # Get the crew instance
    project = TestProject()
    crew_instance = project.crew()
    
    # Run the crew and get the result
    final_result = crew_instance.kickoff()
    
    print("\n\n========================")
    print("Final code for the game:")
    print("========================\n")
    
    # Extract the actual code from the last task execution
    if final_result:
        print(final_result)
    else:
        # Fallback to Chief QA Engineer's output if needed
        print(crew_instance.tasks[-1].output)





def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        TestProject().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        TestProject().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        TestProject().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
