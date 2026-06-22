"""
电力领域情报简报 - 主程序
每日自动抓取、摘要、推送至飞书群（Webhook 方式）
支持分多条消息推送，避免超长截断
"""
import sys
import os
import json
import requests
from datetime import datetime

from fetch_sources import fetch_all_sources
from summarize import batch_summarize


# 飞书单条消息字符限制（留余量）
FEISHU_MSG_LIMIT = 3500


def _send_text_message(webhook_url, text):
    """发送单条文本消息到飞书"""
    payload = {
        "msg_type": "text",
        "content": {"text": text}
    }
    try:
        resp = requests.post(webhook_url, json=payload, timeout=30)
        result = resp.json()
        if result.get("code") == 0:
            return True
        else:
            print("[WARN] 飞书消息发送失败: " + str(result))
            return False
    except Exception as e:
        print("[WARN] 飞书消息发送异常: " + str(e))
        return False


def _build_item_text(item, index):
    """构建单条信息的文本"""
    category_icon = "[微电网]" if item["category"] == "微电网与虚拟电厂" else "[网络安全]"
    text = str(index) + ". " + category_icon + " " + item['title'][:60] + "\n"
    
    summary = item.get("ai_summary", "暂无摘要")
    if summary and summary != "[未配置API Key，无法生成摘要]":
        text += "   摘要: " + summary + "\n"
    
    text += "   链接: " + item['link'] + "\n"
    text += "   来源: " + item['source_name'] + " | " + item['source_type'] + "\n"
    
    if item.get("matched_keywords"):
        tags = " | ".join(item["matched_keywords"][:3])
        text += "   标签: " + tags + "\n"
    
    text += "\n"
    return text


def push_to_feishu_webhook(items, webhook_url):
    """通过飞书群机器人 Webhook 推送简报，支持分多条消息"""
    if not webhook_url:
        print("[WARN] 未配置 FEISHU_WEBHOOK_URL，跳过推送")
        return False

    if not items:
        return True

    today = datetime.now().strftime("%Y年%m月%d日")
    total = len(items)
    mg_count = len([i for i in items if i["category"] == "微电网与虚拟电厂"])
    sec_count = len([i for i in items if i["category"] == "电力系统网络安全"])

    # 构建消息头
    header = "电力领域情报简报 - " + today + "\n\n"
    header += "本期共收录 " + str(total) + " 条信息\n"
    header += "微电网与虚拟电厂: " + str(mg_count) + " 条\n"
    header += "电力系统网络安全: " + str(sec_count) + " 条\n"
    header += "生成时间: " + datetime.now().strftime('%H:%M') + "\n"
    header += "=" * 40 + "\n\n"

    # 先发送消息头
    if not _send_text_message(webhook_url, header):
        print("[WARN] 消息头发送失败")

    # 按分类分组推送
    categories = [
        ("微电网与虚拟电厂", [i for i in items if i["category"] == "微电网与虚拟电厂"]),
        ("电力系统网络安全", [i for i in items if i["category"] == "电力系统网络安全"]),
    ]

    msg_count = 0
    for category_name, cat_items in categories:
        if not cat_items:
            continue

        # 分类标题
        cat_header = "\n【" + category_name + "】共 " + str(len(cat_items)) + " 条\n"
        cat_header += "-" * 40 + "\n\n"

        # 分批发送该分类的信息
        current_batch = cat_header
        batch_index = 1

        for item in cat_items:
            item_text = _build_item_text(item, batch_index)
            
            # 如果当前批次加上这条会超限，先发送当前批次
            if len(current_batch) + len(item_text) > FEISHU_MSG_LIMIT:
                if _send_text_message(webhook_url, current_batch):
                    msg_count += 1
                else:
                    print("[WARN] 批次发送失败，跳过剩余内容")
                    break
                current_batch = item_text
                batch_index = 1
            else:
                current_batch += item_text
                batch_index += 1

        # 发送最后一批
        if current_batch and current_batch != cat_header:
            if _send_text_message(webhook_url, current_batch):
                msg_count += 1

    # 发送页脚
    footer = "\n" + "=" * 40 + "\n"
    footer += "本简报由AI自动生成，仅供学术参考\n"
    footer += "共发送 " + str(msg_count + 1) + " 条消息\n"
    _send_text_message(webhook_url, footer)

    print("[OK] 飞书群消息推送完成！共 " + str(total) + " 条信息，分 " + str(msg_count + 2) + " 条消息发送")
    return True


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
    print("启动时间: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 70)

    # Step 1: 抓取信息
    print("\nStep 1: 抓取信息源...")
    items = fetch_all_sources()

    if not items:
        print("\n未抓取到新信息，但仍推送状态提示")
        webhook_url = os.getenv("FEISHU_WEBHOOK_URL")
        if webhook_url:
            _send_text_message(
                webhook_url,
                "电力领域情报简报 - " + datetime.now().strftime('%Y-%m-%d') + "\n\n今日未抓取到新信息。\n\n可能原因：\n- 信源暂无更新\n- 网络连接问题\n- 关键词过滤过严\n\n请检查日志了解详情。"
            )
        return

    print("\n共抓取 " + str(len(items)) + " 条新信息")

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
    print("结束时间: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 70)


if __name__ == "__main__":
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
