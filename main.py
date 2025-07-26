# main.py

import os
import json
from typing import Type

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import tool
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages

# --- 1. 环境设置 ---
load_dotenv()

if "DEEPSEEK_API_KEY" not in os.environ:
    print("错误：请在 .env 文件中设置 DEEPSEEK_API_KEY 环境变量。")
    exit()


# --- 2. 定义工具 ---
@tool
def get_weather(city: str) -> str:
    """当你需要查询指定城市的天气时，使用此函数。"""
    city_map = {
        "beijing": "beijing",
        "北京": "beijing",
        "shenzhen": "shenzhen",
        "深圳": "shenzhen"
    }
    lookup_key = city.lower()
    data_key = city_map.get(lookup_key)

    weather_data = {
        "beijing": {
            "location": "北京",
            "temperature": "12°C",
            "current": "32",
            "low": "8",
            "high": "35",
            "rain_probability": 10,
            "humidity": 40
        },
        "shenzhen": {
            "location": "深圳",
            "temperature": "28°C",
            "current": "28",
            "low": "25",
            "high": "31",
            "rain_probability": 90,
            "humidity": 85
        }
    }

    if data_key and data_key in weather_data:
        return json.dumps(weather_data[data_key], ensure_ascii=False)
    else:
        return json.dumps({"error": "Weather unavailable for this city"}, ensure_ascii=False)


# --- 3. 创建智能体 ---
llm = ChatDeepSeek(model="deepseek-chat", temperature=0)
tools = [get_weather]

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个乐于助人的天气查询助手。你有工具可以查询天气，请使用中文回答用户的问题。"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

llm_with_tools = llm.bind_tools(tools)

agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
        }
        | prompt
        | llm_with_tools
        | OpenAIToolsAgentOutputParser()
)

# --- 4. 创建智能体执行器 ---
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- 5. 运行智能体并测试 ---
if __name__ == "__main__":
    print("--- 测试案例 1: 查询存在的城市 (北京) ---")
    query1 = "你好，请问北京今天天气怎么样？"
    response1 = agent_executor.invoke({"input": query1})
    print("\n[最终答案]:", response1["output"])

    print("\n" + "=" * 50 + "\n")

    print("--- 测试案例 2: 查询不存在的城市 (东京) ---")
    query2 = "东京的天气如何？"
    response2 = agent_executor.invoke({"input": query2})
    print("\n[最终答案]:", response2["output"])

    print("\n" + "=" * 50 + "\n")

    print("--- 测试案例 3: 更复杂的推理查询 (深圳) ---")
    query3 = "查找深圳的天气，然后用一句话告诉我出门要不要带伞"
    response3 = agent_executor.invoke({"input": query3})
    print("\n[最终答案]:", response3["output"])