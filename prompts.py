from haystack.nodes import PromptNode, PromptTemplate
from haystack import Pipeline
from haystack_memory.prompt_templates import memory_template
from haystack_memory.memory import MemoryRecallNode
from haystack_memory.utils import MemoryUtils

from haystack.agents import Agent, Tool
from utils import retriever


def pipeline(api_key, working_memory):
    QA_promptnode = PromptTemplate(
            name="zero-shot-QA",
            prompt_text="You are a helpful and knowledgeable agent. Only Answer if the {documents} contain the answer. If the user question is not related to the provided {documents}, say I don't have an answer\n"
                        "Question: {query}\n"
                        "Answer:"
        )

    QA_builder = PromptNode(model_name_or_path="gpt-3.5-turbo",
                            api_key=api_key,
                            default_prompt_template=QA_promptnode)

    pipe = Pipeline()
    pipe.add_node(component=retriever(api_key), name="Retriever", inputs=["Query"])
    pipe.add_node(component=QA_builder, name="Generator", inputs=["Retriever"])

    # Define the agent and tools
    prompt_node = PromptNode(model_name_or_path="gpt-3.5-turbo",
                                api_key=api_key,
                                max_length=512,
                                stop_words=["Observation:"])
    
    
    memory_agent = Agent(prompt_node=prompt_node, prompt_template=memory_template)
    search_tool = Tool(name="DocumentStore_QA",
                       pipeline_or_node=pipe,
                       description="Access this tool to find missing information needed to answer questions.",
                       output_variable="results")
    # if not working_memory:
    #     working_memory = []
    sensory_memory = []
    memory_node = MemoryRecallNode(memory=working_memory)
    memory_tool = Tool(name="Memory",
                    pipeline_or_node=memory_node,
                    description="Your memory. Always access this tool first to remember what you have learned.")
    
    memory_agent.add_tool(search_tool)
    memory_agent.add_tool(memory_tool)
    memory_utils = MemoryUtils(working_memory=working_memory, sensory_memory=sensory_memory, agent=memory_agent)
    return memory_utils