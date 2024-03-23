import typer
from dotenv import load_dotenv

from .crews import FinancialCrew

load_dotenv()


app = typer.Typer()


@app.command()
def run_report_agent(symbol: str):
    """Run the FinancialCrew agent."""
    print("## Welcome to Report Creator Crew")
    print("-------------------------------")
    mycrew = FinancialCrew(symbol)
    result = mycrew.run()
    print("\n\n########################")
    print("## Here is your result:")
    print("########################\n")
    print(result)
