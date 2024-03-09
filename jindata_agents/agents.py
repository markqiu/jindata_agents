import os
from textwrap import dedent

from crewai import Agent
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_openai import ChatOpenAI

from jindata_agents.tools import ChartingTools, DataFetchingTools, ExtractionTools, MarkdownTools

load_dotenv()

oai_api_key = os.getenv("OPENAI_API_KEY")


class FinancialResearchAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0.4, api_key=oai_api_key)
        self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4-turbo-preview", temperature=0.5)
        self.Ollama = Ollama(model="openhermes")

    def markdown_report_creator(self):
        return Agent(
            role="Markdown Report Creator",
            goal=dedent("""Retrieve accurate data of the metrics requested for a particular symbol."""),
            backstory=dedent(
                """Expert in creating markdown reports. The best at using tools to gather data from an API.
                You retrieve **EVERY** metric from QuickFS when asked and never miss a single one."""
            ),
            tools=[ExtractionTools.parse_string, DataFetchingTools.get_metric_data_from_quickfs],
            verbose=True,
            llm=self.OpenAIGPT4,
        )

    def chart_creator(self):
        return Agent(
            role="Chart Creator",
            goal=dedent("""Create a chart of the data provided using the tool."""),
            backstory=dedent(
                """Expert in creating charts. You are known for receiving a list of data points and meticulously creating an accurate chart.
                You must use the tool provided. """
            ),
            tools=[ChartingTools.create_chart],
            verbose=True,
            llm=self.OpenAIGPT4,
        )

    def markdown_writer(self):
        return Agent(
            role="Data Report Creator",
            goal=dedent("""Use *.png files in same directory to add the correct syntax a markdown file."""),
            backstory=dedent(
                """Expert in writing text inside a markdown file. You take a text input and write the contents to
                a markdown file in the same directory. You always add a new line after inserting into the markdown file.
                **YOU USE MARKDOWN SYNTAX AT ALL TIMES NO MATTER WHAT** YOU NEVER INSERT ANYTHING INTO
                THE report.md FILE THAT ISN'T MARKDOWN SYNTAX. """
            ),
            tools=[MarkdownTools.write_text_to_markdown_file],
            verbose=True,
            llm=self.OpenAIGPT4,
        )
