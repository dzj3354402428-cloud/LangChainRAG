# 基于 Streamlit + LangChain RAG 的智能客服

这是一个面向服装零售场景的本地知识库问答项目。项目使用 **Streamlit** 构建交互页面，结合 **LangChain**、**Chroma** 和 **通义千问 / DashScope** 能力，实现文本知识库上传、向量化入库、语义检索、对话生成与会话记忆，适合用于学习和展示一个轻量 RAG 应用的完整闭环。

## 项目功能

当前版本提供以下能力：

- 上传 `.txt` 文件作为知识库内容
- 对文本内容进行切分、向量化并写入本地 Chroma 向量库
- 基于用户问题进行语义检索
- 使用大模型结合检索结果生成回答
- 支持基于 `session_id` 的本地多轮对话记忆
- 面向服装客服场景进行问答回复

## 技术栈

- Streamlit
- LangChain
- Chroma
- DashScope Embeddings
- Tongyi / Qwen 对话模型

## 项目结构

```text
.
├─ app_qa.py              # 客服问答页面
├─ app_file_uploader.py   # 知识库上传页面
├─ rag.py                 # RAG 主流程封装
├─ knowledge_base.py      # 文本切分、去重与向量入库
├─ vector_stores.py       # 向量检索封装
├─ file_history_store.py  # 本地会话历史存储
├─ config_data.py         # 项目配置
├─ requirements.txt       # Python 依赖
├─ chroma_db/             # 本地向量库目录（运行后生成）
├─ chat_data/             # 本地聊天记录目录（运行后生成）
└─ md5.text               # 文本去重记录文件
```

## 运行前准备

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

项目使用阿里云 DashScope 相关模型能力。运行前请先配置环境变量，例如：

```bash
set DASHSCOPE_API_KEY=your_api_key_here
```

如果你使用的是 macOS 或 Linux：

```bash
export DASHSCOPE_API_KEY=your_api_key_here
```

## 运行方式

### 1. 启动知识库上传页面

```bash
streamlit run app_file_uploader.py
```

在页面中上传 `.txt` 文件后，系统会自动：

- 读取文本内容
- 计算 MD5 做去重
- 按规则切分文本
- 写入本地 Chroma 向量库

### 2. 启动智能客服问答页面

```bash
streamlit run app_qa.py
```

进入页面后即可输入问题，系统会：

- 检索知识库相关内容
- 拼接上下文与历史消息
- 调用模型生成回答

## 使用示例

适合录入的知识内容示例：

- 商品尺码说明
- 面料说明
- 配送与退换货规则
- 活动政策
- 售后说明

示例问题：

- 我的身高 170cm，体重 65kg，应该选择什么尺码？
- 这件衣服支持七天无理由退货吗？
- 不同面料的洗护方式有什么区别？

## 当前实现说明

这个项目目前更适合作为一个**学习型 / 展示型 RAG 项目**，已经具备完整主流程，但仍有一些边界：

- 当前知识库上传仅支持 `.txt` 文件
- 向量库和聊天记录默认保存在本地目录
- 会话 ID 目前通过配置文件固定
- 暂未提供部署脚本、单元测试和生产级鉴权能力
- 暂未对 Prompt、召回效果和异常处理做系统性优化

## 适合展示的亮点

如果你把它放到 GitHub 上，这个项目比较适合展示以下能力：

- 你理解 RAG 的基础工作流
- 你能把大模型能力接入到一个可交互应用中
- 你掌握了知识库入库、向量检索、多轮对话记忆这些关键模块
- 你具备从脚本到小型应用原型的整合能力

## 后续可优化方向

如果后面你想继续打磨成更强的作品，可以考虑：

- 支持 PDF、Markdown、Word 等更多知识源
- 增加 `.env.example` 和更规范的配置管理
- 补充 `.gitignore`
- 增加页面截图或演示 GIF
- 支持动态创建会话 ID
- 增加检索结果展示，提升可解释性
- 增加 Dockerfile 或部署说明

## 说明

本项目主要用于学习和展示本地知识库问答系统的实现思路，不作为生产级客服系统直接使用。
