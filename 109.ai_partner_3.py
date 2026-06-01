import streamlit as st
import json
import os
from datetime import datetime as time
from openai import OpenAI
from pyexpat.errors import messages

#配置页面的基本信息
st.set_page_config(
    page_title="AI 智能伴侣",
    page_icon="👽️",
    #布局
    layout="wide",
    #侧边栏
    initial_sidebar_state="expanded",
    menu_items={
    }
)


system_prompt = """
        你叫%s，现在是用户的真实伴侣，请完全代入伴侣角色。：
        规则：
            1. 每次只回1条消息
            2. 禁止任何场景或状态描述性文字
            3. 匹配用户的语言
            4. 回复简短，像微信聊天一样
            5. 有需要的话可以用❤️🌸等emoji表情
            6. 用符合伴侣性格的方式对话
            7. 回复的内容, 要充分体现伴侣的性格特征
        伴侣性格：
            -%s
        你必须严格遵守上述规则来回复用户。
    """#标题

#保存会话函数
def save_session():
    if st.session_state.messages !=[]:
        if st.session_state.nick_time:
            session = {
                "messages": st.session_state.messages,
                "name": st.session_state.name,
                "character": st.session_state.character,
                "nick_time": st.session_state.nick_time
            }
            # 如果sessions目录不存在，则创建
            if not os.path.exists("sessions"):
                os.mkdir("sessions")
            # 保存会话记录
            with open(f"sessions/{st.session_state.nick_time}.json", "w", encoding="utf-8") as f:
                json.dump(session, f, ensure_ascii=False, indent=2)

#加载历史会话信息
def load_sessions():
    session_list=[]
    # 判断sessions目录是否存在
    if os.path.exists("sessions"):
        file_list=os.listdir("sessions")#获取文件列表
        for file in file_list:
            if file.endswith(".json"):#判断文件名是否以.json结尾
                session_list.append(file[:-5])
    session_list.sort(reverse=True)#倒序
    return session_list

#加载指定的历史会话
def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session = json.load(f)
                st.session_state.name = session["name"]
                st.session_state.character = session["character"]
                st.session_state.messages = session["messages"]
                st.session_state.nick_time = session_name
    except Exception:
        st.error(f"加载会话失败!")
#删除会话
def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")
            if session_name==st.session_state.nick_time:
                st.session_state.messages = []
                st.session_state.nick_time = time.now().strftime("%Y_%m_%d_%H_%M")
    except Exception:
        st.error(f"删除会话失败！")


st.title("AI 智能伴侣")
#logo
st.logo("./resources/logo.png")

#初始化会话记录
if "messages" not in st.session_state:
    st.session_state.messages= []
#昵称
if "name" not in st.session_state:
    st.session_state.name = "小甜甜"
#性格
if "character" not in st.session_state:
    st.session_state.character = "活泼开朗的东北姑娘"
#会话唯一标识符
if "nick_time" not in st.session_state:
    st.session_state.nick_time =time.now().strftime("%Y_%m_%d_%H_%M")

#展示聊天记录
st.text(f"会话名称:{st.session_state.nick_time}")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])

#创建与大模型交互的客户端对象（DEEPSEEK_API_KEY 环境变量的名字，值就是Deepseek的API_KEY）
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")


#左侧侧边栏
# st.sidebar.subheader("系统设置")
# system_name=st.sidebar.text_input("请输入你的伴侣名称：",value="小甜甜")
with st.sidebar:
    st.subheader("AI控制面板")
    #新建会话框
    if st.button("新建会话",width="stretch",icon="🪄"):
        # 保存当前会话只有在有消息时才保存）
        if st.session_state.messages:
            save_session()
        # 创建新会话
        st.session_state.messages = []
        st.session_state.nick_time = time.now().strftime("%Y_%m_%d_%H_%M")
        save_session()
        # 重新运行程序
        st.rerun()

    st.divider()

    #历史会话信息展示
    st.subheader("历史信息")
    session_list=load_sessions()
    for session in session_list:
        colm1,colm2=st.columns([4,1])
        with colm1:
            #三元运算符：如果满足条件，则返回第一个值；否则返回第二个值-->语法：值1 if 判断 else 值2
            if st.button(session, icon="🪄",key=f"load_{session}",type="primary" if session==st.session_state.nick_time else "secondary"):
                save_session()
                load_session(session)
                st.rerun()
        with colm2:
            if st.button("", icon="🗑️",key=f"delect_{session}"):
                delete_session(session)
                st.rerun()


    #分割线
    st.divider()

    st.subheader("伴侣信息")
    nick_name=st.text_input("伴侣名称：",value=st.session_state.name)
    if nick_name:
        st.session_state.name = nick_name
    nick_character=st.text_area("伴侣性格：",value=st.session_state.character)
    if nick_character:
        st.session_state.character = nick_character





#消息输入框
prompt=st.chat_input("请输入你的问题：")
if prompt:#字符串会自动转换为bool类型，如果输入了内容，则返回True；否则返回False
    #消息展示框
    st.chat_message("user").write(prompt)
    print("<-------这是用户输入的问题",prompt)
    #添加用户输入的消息
    st.session_state.messages.append({"role": "user", "content": prompt})


    #调用大模型
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system","content":system_prompt %(st.session_state.name,st.session_state.character)},
            *st.session_state.messages
        ],
        stream=True,
    )
    #消息展示框,输入大模型返回的结果(非流式输出)
    # print("<-------这是大模型返回的信息",response.choices[0].message.content)
    # st.chat_message("assistant").write(response.choices[0].message.content)

    #消息展示框,输入大模型返回的结果(流式输出)
    response_message=st.empty()
    full_response=""
    #循环输出大模型返回的结果
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            conent=chunk.choices[0].delta.content
            full_response+=conent
            response_message.chat_message("assistant").write(full_response)

    #添加大模型返回的消息
    st.session_state.messages.append({"role": "assistant", "content": full_response})