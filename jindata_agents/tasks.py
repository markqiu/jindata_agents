from textwrap import dedent

from crewai import Task


class MarkdownReportCreationTasks:
    def __tip_section(self):
        return "You *MUST* do your best and if done well, I will give 10000 dollars!"

    def parse_input(self, agent, data: str):
        return Task(
            description=dedent(
                f"""
            **Task**: 使用工具(tool)从输入中抽取 symbol和数据名称列表.
            **Description**: 使用工具(tool)从输入中抽取出 symbol和数据名称列表

            **Parameters**:
            - input: {data}

            **Notes**
            {self.__tip_section()}
            """
            ),
            agent=agent,
            expected_output="""一个包含 symbol和数据名称的字典
            Example output: `{'symbol': 'SH600519', 'data_names': ['收盘价', '总资产']}`""",
        )

    def get_data_from_api(self, agent, context):
        return Task(
            description=dedent(
                f"""
            **Description**: 首先对所有要获取的数据按照data_type分组,对每组数据,分别使用工具传入适当的参数获取所有的symbol的该分组数据。
            如果不知道数据属于哪个分组,则采用缺省的data_type参数,即'factor'。

            **Notes**
            You MUST use jindta to get data that the client requests. You may have to complete this task multiple times.
            {self.__tip_section()}
            """
            ),
            agent=agent,
            context=context,
            expected_output="""A list of the data retrieved for each one.
            Example output: [
                {data_name:'总资产', data: [...data_points],
                {data_name:'营业收入', data: [...data_points],
                {...}
                ]""",
        )

    def create_charts(self, agent, context) -> Task:
        return Task(
            description=dedent(
                f"""
                Create graphics of the data representing financial metrics of a company.  DO NOT change the metric name when you create the title of the chart.

                {self.__tip_section()}
            """
            ),
            agent=agent,
            context=context,
            expected_output="""
                A list of the file locations of the created charts.
                Example output: [总资产.png, 营业收入.png]
                """,
        )

    def write_markdown(self, agent, context):
        return Task(
            description=dedent(
                f"""
                **Task**: Insert markdown syntax to md file
                **Description**: Take the input file location and insert it into a markdown file.
                For Example: writes ![](总资产.png) to markdown file.

                YOU MUST USE MARKDOWN SYNTAX AT ALL TIMES.

                **Notes**
                {self.__tip_section()}
            """
            ),
            agent=agent,
            expected_output="""A report.md file formatted in markdown syntax.
            Example output:
                ![](./营业收入.png)\n
                ![](./总资产.png)
                """,
            context=context,
        )
