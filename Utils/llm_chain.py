from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

# Prompt template for commit message generation
prompt_template = PromptTemplate(
    input_variables=["diff_summary"],
    template="""
You are an expert at writing concise and descriptive git commit messages.
Given the following code changes, generate a commit message that summarizes the intent:

{diff_summary}
"""
)

def generate_commit_message(diff_summary):
    """
    Uses LangChain and OpenAI to generate a commit message from a diff summary.
    Requires OPENAI_API_KEY to be set in the environment.
    """
    llm = ChatOpenAI(temperature=0.2)
    chain = LLMChain(llm=llm, prompt=prompt_template)
    return chain.run(diff_summary=diff_summary) 