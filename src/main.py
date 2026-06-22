"""
电力领域情报简报 - 主程序
每日自动抓取、摘要、推送至飞书群（Webhook 方式）
"""
import sys
import os
import json
import requests
from datetime import datetime

from fetch_sources import fetch_all_sources
from summarize import batch_summarize


def push_to_feishu_webhook(items, webhook_url):
    """通过飞书群机器人 Webhook 推送简报"""
    if not webhook_url:
        print("[WARN] 未配置 FEISHU_WEBHOOK_URL，跳过推送")
        return False

    today = datetime.now().strftime("%Y年%m月%d日")
    total = len(items)
    mg_count = len([i for i in items if i["category"] == "微电网与虚拟电厂"])
    sec_count = len([i for i in items if i["category"] == "电力系统网络安全"])

    # 构建文本消息内容
    content = f"电力领域情报简报 - {today}\n\n"
    content += f"本期共收录 {total} 条信息\n"
    content += f"微电网与虚拟电厂: {mg_count} 条\n"
    content += f"电力系统网络安全: {sec_count} 条\n"
    content += f"生成时间: {datetime.now().strftime('%H:%M')}\n"
    content += "=" * 40 + "\n\n"

    # 每条信息
    for i, item in enumerate(items[:20], 1):
        category_icon = "[微电网]" if item["category"] == "微电网与虚拟电厂" else "[网络安全]"
        content += f"{i}. {category_icon} {item['title'][:60]}\n"

        summary = item.get("ai_summary", "暂无摘要")
        if summary and summary != "[未配置API Key，无法生成摘要]":
            content += f"   摘要: {summary[:100]}...\n"

        content += f"   链接: {item['link']}\n"
        content += f"   来源: {item['source_name']} | {item['source_type']}\n"

        if item.get("matched_keywords"):
            tags = " | ".join(item["matched_keywords"][:3])
            content += f"   标签: {tags}\n"

        content += "\n"

    # 页脚
    content += "=" * 40 + "\n"
    content += "本简报由AI自动生成，仅供学术参考\n"

    # 构建 Webhook 请求体
    payload = {
        "msg_type": "text",
        "content": {
            "text": content
        }
    }

    try:
        resp = requests.post(webhook_url, json=payload, timeout=30)
        result = resp.json()

        if result.get("code") == 0:
            print(f"[OK] 飞书群消息推送成功！共 {len(items)} 条信息")
            return True
        else:
            print(f"[WARN] 飞书推送失败: {result}")
            return False

    except Exception as e:
        print(f"[WARN] 飞书推送异常: {e}")
        return False


def load_items_from_file(filepath):
    """从文件加载已抓取的信息（用于调试）"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_items_to_file(items, filepath):
    """保存信息到文件"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def main():
    """主工作流"""
    print("=" * 70)
    print("电力领域情报简报生成器")
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    # Step 1: 抓取信息
    print("\nStep 1: 抓取信息源...")
    items = fetch_all_sources()

    if not items:
        print("\n未抓取到新信息，工作流结束")
        return

    print(f"\n共抓取 {len(items)} 条新信息")

    # 保存原始数据
    save_items_to_file(items, "data/raw_items.json")

    # Step 2: AI摘要
    print("\nStep 2: AI摘要生成...")
    items = batch_summarize(items)

    # 保存摘要后数据
    save_items_to_file(items, "data/summarized_items.json")

    # Step 3: 推送到飞书群（Webhook）
    print("\nStep 3: 推送到飞书群...")
    webhook_url = os.getenv("FEISHU_WEBHOOK_URL")

    if webhook_url:
        result = push_to_feishu_webhook(items, webhook_url)
        if result:
            print("\n[OK] 工作流完成！简报已推送至飞书群")
        else:
            print("\n[WARN] 飞书推送失败，但数据已保存至 data/summarized_items.json")
    else:
        print("\n[WARN] 未配置 FEISHU_WEBHOOK_URL，跳过推送")
        print("   数据已保存至 data/summarized_items.json")

    print("=" * 70)
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)


if __name__ == "__main__":
    # 支持命令行参数
    if "--skip-fetch" in sys.argv:
        print("使用已有数据...")
        items = load_items_from_file("data/raw_items.json")
        if items:
            items = batch_summarize(items)
            webhook_url = os.getenv("FEISHU_WEBHOOK_URL")
            if webhook_url:
                push_to_feishu_webhook(items, webhook_url)
        else:
            print("未找到已有数据")
    else:
        main()
