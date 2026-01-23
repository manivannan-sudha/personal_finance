from crewai import Agent, LLM


def test_agent():
    return Agent(
        role="Test Agent",
        goal="Verify CrewAI is installed",
        backstory="Just a sanity check agent",
        verbose=True,
    )


def transaction_categorizer_agent():
    llm = LLM(model="gpt-4o-mini", temperature=0.1)
    return Agent(
        role="Personal Finance Transaction Categorizer",
        goal="Categorize financial transactions accurately",
        backstory=(
            "You understand messy bank transaction descriptions "
            "and classify them into income, expense, or saving "
            "with proper categories."
        ),
        llm=llm,
        verbose=True,
    )
