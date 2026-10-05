# from _typeshed import importlib
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

class CodeOutput(BaseModel):
    ai_code: str = Field(description="Executable .ai stack code")
    python_code: str = Field(description="Equivalent standard Python code")

with open("system_prompt.txt", "r") as f:
    system_prompt = f.read()

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{request}")
])

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="google/gemini-2.5-flash",
    temperature=0,
    max_tokens=1500
)

model = prompt_template | llm.with_structured_output(CodeOutput)

prompt = "Calculate and print the first 10 numbers in the Fibonacci sequence."

result = model.invoke({"request": prompt})

with open("test.ai", "w") as f:
    f.write(result.ai_code.strip() + "\n")

with open("test.py", "w") as f:
    f.write(result.python_code.strip() + "\n")

print("generated test.ai and test.py")
