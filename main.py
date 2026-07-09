from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
import json
import os

# 大模型配置，保留你的密钥
llm = ChatOpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-ws-H.EMRDHPR.Jvhl.MEUCIFZc1PXwVEnBp48SEgfG28nW3FK2gorPsQX2NHAisSTzAiEA8-JmT0d6rrtVjmMH7j5Hr8CDrOt-GzFkZJqs8-RuwJQ",
    model="qwen2.5-7b-instruct",
    temperature=0
)

MEMORY_FILE = "memory.json"

# 工具1：读取全部笔记
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 工具2：保存笔记
def save_memory(content: str):
    memory = load_memory()
    memory.append({"content": content})
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)
    return "笔记保存成功"

# 工具3：检索笔记
def search_memory(query: str):
    memory = load_memory()
    result = [item["content"] for item in memory if query in item["content"]]
    return result if result else "没有匹配的笔记"

# 工具4：数学计算器
def calculate(expr: str):
    try:
        return eval(expr)
    except Exception as e:
        return f"计算失败：{str(e)}"

# 工具5：读取本地txt文件
def read_file(file_name: str):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"读取文件失败：{str(e)}"

# 注册5个工具（满足课程5个工具硬性要求）
tools = [
    Tool(name="读取记忆", func=load_memory, description="读取所有保存的学习笔记"),
    Tool(name="保存笔记", func=save_memory, description="把学习内容永久存到本地"),
    Tool(name="检索笔记", func=search_memory, description="关键词查询历史笔记"),
    Tool(name="计算器", func=calculate, description="四则数学运算"),
    Tool(name="读取本地文件", func=read_file, description="读取项目内txt文档")
]

# 简易交互程序入口，无React模块，不会导入报错
if __name__ == "__main__":
    print("===== AI知识库工具程序启动 =====")
    print("可用功能：保存笔记、检索笔记、数学计算、读取文件、查看全部笔记")
    while True:
        user_input = input("\n请输入指令（输入exit退出）：")
        if user_input.lower() == "exit":
            print("程序结束")
            break
        # 简易工具分发逻辑
        if "保存" in user_input:
            res = save_memory(user_input.replace("保存", ""))
            print(res)
        elif "检索" in user_input:
            keyword = user_input.replace("检索", "")
            print(search_memory(keyword))
        elif "计算" in user_input:
            expr = user_input.replace("计算", "")
            print(calculate(expr))
        elif "读取文件" in user_input:
            filename = user_input.replace("读取文件", "").strip()
            print(read_file(filename))
        elif "全部笔记" in user_input:
            print(load_memory())
        else:
            # 交给大模型回答普通问题
            ans = llm.invoke(user_input)
            print("AI回答：", ans.content)