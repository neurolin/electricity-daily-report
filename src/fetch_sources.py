"""
信息抓取模块
支持RSS、网页抓取、arXiv API
"""
import feedparser
import requests
from bs4 import BeautifulSoup
import hashlib
import json
import time
from datetime import datetime, timedelta
from urllib.parse import urljoin
import re

from config import ALL_SOURCES, RELEVANCE_KEYWORDS


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
        # 至少匹配2个关键词或包含核心关键词
        core_keywords = ["微电网", "microgrid", "虚拟电厂", "VPP", "virtual power plant",
                        "网络安全", "cybersecurity", "加密", "encryption", "攻击", "attack"]
        has_core = any(kw.lower() in text for kw in core_keywords)
        return score >= 2 or has_core, matched_keywords

    def fetch_rss(self, source, category):
        """抓取RSS源"""
        items = []
        try:
            feed = feedparser.parse(source["url"])
            for entry in feed.entries[:15]:  # 最近15条
                title = entry.get("title", "")
                link = entry.get("link", "")
                summary = entry.get("summary", "") or entry.get("description", "")
                published = entry.get("published", "") or entry.get("updated", "")

                # 检查相关性
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

            print(f"  ✓ {source['name']}: 抓取 {len(items)} 条")
        except Exception as e:
            print(f"  ✗ {source['name']}: RSS抓取失败 - {e}")
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

                # 补全URL
                full_url = urljoin(source["url"], href)

                # 检查相关性
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

            print(f"  ✓ {source['name']}: 抓取 {len(items)} 条")
        except Exception as e:
            print(f"  ✗ {source['name']}: 网页抓取失败 - {e}")
        return items

    def fetch_arxiv(self, source, category):
        """抓取arXiv（特殊处理）"""
        items = []
        try:
            feed = feedparser.parse(source["url"])
            for entry in feed.entries[:10]:
                title = entry.get("title", "")
                link = entry.get("link", "")
                summary = entry.get("summary", "")
                published = entry.get("published", "")

                is_rel, matched = self._is_relevant(title, summary, category)
                if not is_rel:
                    continue

                item_hash = self._generate_hash(link)
                if item_hash in self.history:
                    continue

                items.append({
                    "title": title.strip(),
                    "link": link,
                    "summary": summary[:1000].strip(),
                    "published": published,
                    "source_name": source["name"],
                    "source_type": "预印本",
                    "category": category,
                    "hash": item_hash,
                    "matched_keywords": matched,
                    "fetched_at": datetime.now().isoformat()
                })
                self.history.add(item_hash)

            print(f"  ✓ {source['name']}: 抓取 {len(items)} 条")
        except Exception as e:
            print(f"  ✗ {source['name']}: arXiv抓取失败 - {e}")
        return items

    def fetch_all(self):
        """抓取所有信源"""
        all_items = []

        for category, source_groups in ALL_SOURCES.items():
            print(f"
{'='*60}")
            print(f"📂 正在抓取: {category}")
            print(f"{'='*60}")

            for group_name, sources in source_groups.items():
                print(f"
  📑 {group_name}")
                for source in sources:
                    source_type = source.get("type", "rss")

                    if source_type == "rss" or "arxiv" in source["url"].lower():
                        items = self.fetch_rss(source, category)
                    elif source_type == "web":
                        items = self.fetch_web(source, category)
                    else:
                        items = self.fetch_rss(source, category)

                    all_items.extend(items)
                    time.sleep(1)  # 礼貌延迟

        self._save_history()
        return all_items


def fetch_all_sources():
    """对外接口：抓取所有信源"""
    fetcher = SourceFetcher()
    return fetcher.fetch_all()


if __name__ == "__main__":
    items = fetch_all_sources()
    print(f"
{'='*60}")
    print(f"总计抓取: {len(items)} 条新信息")
    print(f"{'='*60}")

