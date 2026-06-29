import os, json
from typing import Sequence
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
from langchain_core.chat_history import BaseChatMessageHistory


class FileChatMessageHistory(BaseChatMessageHistory):
    storage_path: str
    session_id: str

    def __init__(self, storage_path: str, session_id: str):
        self.storage_path = storage_path  # 不同会话id的存储文件，所在的文件夹路径
        self.session_id = session_id  # 会话id
        self.file_path = os.path.join(self.storage_path, self.session_id)  # 完整的文件路径

    @property   # 把一个函数伪装成了一个属性
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                messages_data = json.load(f)    # 将文本转换成列表套字典
                return messages_from_dict(messages_data)    # 将列表套字典的格式转换成langchain大模型能看懂的列表格式
        except FileNotFoundError:
            return []
        """如果系统是第一次和用户聊天，本地还没有生成文件，它不会宕机报错，而是平滑地返回一个空列表 []"""

    def add_messages(self, message: Sequence[BaseMessage]) -> None:
        all_messages = list(self.messages)  # 把历史记忆读出来放到内存里
        all_messages.extend(message)    # 把刚刚发生的新对话（message）拼接到列表尾部
        serialized = [message_to_dict(message) for message in all_messages] # 把所有对象序列化成普通的字典格式

        file_path = self.file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # 检查存放记忆的文件夹存不存在，不存在就当场建一个

        with open(file_path, "w", encoding="utf-8") as f:   # 用覆盖写入模式把最新的完整记录固化到本地 JSON 文件中。
            json.dump(serialized, f, ensure_ascii=False, indent=2)

    def clear(self) -> None:
        file_path = self.file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:  # with ... as f:当代码执行完 with 内部的代码块后，会自动帮你关闭文件。
            # 'w'是写入模式,如果文件夹不存在会自动创建;如果已经存在则会直接清空文件夹里所有的内容,准备写入新内容
            json.dump([], f)

def get_history(session_id: str):   # 暴露给外面的调用接口，只需传入session_id就可以调用FileChatMessageHistory类
    return FileChatMessageHistory(storage_path="./chat_data", session_id=session_id)

