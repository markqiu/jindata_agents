import secrets
from typing import List

import matplotlib.pyplot as plt
from dotenv import load_dotenv
from jindata.reader2.api import JinDataQuantReader
from langchain.tools import tool
from pydantic import BaseModel

load_dotenv()


class ExtractionTools:
    @staticmethod
    @tool("从输入中抽取symbol和数据名称列表")
    def parse_string(input: str):
        """
        Useful to extract the relevant information from the input string. Parses string and extracts the symbol and all of the relevant data name requested.
        Only the first word is the symbol and the rest are the data names.
        Output:
            {"symbol": "SH000001", "data_names": ["PE", "PB", "PCF"]}
        """
        words = input.split()
        symbol = words[0]
        result_list = {"symbol": symbol, "data_names": words[1:]}
        return result_list


class DataFetchingTools:
    @staticmethod
    @tool("通过 jindata API 获取一个或多个symbol的的数据")
    def get_data_from_jindata(
        symbols: list[str],
        data_names: list[str],
        start_date: str,
        end_date: str,
        frequency: str = "1D",
        data_type: str = "factor",
        market_name: str = "cn",
    ):
        """
        此函数用于根据给定的symbol和数据名称等参数,从jindata API一次检索一个类别(data_type)的数据。

        参数:
        symbols (list[str]): 需要获取数据的符号列表。
        data_names (list[str]): 需要获取的数据的列表。
        start_date (str): 需要获取数据的开始日期,格式为'YYYY-MM-DD'。
        end_date (str): 需要获取数据的结束日期,格式为'YYYY-MM-DD'。
        frequency (str): 需要获取数据的频率。例如,'1D'表示每日数据。注意,如果 data_type是财务因子数据,则频率只能是'1Q'或'1Y'。
        data_type (str, 可选): 需要获取的数据类型,包括行情因子数据(factor)、财务因子数据(finance)、宏观经济数据(macro)、
                              个股行业数据(industry),。默认为'factor'。
        market_name (str, 可选): 需要获取数据的市场编码。默认为'cn'。

        返回:
        pd.Dataframe: 包含检索到的以 timestamp, symbol, 收盘价, 开盘价 为列名的Dataframe。

        示例:
        1. 获取行情因子数据
            get_data_from_jindata(['SH600001', 'SZ000001'], ['收盘价', '开盘价'], '2020-01-01', '2020-12-31', '1D', 'factor', 'cn')
            返回: 行情因子数据,dataframe以 timestamp, symbol, 收盘价, 开盘价 为列名的数据表
        2.  获取财务因子数据
            get_data_from_jindata(['SH600001', 'SZ000001'], ['应收票据及应收账款', '开盘价'], '2020-01-01', '2020-12-31', '1Q', 'finance', 'cn')
            返回: 财务因子数据,dataframe以 timestamp, symbol, 收盘价, 开盘价 为列名的数据表
        3. 获取宏观经济数据
            get_data_from_jindata(['SH600001', 'SZ000001'], ['GDP:当季同比', 'GDP:当季值'], '2020-01-01', '2020-12-31', '1Q', 'macro', 'cn')
            返回: 宏观经济数据,dataframe以 timestamp, symbol, GDP:当季同比, GDP:当季值 为列名的数据表
        4. 获取个股行业数据
            get_data_from_indata(['SH600001', 'SZ000001'], '2020-01-01', '2020-12-31', '1D', 'industry', 'cn')
            返回: 个股行业数据,dataframe以 timestamp, symbol, 申万行业分类信息 为列名的数据表
        """
        load_dotenv()
        client = JinDataQuantReader()
        if data_type == "factor":
            return client.query_symbol_factors(
                symbols=symbols,
                factors=data_names,
                start_date=start_date,
                end_date=end_date,
                frequency=frequency,
                market_name=market_name,
            )
        elif data_type == "macro":
            return client.query_economic_factors(
                symbols=symbols,
                factors=data_names,
                start_date=start_date,
                frequency=frequency,
                market_name=market_name,
            )
        elif data_type == "industry":
            return client.query_symbol_industry(
                symbols=symbols,
                start_date=start_date,
                end_date=end_date,
                market_name=market_name,
            )
        elif data_type == "finance":
            return client.query_symbol_finance_factors(
                symbols=symbols,
                start_date=start_date,
                end_date=end_date,
                frequency=frequency,
                factors=data_names,
                market_name=market_name,
            )
        else:
            return "Invalid data type, please choose from 'factor', 'macro', 'industry', 'finance'."


class CreateChartInput(BaseModel):
    data_name: str
    data: List[float]


class CreateChartOutput(BaseModel):
    file_path: str


class ChartingTools:
    @staticmethod
    @tool("Create a chart of the data")
    def create_chart(data_name: str, data: List) -> CreateChartOutput:
        """
        Creates a bar chart graphic based on the provided data.

        Parameters:
        - data_name (str): The name of the metric to be visualized on the chart.
        - data (List[float]): A list of numerical data points representing the metric over time.

        Returns:
        - file_path (str): The file path to the saved chart image.

        Example:
        - create_chart(data_name='revenue', data=[100, 150, 120, 200, 180]))
        - Returns: CreateChartOutput(file_path='./{{data_name}}.png')
        """
        years = list(range(len(data)))

        # Generate a random color for all bars
        bar_color = f"#{secrets.randbelow(0xFFFFFF):06x}"

        fig, ax = plt.subplots()
        ax.bar(years, data, color=bar_color)
        ax.set_xlabel("Years")
        ax.set_title(data_name)

        # Save the figure to the current directory
        file_path = f"./{data_name.replace(' ', '_')}_chart.png"
        fig.savefig(file_path, format="png")
        plt.close(fig)  # Close the Matplotlib figure to free resources

        return CreateChartOutput(file_path=file_path)


class MarkdownTools:
    @staticmethod
    @tool("Write text to markdown file")
    def write_text_to_markdown_file(text: str) -> str:
        """Useful to write markdown text in a *.md file.
        The input to this tool should be a string representing what should used to create markdown syntax.
        Takes the location of the file as a string and creates the correct syntax thats compatible with an .md file eg report.md

         **Example** Writes `![](fcf_chart.png)` to report.md file.

        :param text: str, the string to write to the file
        """
        try:
            markdown_file_path = r"report.md"

            with open(markdown_file_path, "w") as file:
                file.write(text)

            return f"File written to {markdown_file_path}."
        except Exception:
            return "Something has gone wrong writing images to markdown file."
