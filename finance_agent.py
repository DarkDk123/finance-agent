from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools

import os

os.environ["GROQ_API_KEY"] = "GROQ_API_KEY" # Change to Your API KEY!
groq = Groq(id="llama3-groq-70b-8192-tool-use-preview")

# Agent to Search the Web
web_search_agent = Agent(
    name="Web Searcher Agent",
    role="Search the web for the information",
    model=groq,  # Using llama-3.1-8b-instant with Groq
    agent_id="web-search-agent",
    tools=[DuckDuckGo()],
    instructions=["Alway include sources"],
    show_tool_calls=True,
    markdown=True,
)

# Agent to Give Financial Information
financial_agent = Agent(
    name="Finance Analyzer Agent",
    role="Analyze Financial Information with given tools",
    model=groq,
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
            company_news=True,
        ),
    ],
    instructions=["Nicely format the data", "Use tables to display the data"],
    show_tool_calls=True,
    markdown=True,
)


# A Leader agent with above agents as team members.
agent_team = Agent(
    model=groq,
    role="Leader agent for user queries with web search & financial analyst team",
    team=[web_search_agent, financial_agent],
    instructions=["Always include sources", "Use table to display the data"],
    show_tool_calls=True,
    markdown=True,
)


# Runner Code!
if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")
        agent_team.print_response(user_input, stream=True)

## We can also use phidata UI to interact with our Agents!
