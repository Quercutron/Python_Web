ai_partner_3是基于streamlit框架，实现基于web页面与大模型进行交互（deepseek官方提供的的api接口）。

实现功能：会话记忆，新建会话，加载历史会话，删除历史会话，自定义大模型名称和性格（系统提示词）。

技术栈：streamlit+json+os+datatime+openai+pyexpat

汉字迷盒是基于fastAPI框架，通过REST风格的API接口服务，实现web页面与大模型进行交互。

实现功能：挂在静态目录，读写json格式文件，展示会话信息，加载历史会话，删除指定会话，exception_handler捕获异常，BaseModel数据校验，loggin打印日志

技术栈：fastapi+starlette+fastapi+pydantic+logging+uvicorn
