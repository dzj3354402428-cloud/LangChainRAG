"""
知识库
"""
import os
import config_data as config
import hashlib
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime


# 依据字符串的md5值进行去重,只有新内容才会被送入文档分割器（spliter）并写入 Chroma 库。
def check_md5(md5_str:str):# 查“指纹”
    # 检查传入的md5字符串是否已经被处理过了
    if not os.path.exists(config.md5_path):
        # if进入表示文件不存在，说明没有处理过这个md5值
        open(config.md5_path,'w',encoding='utf-8').close()# 以'w'模式打开，若文件不存在会自动创建
        return False #False表示这个md5值未处理过,True表示处理过
    else:
        for line in open(config.md5_path,'r',encoding='utf-8').readlines():# readlines拿到文件全部行
            line = line.strip() # 处理字符串前后的空白字符
            if line == md5_str:
                return True # 已处理过
        return False


def save_md5(md5_str:str):
    # 将传入的md5字符串，记录到文件中保存
    with open(config.md5_path,'a',encoding='utf-8') as f: # 以追加模式打开文件
        f.write(md5_str + '\n')

def get_string_md5(input_str:str,encoding='utf-8'):# 算“指纹”
    # 将传入的字符串转换为md5字符串
    # 1. 计算机底层不认识字符串，只认识字节（0和1）。所以先把文字转化为字节流。
    str_bytes = input_str.encode(encoding=encoding)

    #创建md5对象
    # 2. 从 hashlib 库中召唤出一个专门用来算 md5 的“加工机器”
    md5_obj = hashlib.md5() # 得到md5对象

    # 3. 把刚才准备好的字节流扔进机器里
    md5_obj.update(str_bytes) # 更新内容（传入即将要转换的字节数组）

    # 4. 按下输出按钮，hexdigest() 表示输出肉眼可读的 16 进制字符串格式
    md5_hex = md5_obj.hexdigest() # 得到md5的十六进制字符串

    return md5_hex

class KnowledgeBaseService(object):
    def __init__(self):
        os.makedirs(config.persist_dir, exist_ok=True)  # 如果文件夹不存在则创建，如果文件夹已经存在则跳过
        self.chroma = Chroma(
            collection_name=config.collections_name,   # 数据库的表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v1"),
            persist_directory=config.persist_dir, # 数据库的本地存储文件夹

        ) # 向量存储的实例 Chroma向量库对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,   # 分割时每个文本段最大长度
            chunk_overlap=config.chunk_overlap, # 连续文本段之间字符串的重叠数量
            separators=config.separators,   # 自然段落划分的符号
            length_function=len,    # 使用Python自带的len函数做长度统计依据
        ) # 文本分割器的对象

    def upload_by_str(self,data:str,filename):
        # 将传入的字符串，进行向量化，存入向量数据库中
        md5_value = get_string_md5(data)# 调用get_string_md5方法计算传入的文本md5值

        if check_md5(md5_value):# 调用check_md5方法检查传入的文本是否已经存在
            print(f"文件 {filename} 已存在，停止处理！")
            return f"文件 {filename} 已存在，无需重复录入！"
        current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        doc = Document(
            page_content=data,
            metadata={
                "source": filename,
                "create_time": current_time,
                "operator":"Duzijun"
            }
        )
        if len(data) > config.max_split_char_number:
            print(f"发现新文件 {filename}，准备开始加工...")
            # langchain不认识纯文本对象，只认识document对象，因此需要将传入的文本用document包装起来
            splits = self.spliter.split_documents([doc])  # 对文本进行切片
        else:
            print(f"发现新短文件 {filename}，无需切分，直接整体入库...")
            splits = [doc]

        # 将切好的碎片存入chroma数据库
        self.chroma.add_documents(splits)
        # 记录到md5.text中
        save_md5(md5_value)
        return "[成功]内容已经成功载入向量库"

if __name__ == '__main__':
    service = KnowledgeBaseService()
    r = service.upload_by_str("杜子骏",filename="testfile")
    print(r)
