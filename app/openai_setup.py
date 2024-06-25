import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import create_openai_tools_agent, AgentExecutor
from app.tools import add, multiply
from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    MessagesPlaceholder
)

load_dotenv()

llm = AzureChatOpenAI(
    openai_api_key=os.getenv("KEY"),
    azure_endpoint=os.getenv("ENDPOINT"),
    openai_api_version=os.getenv("API_VERSION"),
    deployment_name=os.getenv("LLM_MODEL_NAME"),
    temperature=0,
)

sys_prom = "you are a helpful AI assistant which modifys the contracts based on given instructions"
messages = [
    SystemMessagePromptTemplate.from_template(sys_prom),
    HumanMessagePromptTemplate.from_template("{original_contract},{instructions}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
]

prompt = ChatPromptTemplate.from_messages(messages)

tools = [add, multiply]

agent = create_openai_tools_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=True,
    return_source_documents=True
)

def update_contract(original, instructions):
    try:
        response = agent_executor.invoke({"original_contract": original, "instructions": instructions})
        updated_contract = response['output']
    except Exception as e:
        updated_contract = f"Error: {str(e)}"
    return updated_contract
