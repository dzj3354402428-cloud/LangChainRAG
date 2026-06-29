"""
基于streamlit完成WEB网页上传服务

当web页面元素发生变化，则代码重新执行一遍
"""
import streamlit as st
from knowledge_base import KnowledgeBaseService

# 添加网页标题
st.title("知识库更新服务")

# st.session_state（一个状态锁存器或缓存区）本质是一个字典
if "kb_service" not in st.session_state:
    st.session_state["kb_service"] = KnowledgeBaseService()

# 文件上传服务file_uploader
uploader_file = st.file_uploader(
    "请上传txt文件",
    type=["txt"],# 接收文件类型为txt
    accept_multiple_files=False,# 不接受多文件上传
)

if uploader_file is not None:
    # 提取文件信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024 # KB

    st.subheader(f"文件名{file_name}")
    st.write(f"格式:{file_type} | 大小:{file_size:.2f} KB")

    # get_value -> bytes -> decode('utf-8) 获取文件内容
    text = uploader_file.getvalue().decode("utf-8")

    # st.spinner 可以给网页加一个非常专业的“转圈圈”加载动画
    with st.spinner("正在进行 MD5校验、切分与向量入库，请稍候..."):
        try:
            # 从保险柜里拿出服务实例，并调用你的方法
            result = st.session_state["kb_service"].upload_by_str(text, file_name)
            if "已存在" in result:
                # 如果后端传回的话里包含“已存在”，说明触发了 MD5 拦截
                # 使用 st.warning 弹出一个黄色的警告框
                st.warning(result)
            else:
                # 否则说明是真的存进去了
                # 使用 st.success 弹出绿色的成功框
                st.success(f"文件 {file_name} 已成功处理并存入知识库！")
        except Exception as e:
            # 防御性编程：万一出错，捕获错误并在网页上飘红显示
            st.error(f"入库失败，遇到了点问题: {e}")