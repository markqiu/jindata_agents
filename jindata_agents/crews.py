from crewai import Crew

from .agents import chart_creator, markdown_report_creator, markdown_writer
from .llms import openai_gpt35
from .tasks import MarkdownReportCreationTasks


class FinancialCrew:
    def __init__(self, data):
        self.data = data

    def run(self):
        tasks = MarkdownReportCreationTasks()

        # AGENTS
        report_agent = markdown_report_creator(openai_gpt35)
        chart_agent = chart_creator(openai_gpt35)
        markdown_agent = markdown_writer(openai_gpt35)

        # TASKS
        parse_inputs_task = tasks.parse_input(report_agent, self.data)
        retrieve_metrics_data_task = tasks.get_data_from_api(report_agent, [parse_inputs_task])
        create_chart_task = tasks.create_charts(chart_agent, [retrieve_metrics_data_task])
        create_markdown_file_task = tasks.write_markdown(markdown_agent, [create_chart_task])

        # Define your custom crew here
        crew = Crew(
            agents=[report_agent, chart_agent, markdown_agent],
            tasks=[
                parse_inputs_task,
                retrieve_metrics_data_task,
                create_chart_task,
                create_markdown_file_task,
            ],
            verbose=True,
            manager_llm=openai_gpt35,
        )

        result = crew.kickoff()
        print(crew.usage_metrics)
        return result
