import requests
from bs4 import BeautifulSoup
import time
import hashlib
import pickle
import os
from functools import wraps
from urllib.parse import urlparse

class OptimizedWebSearcher:
    """
    ✅ DuckDuckGo 搜索
    ✅ 本地缓存
    ✅ 自动重试
    ✅ 结果过滤 + 排序
    ✅ 网页正文抓取（可用于RAG / 大模型）
    """

    def __init__(self, cache_enabled=True, cache_dir="search_cache"):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })

        self.cache_enabled = cache_enabled
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    # ========== 通用重试装饰器 ==========
    def retry(self, max_attempts=3, delay=1):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                for attempt in range(max_attempts):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        if attempt == max_attempts - 1:
                            raise e
                        time.sleep(delay)
                return None
            return wrapper
        return decorator

    # ========== 缓存 ==========
    def get_cache_key(self, query, max_results):
        key = f"{query}_{max_results}"
        return hashlib.md5(key.encode()).hexdigest()

    def get_cache(self, query, max_results):
        if not self.cache_enabled:
            return None

        cache_file = os.path.join(self.cache_dir, self.get_cache_key(query, max_results))

        if os.path.exists(cache_file):
            with open(cache_file, "rb") as f:
                return pickle.load(f)

        return None

    def set_cache(self, query, max_results, data):
        if not self.cache_enabled:
            return

        cache_file = os.path.join(self.cache_dir, self.get_cache_key(query, max_results))

        with open(cache_file, "wb") as f:
            pickle.dump(data, f)

    # ========== 网页正文抓取 ==========
    def fetch_page_content(self, url, max_length=2000):
        try:
            res = self.session.get(url, timeout=10)
            soup = BeautifulSoup(res.text, "html.parser")

            for s in soup(["script", "style", "noscript"]):
                s.decompose()

            text = " ".join(soup.stripped_strings)
            return text[:max_length]

        except Exception:
            return ""

    # ========== 结果过滤 ==========
    def filter_results(self, results, min_length=10, exclude_domains=None):
        if exclude_domains is None:
            exclude_domains = []

        filtered = []

        for result in results:
            if len(result.get("snippet", "")) < min_length:
                continue

            url = result.get("url", "")
            domain = urlparse(url).netloc

            if any(ex in domain for ex in exclude_domains):
                continue

            filtered.append(result)

        return filtered

    # ========== 结果排序 ==========
    def rank_results(self, results, query):

        query_words = set(query.lower().split())

        def relevance_score(result):
            title = result.get("title", "").lower()
            snippet = result.get("snippet", "").lower()
            content = result.get("content", "").lower()

            score = 0
            for word in query_words:
                score += title.count(word) * 2
                score += snippet.count(word) * 1
                score += content.count(word) * 0.5

            return score

        return sorted(results, key=relevance_score, reverse=True)

    # ========== DuckDuckGo 搜索 ==========
    def search_duckduckgo(self, query, max_results=5):
        cached = self.get_cache(query, max_results)
        if cached:
            return cached

        url = "https://html.duckduckgo.com/html/"
        params = {"q": query, "ia": "web"}

        response = self.session.post(url, data=params, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []

        for item in soup.find_all("div", class_="result"):
            title_elem = item.find("a", class_="result__a")
            url_elem = item.find("a", class_="result__url")
            snippet_elem = item.find("a", class_="result__snippet")

            if title_elem and url_elem:

                link = url_elem.get("href")

                result = {
                    "title": title_elem.get_text(strip=True),
                    "url": link,
                    "snippet": snippet_elem.get_text(strip=True) if snippet_elem else "",
                    "content": self.fetch_page_content(link)
                }

                results.append(result)

                if len(results) >= max_results:
                    break

        # 过滤 + 排序
        results = self.filter_results(results)
        results = self.rank_results(results, query)

        self.set_cache(query, max_results, results)

        return results


# ========== 单独测试 ==========
if __name__ == "__main__":
    searcher = OptimizedWebSearcher(cache_enabled=True)
    r = searcher.search_duckduckgo("GB28181 协议说明", 5)

    for i in r:
        print("\n标题:", i["title"])
        print("链接:", i["url"])
        print("摘要:", i["snippet"])
        print("正文:", i["content"][:300])
        print("-" * 60)
