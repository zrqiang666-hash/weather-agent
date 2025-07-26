# 智能天气查询助手 

本项目是一个基于函数调用（Function Calling）的 AI 智能体（Agent）。它能够理解用户的自然语言提问，智能地调用一个模拟的 `get_weather` 函数来获取天气信息，并根据用户的具体指令给出格式化或推理后的回答。

## 使用的模型/API方式

* **模型 (Model)**: 本项目使用 **DeepSeek** 提供的 `deepseek-chat` 对话模型作为智能体的“大脑”。
* **API方式**: 通过 DeepSeek 官方 API 进行调用。
* **开发框架 (Framework)**: 整个项目基于 **LangChain** 框架构建。LangChain 负责处理复杂的代理逻辑（Agent Logic），包括提示词管理、工具的集成与调用、以及与 DeepSeek API 的通信。

## 如何运行/测试

请按照以下步骤在你的本地环境中运行本项目。

### 1. 准备代码
克隆本仓库或将 `main.py` 和 `.env` 文件下载到本地同一个文件夹中。

### 2. 安装依赖
在你的终端或命令行工具中，进入项目文件夹，并运行以下命令来安装所有必需的 Python 库：
```bash
pip install langchain langchain-deepseek python-dotenv
```

### 3. 配置API Key
1.  在项目根目录下，创建一个名为 `.env` 的文件。
2.  打开 `.env` 文件，并按以下格式添加你的 DeepSeek API Key。

    ```
    DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxx"
    ```
    > 你可以从 [DeepSeek 开放平台](https://platform.deepseek.com/) 免费获取你的 API Key。

### 4. 运行脚本
一切准备就绪后，在终端中运行主程序：
```bash
python main.py
```

### 5. 预期输出
程序会依次执行三个测试案例，并因为代码中设置了 `verbose=True`，你会看到详细的智能体“思考链”。最终输出结果应如下所示：

```
--- 测试案例 1: 查询存在的城市 (北京) ---
> Entering new AgentExecutor chain...
... (思考链) ...
> Finished chain.
[最终答案]: 北京今天的天气情况如下：...

==================================================

--- 测试案例 2: 查询不存在的城市 (东京) ---
> Entering new AgentExecutor chain...
... (思考链) ...
> Finished chain.
[最终答案]: 目前无法获取东京的天气信息。...

==================================================

--- 测试案例 3: 更复杂的推理查询 (深圳) ---
> Entering new AgentExecutor chain...
... (思考链) ...
> Finished chain.
[最终答案]: 深圳今天有90%的降雨概率，出门记得带伞！
```

## 哪些部分借助了 AI/搜索 完成

**框架选择与搭建**：项目的整体结构，以及选择使用 LangChain 框架来实现 Agent 的思路，是基于行业内构建 LLM 应用的最佳实践。AI 辅助生成了使用 LangChain `AgentExecutor` 和 `@tool` 装饰器的基础代码模板。





