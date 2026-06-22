"""
飞书推送模块
支持推送到飞书新版云文档（wiki/ 路径）和群聊机器人
"""
import requests
import json
import time
from datetime import datetime
from config import FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_DOC_TOKEN, FEISHU_CONFIG


class FeishuPusher:
    """飞书推送器"""

    def __init__(self):
        self.app_id = FEISHU_APP_ID
        self.app_secret = FEISHU_APP_SECRET
        self.doc_token = FEISHU_DOC_TOKEN
        self.access_token = None
        self.token_expires = 0

    def _get_access_token(self):
        """获取飞书 tenant_access_token"""
        if self.access_token and time.time() < self.token_expires - 300:
            return self.access_token

        if not self.app_id or not self.app_secret:
            print("⚠️ 未配置飞书应用凭证，跳过推送")
            return None

        try:
            resp = requests.post(
                "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
                json={"app_id": self.app_id, "app_secret": self.app_secret},
                timeout=10,
            )
            result = resp.json()
            if result.get("code") == 0:
                self.access_token = result["tenant_access_token"]
                self.token_expires = time.time() + result.get("expire", 7200)
                return self.access_token
            else:
                print(f"⚠️ 获取token失败: {result}")
                return None
        except Exception as e:
            print(f"⚠️ 获取token异常: {e}")
            return None

    def _build_blocks(self, items):
        """构建飞书文档内容块"""
        today = datetime.now().strftime("%Y年%m月%d日")
        blocks = []

        # 1. 文档标题
        blocks.append({
            "block_type": 1,
            "heading": {
                "level": 1,
                "elements": [
                    {
                        "type": "textRun",
                        "textRun": {
                            "content": f"📋 电力领域情报简报 - {today}"
                        },
                    }
                ],
            },
        })

        # 2. 概述
        total = len(items)
        mg_count = len([i for i in items if i["category"] == "微电网与虚拟电厂"])
        sec_count = len([i for i in items if i["category"] == "电力系统网络安全"])

        overview = f"""本期共收录 {total} 条信息，其中：
• 微电网与虚拟电厂: {mg_count} 条
• 电力系统网络安全: {sec_count} 条

生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}
"""
        blocks.append({
            "block_type": 2,
            "text": {
                "elements": [
                    {
                        "type": "textRun",
                        "textRun": {"content": overview},
                    }
                ]
            },
        })

        # 3. 分隔线
        blocks.append({"block_type": 11, "divider": {}})

        # 4. 按分类组织内容
        for category in ["微电网与虚拟电厂", "电力系统网络安全"]:
            cat_items = [i for i in items if i["category"] == category]
            if not cat_items:
                continue

            # 分类标题
            icon = "🔹" if category == "微电网与虚拟电厂" else "🔒"
            blocks.append({
                "block_type": 1,
                "heading": {
                    "level": 2,
                    "elements": [
                        {
                            "type": "textRun",
                            "textRun": {
                                "content": f"{icon} {category} ({len(cat_items)}条)"
                            },
                        }
                    ],
                },
            })

            # 按来源类型分组
            for source_type in [
                "学术期刊",
                "预印本",
                "政策与行业",
                "市场报告与行业",
                "技术框架与标准",
                "会议与论坛",
                "行业博客与资讯",
                "YouTube/博客",
                "网页",
                "RSS",
            ]:
                type_items = [
                    i
                    for i in cat_items
                    if i["source_type"] == source_type
                    or (
                        source_type == "网页"
                        and i["source_type"] not in ["学术期刊", "预印本", "RSS"]
                    )
                ]
                if not type_items:
                    continue

                # 来源类型小标题
                blocks.append({
                    "block_type": 1,
                    "heading": {
                        "level": 3,
                        "elements": [
                            {
                                "type": "textRun",
                                "textRun": {
                                    "content": f"📑 {source_type}"
                                },
                            }
                        ],
                    },
                })

                # 每条信息
                for item in type_items[:FEISHU_CONFIG.get("max_items_per_category", 15)]:
                    # 信息标题（加粗）
                    blocks.append({
                        "block_type": 2,
                        "text": {
                            "elements": [
                                {
                                    "type": "textRun",
                                    "textRun": {
                                        "content": "📌 ",
                                        "text_style": {"bold": True},
                                    },
                                },
                                {
                                    "type": "textRun",
                                    "textRun": {
                                        "content": item["title"],
                                        "text_style": {"bold": True},
                                    },
                                },
                            ]
                        },
                    })

                    # AI摘要
                    summary_text = item.get("ai_summary", "暂无摘要")
                    blocks.append({
                        "block_type": 2,
                        "text": {
                            "elements": [
                                {
                                    "type": "textRun",
                                    "textRun": {
                                        "content": f"💡 {summary_text}"
                                    },
                                }
                            ]
                        },
                    })

                    # 链接和来源
                    link_text = f"🔗 {item['link']}
📰 {item['source_name']}"
                    blocks.append({
                        "block_type": 2,
                        "text": {
                            "elements": [
                                {
                                    "type": "textRun",
                                    "textRun": {"content": link_text},
                                }
                            ]
                        },
                    })

                    # 标签
                    if item.get("matched_keywords"):
                        tags = " | ".join(item["matched_keywords"][:5])
                        blocks.append({
                            "block_type": 2,
                            "text": {
                                "elements": [
                                    {
                                        "type": "textRun",
                                        "textRun": {
                                            "content": "🏷️ ",
                                            "text_style": {"italic": True},
                                        },
                                    },
                                    {
                                        "type": "textRun",
                                        "textRun": {
                                            "content": tags,
                                            "text_style": {"italic": True},
                                        },
                                    },
                                ]
                            },
                        })

                    # 小分隔
                    blocks.append({
                        "block_type": 11,
                        "divider": {
                            "color": {
                                "red": 200,
                                "green": 200,
                                "blue": 200,
                                "alpha": 1,
                            }
                        },
                    })

        # 5. 页脚
        blocks.append({
            "block_type": 2,
            "text": {
                "elements": [
                    {
                        "type": "textRun",
                        "textRun": {
                            "content": f"
---
📌 本简报由AI自动生成，仅供学术参考
⏰ 下次更新: {datetime.now().strftime('%Y-%m-%d')} 08:00"
                        },
                    }
                ]
            },
        })

        return blocks

    def push_to_doc(self, items):
        """推送到飞书文档"""
        doc_token = self.doc_token
        if not doc_token:
            print("⚠️ 未配置 FEISHU_DOC_TOKEN")
            return False

        token = self._get_access_token()
        if not token:
            return False

        try:
            blocks = self._build_blocks(items)

            # 获取文档root block
            resp = requests.get(
                f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks",
                headers={"Authorization": f"Bearer {token}"},
                timeout=10,
            )
            doc_info = resp.json()

            if doc_info.get("code") != 0:
                print(f"⚠️ 获取文档信息失败: {doc_info}")
                return False

            root_block = doc_info["data"]["items"][0]["block_id"]

            # 分批追加内容（每批最多50个block）
            batch_size = 50
            for i in range(0, len(blocks), batch_size):
                batch = blocks[i : i + batch_size]
                resp = requests.post(
                    f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_token}/blocks/{root_block}/children",
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json",
                    },
                    json={"children": batch},
                    timeout=30,
                )
                result = resp.json()
                if result.get("code") != 0:
                    print(f"⚠️ 追加内容失败(batch {i//batch_size+1}): {result}")
                    return False
                time.sleep(0.5)

            print(f"✓ 推送完成，共 {len(blocks)} 个内容块")

            # 获取文档URL
            doc_url = f"https://www.feishu.cn/wiki/{doc_token}"
            print(f"📄 文档链接: {doc_url}")
            return True

        except Exception as e:
            print(f"⚠️ 推送异常: {e}")
            return False

    def push_to_webhook(self, items, webhook_url):
        """通过Webhook推送到飞书群（备用方案）"""
        if not webhook_url:
            print("⚠️ 未配置Webhook，跳过群推送")
            return False

        today = datetime.now().strftime("%Y-%m-%d")
        total = len(items)

        # 构建卡片消息
        card = {
            "msg_type": "interactive",
            "card": {
                "header": {
                    "title": {
                        "tag": "plain_text",
                        "content": f"📋 电力领域情报简报 - {today}",
                    },
                    "template": "blue",
                },
                "elements": [
                    {
                        "tag": "div",
                        "text": {
                            "tag": "lark_md",
                            "content": f"**本期共收录 {total} 条信息**
• 微电网与虚拟电厂
• 电力系统网络安全",
                        },
                    },
                    {"tag": "hr"},
                ],
            },
        }

        # 添加前5条信息
        for item in items[:5]:
            card["card"]["elements"].append({
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": f"**📌 {item['title'][:50]}**
💡 {item.get('ai_summary', '暂无摘要')[:80]}...
🔗 [{item['source_name']}]({item['link']})",
                },
            })

        try:
            resp = requests.post(webhook_url, json=card, timeout=10)
            if resp.json().get("code") == 0:
                print("✓ 群消息推送成功")
                return True
            else:
                print(f"⚠️ 群推送失败: {resp.json()}")
                return False
        except Exception as e:
            print(f"⚠️ 群推送异常: {e}")
            return False


def push_to_feishu(items, webhook_url=None):
    """对外接口：推送到飞书"""
    pusher = FeishuPusher()

    # 主推送：飞书文档
    doc_result = pusher.push_to_doc(items)

    # 备用推送：群Webhook
    if webhook_url:
        pusher.push_to_webhook(items, webhook_url)

    return doc_result


if __name__ == "__main__":
    # 测试
    test_items = [
        {
            "title": "Test",
            "ai_summary": "Test summary",
            "link": "https://example.com",
            "source_name": "Test Source",
            "source_type": "学术期刊",
            "category": "微电网与虚拟电厂",
            "matched_keywords": ["微电网"],
        }
    ]
    push_to_feishu(test_items)
