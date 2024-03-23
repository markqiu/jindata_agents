from textwrap import dedent

from crewai import Agent

from .tools import ChartingTools, DataFetchingTools, ExtractionTools, MarkdownTools


def natural_language_data_queryer(llm, function_calling_llm=None) -> Agent:
    """
    能够抽取自然语言输入的工具,然后从数据获取工具获取某只股票的准确的数据。
    Args:
        llm:

    Returns:

    """
    return Agent(
        role="实现用自然语言查询投资数据库",
        goal=dedent("""    先用抽取工具解析输入,然后从数据获取工具获取某只股票的准确的数据。"""),
        backstory=dedent(
            """Expert in creating markdown reports. The best at using tools to gather data from an API.
            You retrieve **EVERY** data from jindata when asked and never miss a single one."""
        ),
        tools=[ExtractionTools.parse_string, DataFetchingTools.get_data_from_jindata],
        verbose=True,
        allow_delegation=False,
        llm=llm,
        function_calling_llm=function_calling_llm,
    )


def markdown_report_creator(llm, function_calling_llm=None) -> Agent:
    """
    先用抽取工具解析输入,然后从数据获取工具获取某只股票的准确的数据。
    Args:
        llm:

    Returns:

    """
    return Agent(
        role="Markdown报告创建者",
        goal=dedent("""    先用抽取工具解析输入,然后从数据获取工具获取某只股票的准确的数据。"""),
        backstory=dedent(
            """Expert in creating markdown reports. The best at using tools to gather data from an API.
            You retrieve **EVERY** data from jindata when asked and never miss a single one."""
        ),
        tools=[ExtractionTools.parse_string, DataFetchingTools.get_data_from_jindata],
        verbose=True,
        allow_delegation=False,
        llm=llm,
        function_calling_llm=function_calling_llm,
    )


def chart_creator(llm, function_calling_llm=None) -> Agent:
    """
    Create a chart of the data provided using the tool.
    Args:
        llm:

    Returns:

    """
    return Agent(
        role="Chart Creator",
        goal=dedent("""Create a chart of the data provided using the tool."""),
        backstory=dedent(
            """Expert in creating charts. You are known for receiving a list of data points and meticulously creating an accurate chart.
            You must use the tool provided. """
        ),
        tools=[ChartingTools.create_chart],
        verbose=True,
        llm=llm,
        function_calling_llm=function_calling_llm,
    )


def markdown_writer(llm, function_calling_llm=None) -> Agent:
    """
    Use *.png files in same directory to add the correct syntax a markdown file.
    Args:
        llm:

    Returns:

    """
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
        llm=llm,
        function_calling_llm=function_calling_llm,
    )
