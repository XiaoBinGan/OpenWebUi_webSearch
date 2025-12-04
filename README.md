# 🔍 Custom Web Search Engine

[![GitHub stars](https://img.shields.io/github/stars/XiaoBinGan/OpenWebUi_webSearch?style=social)](https://github.com/XiaoBinGan/OpenWebUi_webSearch/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/XiaoBinGan/OpenWebUi_webSearch?style=social)](https://github.com/XiaoBinGan/OpenWebUi_webSearch/network/members)
[![GitHub issues](https://img.shields.io/github/issues/XiaoBinGan/OpenWebUi_webSearch)](https://github.com/XiaoBinGan/OpenWebUi_webSearch/issues)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

一个基于 DuckDuckGo 的智能搜索引擎系统，支持本地缓存、结果优化、正文抓取，可无缝接入 OpenWebUI 作为默认搜索引擎。

## ✨ 特性

- 🚀 **零成本搜索** - 基于 DuckDuckGo，无需 API Key
- 💾 **智能缓存** - 本地缓存机制，加速重复查询
- 🔄 **自动重试** - 网络异常自动重试，提高稳定性
- 📄 **正文抓取** - 自动提取网页正文内容
- 🎯 **结果优化** - 智能过滤和相关性排序
- 🔌 **OpenWebUI 集成** - 可作为 OpenWebUI 的默认搜索引擎
- 🛠️ **易于扩展** - 支持接入 LangChain、RAG、向量数据库

## 📦 安装

### 1. 克隆项目

```bash
git clone https://github.com/XiaoBinGan/OpenWebUi_webSearch.git
cd OpenWebUi_webSearch
```

### 2. 安装依赖

```bash
pip install fastapi uvicorn requests beautifulsoup4
```

## 🚀 快速开始

### 1. 启动搜索服务

```bash
uvicorn search_api:app --host 0.0.0.0 --port 7777 --reload
```

### 2. 测试 API

浏览器访问：

```
http://127.0.0.1:7777/search?q=Python教程&max_results=5
```

### 3. 独立测试搜索功能

```bash
python optimized_search.py
```

## 🔧 核心模块

### `optimized_search.py`

核心搜索引擎类，提供以下功能：

```python
from optimized_search import OptimizedWebSearcher

# 初始化搜索器
searcher = OptimizedWebSearcher(cache_enabled=True)

# 执行搜索
results = searcher.search_duckduckgo("搜索关键词", max_results=5)

# 结果包含：
# - title: 标题
# - url: 链接
# - snippet: 摘要
# - content: 正文内容（最多2000字符）
```

**主要特性：**
- ✅ 本地缓存（可配置）
- ✅ 自动重试机制
- ✅ 结果过滤（最小长度、域名黑名单）
- ✅ 相关性排序
- ✅ 网页正文抓取

### `search_api.py`

FastAPI 接口服务，提供 RESTful API：

**接口文档：**

- **GET** `/search`
  - 参数：
    - `q` (必需): 搜索关键词
    - `max_results` (可选): 返回结果数量，默认 5
  - 返回：JSON 格式的搜索结果

**示例请求：**

```bash
curl "http://127.0.0.1:7777/search?q=人工智能&max_results=3"
```

**示例响应：**

```json
{
  "query": "人工智能",
  "count": 3,
  "results": [
    {
      "title": "人工智能概述",
      "url": "https://example.com/ai",
      "snippet": "人工智能的基本介绍...",
      "content": "完整正文内容..."
    }
  ]
}
```

## 🔌 OpenWebUI 集成

### 方案 A：本机运行 OpenWebUI

1. 进入 OpenWebUI：`http://127.0.0.1:3000`
2. 进入 **Settings（设置）**
3. 找到 **Web Search / 联网搜索**
4. 填入搜索 URL：

```
http://127.0.0.1:7777/search?q={query}
```

5. 保存配置

### 方案 B：Docker 容器运行 OpenWebUI

使用以下 URL：

```
http://host.docker.internal:7777/search?q={query}
```

或者使用宿主机 IP：

```
http://192.168.1.55:7777/search?q={query}
```

**Docker 环境变量配置：**

```bash
docker run -d \
  -p 3000:8080 \
  -e WEB_SEARCH_ENGINE=custom \
  -e WEB_SEARCH_URL=http://host.docker.internal:7777/search?q={query} \
  --name open-webui \
  ghcr.io/open-webui/open-webui:main
```

## 📁 项目结构

```
.
├── optimized_search.py    # 核心搜索引擎类
├── search_api.py          # FastAPI 接口服务
├── search_cache/          # 搜索结果缓存目录（自动生成）
└── README.md              # 项目文档
```

## ⚙️ 配置选项

### 搜索器配置

```python
searcher = OptimizedWebSearcher(
    cache_enabled=True,        # 是否启用缓存
    cache_dir="search_cache"   # 缓存目录
)
```

### 结果过滤

```python
results = searcher.filter_results(
    results,
    min_length=10,                          # 最小摘要长度
    exclude_domains=["spam.com", "ads.com"] # 排除的域名
)
```

### 正文抓取

```python
content = searcher.fetch_page_content(
    url,
    max_length=2000  # 最大抓取长度
)
```

## 🧪 测试示例

在 OpenWebUI 中测试：

```
帮我搜索一下：GB28181 协议说明
```

在终端测试 API：

```bash
curl "http://127.0.0.1:7777/search?q=GB28181+协议&max_results=5"
```

## 🚀 高级功能（可选升级）

### 1️⃣ 接入 LangChain

将搜索引擎作为 AI Agent 的工具使用

### 2️⃣ 向量数据库集成

自动将搜索结果写入 Chroma 向量数据库

### 3️⃣ 企业级搜索系统

构建完整的企业内部搜索引擎系统

## 🐛 常见问题

### Q: 搜索结果为空？

A: 检查网络连接，DuckDuckGo 可能被防火墙拦截。可以尝试配置代理。

### Q: OpenWebUI 无法连接搜索服务？

A: 
- 确认搜索服务已启动：`curl http://127.0.0.1:7777/search?q=test`
- Docker 环境使用 `host.docker.internal` 而非 `127.0.0.1`
- 检查防火墙是否允许 7777 端口

### Q: 如何清理缓存？

A: 删除 `search_cache` 目录：`rm -rf search_cache`

## 📝 技术栈

- **Python 3.7+**
- **FastAPI** - 高性能 Web 框架
- **Requests** - HTTP 请求库
- **BeautifulSoup4** - HTML 解析
- **Uvicorn** - ASGI 服务器

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📮 联系方式

如有问题或建议，欢迎通过以下方式联系：

- Issue: [GitHub Issues](https://github.com/XiaoBinGan/OpenWebUi_webSearch/issues)
- Email: Solitaryhao8@gmail.com

---

⭐ 如果这个项目对你有帮助，欢迎 Star！
