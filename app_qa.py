from rag import RagService
import streamlit as st
import config_data as config

st.title("智能客服")
st.divider()        # 分隔符

if "message" not in st.session_state:
    st.session_state["message"] = [{"role":"assistant","content":"你好，有什么可以帮助你？"}]
# 如果缓存区里没有聊天记录，就造一个列表，并塞入机器人的第一句开场白

if "rag" not in st.session_state:
    st.session_state["rag"] = RagService()
# 确保只在用户第一次打开网页时实例化 RagService,后续刷新页面不用重新实例化，避免网页卡死


for message in st.session_state["message"]:
    st.chat_message(message["role"]).write(message["content"])

# 在页面下方提供用户输入栏
prompt = st.chat_input()

if prompt:

    # 在页面输出用户提问
    st.chat_message("user").write(prompt)
    st.session_state["message"].append({"role":"user","content":prompt})

    with st.spinner("正在思考中..."):
        res = st.session_state["rag"].invoke(question=prompt,session_id=config.session_id)
        st.chat_message("assistant").write(res)
        st.session_state["message"].append({"role": "assistant", "content": res})