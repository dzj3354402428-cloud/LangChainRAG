
md5_path = "./md5.text"

# Chroma
collections_name = "RAG_base_langchain"
persist_dir = "./chroma_db"

# spliter
chunk_size = 1000
chunk_overlap = 100
separators = [",","\n\n","\n","。","；","？","！",".",";","?",]
max_split_char_number = 1000    # 文本分割阈值

# retriever
return_num = 2      # 检索返回的匹配文档数量

session_id = "Dzj_001"