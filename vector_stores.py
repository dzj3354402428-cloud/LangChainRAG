import config_data as config
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings


class VectorStoreService:
    def __init__(self,embedding):
        """
        :param embedding: 嵌入模型传入
        """
        self.embedding = embedding

        self.vector_store = Chroma(
            collection_name=config.collections_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_dir,
        )

    def get_retriever(self):
        """返回向量检索器，方便加入链"""
        return self.vector_store.as_retriever(search_kwargs = {"k":config.return_num})

if __name__ == "__main__":
    retriever = VectorStoreService(DashScopeEmbeddings(model="text-embedding-v1")).get_retriever()
    res = retriever.invoke("我的身高是165cm，体重是60kg，请给我推荐一个尺码")
    print(res)