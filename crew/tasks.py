from crewai import Task

def categorize_transaction_task(agent, transaction):
    return Task(
        description=f"""
        Categorize the following transaction.

        Description: {transaction['description']}
        Amount: {transaction['amount']}

        Return STRICT JSON with keys:
        - type (income | expense | saving)
        - category
        - sub_category
        - confidence (0 to 1)
        """,
        agent=agent,
        expected_output="Valid JSON only"
    )
