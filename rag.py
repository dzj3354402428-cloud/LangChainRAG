from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from vector_stores import VectorStoreService
from langchain_core.runnables.history import RunnableWithMessageHistory
from file_history_store import get_history

class RagService:
    def __init__(self):
        self.chat_model = ChatTongyi(model="qwen-max")
        self.retriever = VectorStoreService(DashScopeEmbeddings(model="text-embedding-v1")).get_retriever()
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system","你是一家服装店的客服，请严格根据以下<参考资料>回答用户问题.资料中没有的请回答'请咨询人工客服'"
                "简洁和专业的回答用户的问题，参考资料{context}"),
                ("system","我提供你与用户对话的历史记录如下："),
                MessagesPlaceholder("history"), # 为历史记录的插入留下的插槽
                ("user","{question}")
            ]
        )

    def format_docs(self,docs):
        for i, doc in enumerate(docs):
            print(f"\n检索片段 {i + 1}：")
            print(doc.page_content)
        return "\n\n".join(doc.page_content for doc in docs)
    # 将检索器检索到的Document对象用join操作拼成一大段话并打印到终端中

    def _get_chain(self):   # 前面加下划线表示这是内部调用的私有方法
        # 1.专门负责检索知识的支路
        retrieve_chain = RunnableLambda(lambda x: x["question"]) | self.retriever | self.format_docs
        # RunnableLambda 的作用是从输入字典 {"question": "..."} 中精准提取出字符串，送给 retriever

        # 2.主路，核心流水线
        chain = (
                # RunnablePassthrough.assign 是一个“并联器”
                # 它保留原有的 {"question": "..."} 不变，同时把上面子电路跑出来的结果，挂载到 context 字段上
                # 此时信号变成了：{"question": "...", "context": "检索到的超长文本"}
                RunnablePassthrough.assign(context=retrieve_chain)  # 保留原始字典，追加context字段
                | self.prompt   # 把字典里的数据填入prompt模板
                | self.chat_model   # 发给大模型推理
                | StrOutputParser() # 转换成纯净文本格式输出
        )

        # 外挂的存储控制器
        chain_with_history = RunnableWithMessageHistory(
            chain,
            get_history,    # 调用记忆接口
            input_messages_key = "question",
            history_messages_key = "history"
        )
        return chain_with_history

    def invoke(self,question:str,session_id:str):   # 系统对外的标准接口，前端只需调用invoke，塞进去question和session_id就能得到一个回答
        res = self._get_chain().invoke(
            {"question": question},
            config={"configurable":{"session_id":session_id}}
        )
        return res

if __name__ == "__main__":
    session_id = "Dzj01"
    rag = RagService()
    test_question = "我的身高170cm，体重65kg，应该选择什么尺码？"
    res = rag.invoke(test_question,session_id)
    print(res)
