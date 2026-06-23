"""
AI摘要模块
使用Kimi API对抓取的内容进行200字摘要
添加重试机制和指数退避，避免API过载
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
        self.max_retries = 3  # 最大重试次数
        self.base_delay = 2   # 基础间隔2秒
    
    def _build_prompt(self, title, content, category):
        """构建摘要提示词"""
        if category == "微电网与虚拟电厂":
            domain_context = """领域背景：微电网、虚拟电厂、分布式能源、电力市场、黑启动、振荡分析
请重点关注：技术方法、控制策略、市场机制、实验验证、应用案例"""
        else:
            domain_context = """领域背景：电力系统网络安全、加密算法、攻击检测、防御机制
请重点关注：攻击类型、检测方法、防御策略、加密技术、实验验证"""
        
        prompt = """请对以下学术/行业信息进行专业摘要，要求：
1. 字数在200字左右（充分展开，不要过度精简）
2. 必须包含：核心方法/技术、主要发现/结论、对领域的价值
3. 如果内容涉及实验，需说明实验设置和结果
4. 语言简洁专业，适合高校教师快速阅读

""" + domain_context + """

标题：""" + title + """

内容：""" + content[:4000] + """

请直接输出摘要，不要包含"摘要"二字，不要分段。"""
        return prompt
    
    def summarize(self, title, content, category):
        """单条摘要，带重试机制"""
        if not self.api_key:
            print("  [WARN] 未配置KIMI_API_KEY，使用原文摘要")
            return self._fallback_summary(content, title)
        
        prompt = self._build_prompt(title, content, category)
        
        # 重试循环
        for attempt in range(self.max_retries):
            try:
                resp = requests.post(
                    self.api_url,
                    headers={
                        "Authorization": "Bearer " + self.api_key,
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "system", "content": "你是一位电力系统领域的资深专家，擅长为高校教师提炼学术和行业信息的核心要点。摘要要充分完整，不要过度精简。"},
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": self.temperature,
                        "max_tokens": 350
                    },
                    timeout=60
                )
                
                result = resp.json()
                
                # 检查是否过载
                if result.get("error", {}).get("message", "").find("overloaded") != -1:
                    print("  [WARN] API过载，等待后重试 (" + str(attempt + 1) + "/" + str(self.max_retries) + ")")
                    time.sleep(self.base_delay * (attempt + 1))  # 指数退避：2s, 4s, 6s
                    continue
                
                # 检查其他错误
                if "error" in result:
                    error_msg = result.get("error", {}).get("message", "未知错误")
                    print("  [WARN] API错误: " + error_msg + "，重试 (" + str(attempt + 1) + "/" + str(self.max_retries) + ")")
                    time.sleep(self.base_delay * (attempt + 1))
                    continue
                
                # 成功
                if "choices" in result and len(result["choices"]) > 0:
                    summary = result["choices"][0]["message"]["content"].strip()
                    summary = summary.replace("摘要：", "").replace("摘要", "")
                    return summary
                
            except requests.exceptions.Timeout:
                print("  [WARN] API请求超时，重试 (" + str(attempt + 1) + "/" + str(self.max_retries) + ")")
                time.sleep(self.base_delay * (attempt + 1))
                continue
            except Exception as e:
                print("  [WARN] 请求异常: " + str(e) + "，重试 (" + str(attempt + 1) + "/" + str(self.max_retries) + ")")
                time.sleep(self.base_delay * (attempt + 1))
                continue
        
        # 所有重试都失败，使用原文摘要
        print("  [WARN] 所有重试失败，使用原文摘要")
        return self._fallback_summary(content, title)
    
    def _fallback_summary(self, content, title):
        """API失败时的备用摘要：提取原文前200字"""
        text = content if content else title
        text = text.strip()
        
        if len(text) > 200:
            # 提取前200字，尽量在句号处截断
            truncated = text[:200]
            last_period = truncated.rfind("。")
            last_space = truncated.rfind(" ")
            cut_point = max(last_period, last_space)
            if cut_point > 150:
                truncated = truncated[:cut_point + 1]
            return truncated + " [原文摘要，API暂时不可用]"
        else:
            return text + " [原文摘要，API暂时不可用]"
    
    def batch_summarize(self, items):
        """批量摘要"""
        print("")
        print("=" * 60)
        print("开始AI摘要生成...")
        print("=" * 60)
        
        summarized_items = []
        for i, item in enumerate(items):
            print("  [" + str(i+1) + "/" + str(len(items)) + "] " + item['title'][:50] + "...")
            
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
            
            # 增加间隔，避免API过载
            if i < len(items) - 1:
                time.sleep(self.base_delay)
        
        print("")
        print("[OK] 摘要完成: " + str(len(summarized_items)) + " 条")
        return summarized_items


def batch_summarize(items):
    """对外接口：批量摘要"""
    summarizer = Summarizer()
    return summarizer.batch_summarize(items)


if __name__ == "__main__":
    test_items = [{
        "title": "Test article about microgrid black start",
        "summary": "This paper proposes a novel black start strategy...",
        "category": "微电网与虚拟电厂"
    }]
    result = batch_summarize(test_items)
    print(result[0]["ai_summary"])
