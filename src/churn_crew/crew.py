from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff

# Uncomment the following line to use an example of a custom tool
from churn_crew.tools.churn_ml_tool import classifyChurnMLTool, fetchData

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool


@CrewBase
class ChurnCrew:
    """ChurnCrew crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @before_kickoff  # Optional hook to be executed before the crew starts
    def pull_data_example(self, inputs):
        # Example of pulling data from an external API, dynamically changing the inputs
        results = fetchData(inputs["companyId"])
        if results is None:
            raise Exception("Failed to fetch data")
        inputs["companyData"] = results
        return inputs

    @after_kickoff  # Optional hook to be executed after the crew has finished
    def log_results(self, output):
        # Example of logging results, dynamically changing the output
        print(f"Results: {output}")
        return output

    @agent
    def data_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["data_analyst"],
            tools=[classifyChurnMLTool],
            verbose=True,
        )

    @agent
    def feature_usage_analyser(self) -> Agent:
        return Agent(
            config=self.agents_config["feature_usage_analyser"],
            verbose=True,
        )

    @agent
    def retention_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config["retention_specialist"],
            verbose=True,
        )

    @task
    def process_data(self) -> Task:
        return Task(config=self.tasks_config["process_data"], output_file="report.md")

    @task
    def classify_company_data(self) -> Task:
        return Task(config=self.tasks_config["classify_company_data"])

    @task
    def interpret_classification(self) -> Task:
        return Task(config=self.tasks_config["interpret_classification"])

    @task
    def create_retention_strategies(self) -> Task:
        return Task(config=self.tasks_config["create_retention_strategies"])

    @crew
    def crew(self) -> Crew:
        """Creates the ChurnCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
