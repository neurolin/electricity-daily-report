"""
AI摘要模块
使用Kimi API对抓取的内容进行100字摘要
"""
import requests
import time
from config import KIMI_API_KEY, SUMMARY_CONFIG


class Summarizer:
    """AI摘要器"""

    def __init__(self):
        self.api_key = KIMI_API_KEY
        self.model = SUMMARY_CONFIG["model"]
        self.temperature = SUMMARY_CONFIG["temperature"]
        self.max_length = SUMMARY_CONFIG["max_length"]
        self.api_url = "https://api.moonshot.cn/v1/chat/completions"

    def _build_prompt(self, title, content, category):
        """构建摘要提示词"""
        if category == "微电网与虚拟电厂":
            domain_context = """领域背景：微电网、虚拟电厂、分布式能源、电力市场、黑启动、振荡分析
请重点关注：技术方法、控制策略、市场机制、实验验证、应用案例"""
        else:
            domain_context = """领域背景：电力系统网络安全、加密算法、攻击检测、防御机制
请重点关注：攻击类型、检测方法、防御策略、加密技术、实验验证"""

        prompt = f"""请对以下学术/行业信息进行专业摘要，要求：
1. 严格控制在{self.max_length}字左右（不超过120字）
2. 包含核心方法/技术/发现
3. 说明对领域的具体价值
4. 语言简洁专业，适合高校教师快速阅读

{domain_context}

标题：{title}

内容：{content[:3000]}

请直接输出摘要，不要包含"摘要"二字，不要分段。"""
        return prompt

    def summarize(self, title, content, category):
        """单条摘要"""
        if not self.api_key:
            print(f"  [WARN] 未配置KIMI_API_KEY，跳过摘要: {title[:30]}...")
            return "[未配置API Key，无法生成摘要]"

        try:
            prompt = self._build_prompt(title, content, category)

            resp = requests.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "你是一位电力系统领域的资深专家，擅长为高校教师提炼学术和行业信息的核心要点。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": self.temperature,
                    "max_tokens": 200
                },
                timeout=60
            )

            result = resp.json()
            if "choices" in result and len(result["choices"]) > 0:
                summary = result["choices"][0]["message"]["content"].strip()
                # 清理摘要
                summary = summary.replace("摘要：", "").replace("摘要", "")
                if len(summary) > 150:
                    summary = summary[:147] + "..."
                return summary
            else:
                error_msg = result.get("error", {}).get("message", "未知错误")
                print(f"  [WARN] API返回异常: {error_msg}")
                return f"[摘要生成失败: {error_msg}]"

        except requests.exceptions.Timeout:
            print(f"  [WARN] API请求超时: {title[:30]}...")
            return "[API请求超时]"
        except Exception as e:
            print(f"  [WARN] 摘要失败: {title[:30]}... - {e}")
            return f"[摘要生成失败: {str(e)[:50]}]"

    def batch_summarize(self, items):
        """批量摘要"""
        print("")
        print("=" * 60)
        print("开始AI摘要生成...")
        print("=" * 60)

        summarized_items = []
        for i, item in enumerate(items):
            print(f"  [{i+1}/{len(items)}] {item['title'][:50]}...")

            # 使用已有摘要或标题作为输入
            content = item.get("summary", "") or item.get("title", "")
            if not content:
                content = item["title"]

            ai_summary = self.summarize(
                item["title"],
                content,
                item["category"]
            )

            item["ai_summary"] = ai_summary
            summarized_items.append(item)

            # 控制API调用频率
            time.sleep(0.5)

        print("")
        print(f"[OK] 摘要完成: {len(summarized_items)} 条")
        return summarized_items


def batch_summarize(items):
    """对外接口：批量摘要"""
    summarizer = Summarizer()
    return summarizer.batch_summarize(items)


if __name__ == "__main__":
    # 测试
    test_items = [{
        "title": "Test article about microgrid black start",
        "summary": "This paper proposes a novel black start strategy...",
        "category": "微电网与虚拟电厂"
    }]
    result = batch_summarize(test_items)
    print(result[0]["ai_summary"])
