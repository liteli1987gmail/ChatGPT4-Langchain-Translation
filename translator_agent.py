import os

os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = ""

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.agents.agent_toolkits import create_python_agent
from langchain.tools.python.tool import PythonREPLTool
from langchain.utilities import BashProcess

bash = BashProcess()

agent_executor = create_python_agent(
    llm=OpenAI(temperature=0, max_tokens=1000),
    tool=PythonREPLTool(),
    verbose=True
)


agent_executor.run("""list all the files in the directory and filter out the ones with the allowed file types
:{[
    ".doc",
    ".docx",
    ".md",
    ".mdx",
    ".html"
]}，
The absolute paths of all the files with the allowed file types have been written to the input_paths.txt file.
如果input_paths.txt文件中有.docx和.docs的文件，则用python执行'doc_translate.py'。
观察执行这个文件的执行情况，并且输出执行打印。   


""")

# llm = OpenAI(temperature=0.7)

# tools = load_tools(['shell'],llm=llm)

# agent = initialize_agent(tools, 
#                          llm, 
#                          agent="zero-shot-react-description", 
#                          verbose=True)


