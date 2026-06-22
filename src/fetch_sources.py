"""
信息抓取模块
支持RSS、网页抓取、arXiv API（使用feedparser解析）
"""
import feedparser
import requests
from bs4 import BeautifulSoup
import hashlib
import json
import time
from datetime import datetime, timedelta
from urllib.parse import urljoin

from config import ALL_SOURCES, RELEVANCE_KEYWORDS, ARXIV_API_URL


class SourceFetcher:
    """信源抓取器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        self.history = self._load_history()
    
    def _load_history(self):
        """加载已抓取记录"""
        try:
            with open("data/history.json", "r", encoding="utf-8") as f:
                return set(json.load(f))
        except:
            return set()
    
    def _save_history(self):
        """保存已抓取记录"""
        with open("data/history.json", "w", encoding="utf-8") as f:
            json.dump(list(self.history), f, ensure_ascii=False)
    
    def _generate_hash(self, url):
        """生成URL哈希用于去重"""
        return hashlib.md5(url.encode()).hexdigest()[:16]
    
    def _is_relevant(self, title, summary, category):
        """判断内容是否与目标领域相关"""
        text = (title + " " + summary).lower()
        keywords = RELEVANCE_KEYWORDS.get(category, [])
        score = 0
        matched_keywords = []
        for kw in keywords:
            if kw.lower() in text:
                score += 1
                matched_keywords.append(kw)
        # 放宽到1个关键词匹配
        core_keywords = ["microgrid", "virtual power plant", "VPP", "cybersecurity", "attack", "encryption", "power system", "grid"]
        has_core = any(kw.lower() in text for kw in core_keywords)
        return score >= 1 or has_core, matched_keywords
    
    def fetch_rss(self, source, category):
        """抓取RSS源"""
        items = []
        try:
            feed = feedparser.parse(source["url"])
            for entry in feed.entries[:15]:
                title = entry.get("title", "")
                link = entry.get("link", "")
                summary = entry.get("summary", "") or entry.get("description", "")
                published = entry.get("published", "") or entry.get("updated", "")
                
                is_rel, matched = self._is_relevant(title, summary, category)
                if not is_rel:
                    continue
                
                item_hash = self._generate_hash(link)
                if item_hash in self.history:
                    continue
                
                items.append({
                    "title": title.strip(),
                    "link": link,
                    "summary": summary[:800].strip(),
                    "published": published,
                    "source_name": source["name"],
                    "source_type": "学术期刊" if "期刊" in source.get("type", "") else "RSS",
                    "category": category,
                    "hash": item_hash,
                    "matched_keywords": matched,
                    "fetched_at": datetime.now().isoformat()
                })
                self.history.add(item_hash)
            
            print(f"  [OK] {source['name']}: 抓取 {len(items)} 条")
        except Exception as e:
            print(f"  [ERR] {source['name']}: RSS抓取失败 - {e}")
        return items
    
    def fetch_arxiv_api(self, source, category):
        """使用 arXiv API 抓取（用feedparser解析）"""
        items = []
        try:
            params = {
                "search_query": source["query"],
                "start": 0,
                "max_results": 10,
                "sortBy": "submittedDate",
                "sortOrder": "descending"
            }
            resp = requests.get(ARXIV_API_URL, params=params, timeout=30)
            
            # 使用feedparser解析arXiv Atom XML
            # 需要注册arXiv命名空间
            feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
            feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'
            
            feed = feedparser.parse(resp.content)
            
            for entry in feed.entries[:10]:
                title = entry.get("title", "")
                link = entry.get("link", "")
                summary = entry.get("summary", "")
                published = entry.get("published", "")
                
                # 清理标题中的换行
                title = title.replace("\n", " ").strip()
                
                if not title or not link:
                    continue
                
                is_rel, matched = self._is_relevant(title, summary, category)
                if not is_rel:
                    continue
                
                item_hash = self._generate_hash(link)
                if item_hash in self.history:
                    continue
                
                items.append({
                    "title": title,
                    "link": link,
                    "summary": summary[:1000].strip() if summary else "",
                    "published": published,
                    "source_name": source["name"],
                    "source_type": "预印本",
                    "category": category,
                    "hash": item_hash,
                    "matched_keywords": matched,
                    "fetched_at": datetime.now().isoformat()
                })
                self.history.add(item_hash)
            
            print(f"  [OK] {source['name']}: 抓取 {len(items)} 条")
        except Exception as e:
            print(f"  [ERR] {source['name']}: arXiv API抓取失败 - {e}")
        return items
    
    def fetch_web(self, source, category):
        """抓取网页"""
        items = []
        try:
            resp = self.session.get(source["url"], timeout=20)
            resp.encoding = "utf-8"
            soup = BeautifulSoup(resp.text, "html.parser")
            
            selector = source.get("selector", "a")
            links = soup.select(selector)
            
            for link in links[:15]:
                title = link.get_text(strip=True)
                href = link.get("href", "")
                
                if not title or len(title) < 8 or not href:
                    continue
                
                full_url = urljoin(source["url"], href)
                
                is_rel, matched = self._is_relevant(title, "", category)
                if not is_rel:
                    continue
                
                item_hash = self._generate_hash(full_url)
                if item_hash in self.history:
                    continue
                
                items.append({
                    "title": title,
                    "link": full_url,
                    "summary": "",
                    "published": datetime.now().isoformat(),
                    "source_name": source["name"],
                    "source_type": "网页",
                    "category": category,
                    "hash": item_hash,
                    "matched_keywords": matched,
                    "fetched_at": datetime.now().isoformat()
                })
                self.history.add(item_hash)
            
            print(f"  [OK] {source['name']}: 抓取 {len(items)} 条")
        except Exception as e:
            print(f"  [ERR] {source['name']}: 网页抓取失败 - {e}")
        return items
    
    def fetch_all(self):
        """抓取所有信源"""
        all_items = []
        
        for category, source_groups in ALL_SOURCES.items():
            print("")
            print("=" * 60)
            print(f"正在抓取: {category}")
            print("=" * 60)
            
            for group_name, sources in source_groups.items():
                print(f"\n  来源组: {group_name}")
                for source in sources:
                    source_type = source.get("type", "rss")
                    
                    if source_type == "arxiv_api":
                        items = self.fetch_arxiv_api(source, category)
                    elif source_type == "rss":
                        items = self.fetch_rss(source, category)
                    elif source_type == "web":
                        items = self.fetch_web(source, category)
                    else:
                        items = self.fetch_rss(source, category)
                    
                    all_items.extend(items)
                    time.sleep(1)
        
        self._save_history()
        return all_items


def fetch_all_sources():
    """对外接口：抓取所有信源"""
    fetcher = SourceFetcher()
    return fetcher.fetch_all()


if __name__ == "__main__":
    items = fetch_all_sources()
    print("")
    print("=" * 60)
    print(f"总计抓取: {len(items)} 条新信息")
    print("=" * 60)
 
