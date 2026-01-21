from crewai import Agent

def test_agent():
    return Agent(
        role="Test Agent",
        goal="Verify CrewAI is installed",
        backstory="Just a sanity check agent",
        verbose=True
    )
