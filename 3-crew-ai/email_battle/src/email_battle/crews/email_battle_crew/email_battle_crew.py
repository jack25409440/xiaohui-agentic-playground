from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class EmailBattleCrew:
    """Email Battle Crew - Simulates email exchanges between Elon Musk (DOGE) and John Smith (USCIS)"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # YAML configuration files
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # ==================== AGENTS ====================

    @agent
    def elon_musk(self) -> Agent:
        """Head of Department of Government Efficiency (DOGE)"""
        return Agent(
            config=self.agents_config["elon_musk"],  # type: ignore[index]
            verbose=True,
        )

    @agent
    def john_smith(self) -> Agent:
        """GS-12 Immigration Services Officer at USCIS"""
        return Agent(
            config=self.agents_config["john_smith"],  # type: ignore[index]
            verbose=True,
        )

    # ==================== TASKS ====================

    @task
    def send_mass_email(self) -> Task:
        """Elon sends mass email requesting 5 accomplishments"""
        return Task(
            config=self.tasks_config["send_mass_email"],  # type: ignore[index]
        )

    @task
    def reply_to_mass_email(self) -> Task:
        """John replies to the mass email with his 'accomplishments'"""
        return Task(
            config=self.tasks_config["reply_to_mass_email"],  # type: ignore[index]
        )

    @task
    def evaluate_initial_response(self) -> Task:
        """Elon evaluates John's response and decides: PASS or FOLLOW-UP"""
        return Task(
            config=self.tasks_config["evaluate_initial_response"],  # type: ignore[index]
        )

    @task
    def john_follow_up_response(self) -> Task:
        """John responds to Elon's follow-up questions"""
        return Task(
            config=self.tasks_config["john_follow_up_response"],  # type: ignore[index]
        )

    @task
    def elon_follow_up_evaluation(self) -> Task:
        """Elon evaluates follow-up and decides: FOLLOW-UP, TERMINATED, or RETAINED"""
        return Task(
            config=self.tasks_config["elon_follow_up_evaluation"],  # type: ignore[index]
        )

    # ==================== CREW ====================

    @crew
    def crew(self) -> Crew:
        """Creates the Email Battle Crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
