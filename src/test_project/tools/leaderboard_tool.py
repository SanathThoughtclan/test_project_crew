from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict

# Define the input schema for the Leaderboard Tool (optional)
class LeaderboardToolInput(BaseModel):
    """Input schema for the LeaderboardTool."""
    agent_name: str = Field(..., description="Name of the agent whose performance is being tracked.")

class LeaderboardTool(BaseTool):
    name: str = "LeaderboardTool"
    description: str = "Tracks agent performance and displays metrics after execution."
    args_schema: Type[BaseModel] = LeaderboardToolInput

    performance_data: Dict[str, Dict[str, float]] = {}
    def __init__(self):
        super().__init__()  # Ensure BaseTool initializes properly
        #self.performance_data: Dict[str, Dict[str, float]] = {}  # Initialize dictionar

    def _run(self, agent_name: str, execution_time: float) -> str:
        """Tracks the performance of agents during execution."""
        
        if agent_name not in self.performance_data:
            self.performance_data[agent_name] = {
                "executions": 0,
                "total_time": 0.0
            }
        
        # Increment the number of executions for this agent
        self.performance_data[agent_name]["executions"] += 1
        self.performance_data[agent_name]["total_time"] += execution_time

        return f"Performance for {agent_name} tracked successfully."

    def display_leaderboard(self) -> str:
        """Displays the leaderboard with agent performance metrics."""
        leaderboard = []
        for agent, data in self.performance_data.items():
            avg_time = data["total_time"] / data["executions"] if data["executions"] > 0 else 0
            # Format with clear numerical separation
            leaderboard.append(
                f"{agent}: "
                f"Executions={data['executions']}, "
                f"AvgTime={avg_time:.2f}s"
            )
        
        # Sort by average time (ascending)
        leaderboard.sort(key=lambda x: float(x.split("AvgTime=")[1].replace("s", "")), reverse=False)
        
        return "\n".join(leaderboard)
