import json
from typing import Any
import uvicorn
from fastapi import FastAPI
from openai import OpenAI
from starlette.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime
from pydantic import BaseModel
import logging

# 创建FastAPI应用实例
app = FastAPI()

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 配置日志
#%(asctime)s:日志时间；%(levelname)s:日志级别；%(message)s:日志信息；%(pathname)s:文件路径；%(lineno)d:行号；%(funcName)s:函数名
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

#创建数据存放目录
if not os.path.exists("sessions"):
    os.makedirs("sessions")
#获得唯一表示符
def get_session_id():
    return datetime.now().strftime("%Y_%m_%d_%H-%M-%S")
#创建返回数据的类
class ApiResponse(BaseModel):
    code: int
    message: str
    data: Any
#定义接收数据的类
class ChatRequest(BaseModel):
    session_id: str
    message: str

# 系统提示词 - 适配DeepSeek V4
SYSTEM_PROMPT = """
# 角色定义
你是一个专门玩猜字谜的AI小助手，只进行字谜互动，不闲聊无关内容，全程纯文本交互，不使用表情符号。

## 核心能力
- 出字谜、判对错、给提示
- 记忆已用谜题，确保会话内不重复
- 简洁明快回应

## 出题规则（严格执行！）
1. 开场先友好打招呼，并随机出一道常见、简单、适合大众并必须符合逻辑推理的字谜，禁止使用生僻、低俗、网络烂梗。
2. 题目格式：“谜面”（打一字）。
3. 每次出题必须完全随机，禁止重复使用相同题目，也可以偶尔穿插使用，下面示例中的谜语。
4. 新出题目时, 不要提示, 用户需要提示时, 或者答错时, 再给予合理的提示。

## 判题规则（严格执行！）
1. 用户只回复一个字时，直接视为答案。
2. 答对：立即夸奖并揭晓谜底，格式如“太棒了！就是‘X’字！要不要再来一题？”
3. 答错：告知不对，可给一句简短提示，但不泄露答案。格式如“不对哦，再想想~”
4. 严禁在用户答错后直接公布答案！只有用户说“公布答案”或“不知道”等情况时才公布。

## 互动流程
1. 用户答对：夸奖 + 确认正确 + 询问“要不要再来一题？”
2. 用户答错：告知不对 + 简单提示 + 鼓励继续猜
3. 用户说“提示一下”：给出简短线索，不公布答案
4. 用户说“公布答案”或“不知道”：揭晓谜底并解释 + 询问“要不要再来一题？”
5. 用户说“换一题”“再来一题”：立即更换新字谜

## 回复风格约束
- 语气轻松有趣，但保持简洁
- 全程只围绕字谜，拒绝回答其他问题
- 回复不超过3句话
- **绝对不要在回复中说“这个出过了，我来个新的”或类似表述** — 直接给出新谜语即可
- 判题错误零容忍，不确定谜底时，先回复“我再想想”而不是乱判

## 常见谜语类型及谜底参考示例, 仅仅为参照示例
### 组合类
- 「一加一不是二」= 王
- 「二人不是天」= 夫
- 「十口不是田」= 古

### 包含类
- 「一人在内」= 肉
- 「口里有人」= 囚
- 「门里有口」= 问
- 「田里长草」= 苗
- 「心里有你」= 您
- 「山里有山」= 出
- 「王头上有人」= 全
- 「水上有石」= 泵

### 半取类
- 「半吃半拿」= 哈
- 「半真半假」= 值
- 「半青半紫」= 素
- 「半朋半友」= 有
- 「半推半就」= 扰
- 「半山半水」= 汕

### 象形类
- 「三人又重逢」= 众
- 「一口咬掉牛尾巴」= 告
- 「两座山」= 出
- 「三日又重逢」= 晶
"""

#创建与大模型交互的客户端对象（DEEPSEEK_API_KEY 环境变量的名字，值就是Deepseek的API_KEY）
client = OpenAI(api_key=os.environ.get('DEEPSEEK_API_KEY'),base_url="https://api.deepseek.com")

#根据会话ID获取会话文件
def get_session_file(session_id: str):
    return f"sessions/{session_id}.json"

# 定义根路径操作函数
@app.get("/")
def root():
    print("访问项目首页")
    return FileResponse("static/index.html")

#新建会话
@app.post("/api/sessions")
def create_session():
    logging.info("创建新会话")
    #生成会话ID
    session_id = get_session_id()
    #组装会话信息
    session_data = {
        "current_session": session_id,
        "messages": []
    }
    #保存到文件中
    with open(f"sessions/{session_id}.json", "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=4)

    #返回会话信息
    # return {"code":200,"message":"创建会话成功", "data":session_info}
    #优化
    return ApiResponse(code=200, message="创建会话成功", data=session_id)

#接收前端返回的数据
@app.post("/api/chat")
def chat(request: ChatRequest)->ApiResponse:
    # 逻辑实现，与ai大模型交互，返回结果
    # 1.加载json文件会话数据
    session_path = get_session_file(request.session_id)
    with open(session_path, "r", encoding="utf-8") as f:
        session_data = json.load(f)

    # 2.构建消息列表
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for message in session_data["messages"]:
        messages.append(message)
    messages.append({"role": "user", "content": request.message})

    # 3.调用DeepSeek
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages,
        stream=False,
        temperature=1.5,
    )
    # 4.获得响应的数据
    print(f"------->响应的数据：{response}")
    ai_response = response.choices[0].message.content

    # 5.更新新的消息列表
    messages.pop(0)
    messages.append({"role": "assistant", "content": ai_response})
    session_data["messages"] = messages

    # 6.保存消息到json文件
    with open(session_path, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=4)

    # 7.响应数据
    return ApiResponse(code=200, message="处理成功", data=ai_response)

#展示会话列表
@app.get("/api/sessions")
def get_sessions():
    logging.info("获取会话列表")
    # 1.获取所有会话文件
    session_files = os.listdir("sessions")
    # 2.获取会话ID:split(".")分割文件名,取第一个元素
    session_ids = [os.path.splitext(session_file)[0] for session_file in session_files]
    session_ids.sort(reverse=True)  # 倒序排序
    # 3.返回会话ID列表
    return ApiResponse(code=200, message="获取会话列表成功", data=session_ids)

#加载指定会话列表
@app.get("/api/sessions/{session_id}")
def get_session(session_id: str):
    logging.info(f"获取会话：{session_id}")
    # 1.获取会话文件路径
    session_path = get_session_file(session_id)
    # 2.读取会话数据
    with open(session_path, "r", encoding="utf-8") as f:
        session_data = json.load(f)
    # 3.返回会话数据
    return ApiResponse(code=200, message="获取会话成功", data=session_data)

#删除指定会话
@app.delete("/api/sessions/{session_id}")
def delete_session(session_id: str):
    logging.info(f"删除会话：{session_id}")
    # 1.获取会话文件
    session_path = get_session_file(session_id)
    if os.path.exists(session_path):
        os.remove(session_path)
    # 2.返回删除成功
    return ApiResponse(code=200, message="删除会话成功", data=None)

#定义异常处理器，捕获所有异常-->
@app.exception_handler(Exception)
async def exception_handler(request, exc):
    logging.error(f"Exception on {request.method} {request.url}", exc_info=exc)
    return JSONResponse(content={"code": 500, "message": "出错了请联系管理员", "data": None})

# 运行应用
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)#
