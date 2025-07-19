import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.prompts import SystemMessagePromptTemplate
from Utils.tools import all_tools

load_dotenv()

system_prompt = (
    "You are a commit message generator agent. "
    "First, use the available tools to gather information about the git repository, staged changes, and parse the diff. "
    "Only after collecting this information, generate a concise and descriptive commit message."
)

system_message = SystemMessagePromptTemplate.from_template(system_prompt)


def main():
    repo_path = input("Enter the path to the git repository (or '.' for current directory): ").strip()
    openai_model = "gpt-3.5-turbo"
    llm = ChatOpenAI(temperature=0.1, model=openai_model)
    agent = initialize_agent(
        tools=all_tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        system_message=system_prompt
    )
    result = agent.run(repo_path)
    print("\nSuggested commit message:")
    print(result)

if __name__ == "__main__":
    main()
