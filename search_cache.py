from fastapi import FastAPI, Query
from optimized_search import OptimizedWebSearcher

app = FastAPI(title="Custom Web Search Engine")

searcher = OptimizedWebSearcher(cache_enabled=True)

@app.get("/search")
def search(
    q: str = Query(..., description="搜索关键词"),
    max_results: int = Query(5, description="返回结果数量")
):
    results = searcher.search_duckduckgo(q, max_results)

    return {
        "query": q,
        "count": len(results),
        "results": results
    }
