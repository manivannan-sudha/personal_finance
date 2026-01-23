from crewai import Crew
from crew.agents import transaction_categorizer_agent
from crew.tasks import categorize_transaction_task

def run_categorization(transaction: dict):
    """
    Runs the categorization agent on a transaction.
    """
    agent = transaction_categorizer_agent()
    task = categorize_transaction_task(agent, transaction)

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()

    raw_output = result.tasks_output[0].raw
    
    return raw_output