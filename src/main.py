"""
电力领域情报简报 - 主程序
每日自动抓取、摘要、推送
"""
import sys
import json
from datetime import datetime

from fetch_sources import fetch_all_sources
from summarize import batch_summarize
from feishu_push import push_to_feishu


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
    print("="*70)
    print("🚀 电力领域情报简报生成器")
    print(f"⏰ 启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)

    # Step 1: 抓取信息
    print("
📡 Step 1: 抓取信息源...")
    items = fetch_all_sources()

    if not items:
        print("
⚠️ 未抓取到新信息，工作流结束")
        return

    print(f"
✅ 共抓取 {len(items)} 条新信息")

    # 保存原始数据（用于调试）
    save_items_to_file(items, "data/raw_items.json")

    # Step 2: AI摘要
    print("
📝 Step 2: AI摘要生成...")
    items = batch_summarize(items)

    # 保存摘要后数据
    save_items_to_file(items, "data/summarized_items.json")

    # Step 3: 推送到飞书
    print("
📤 Step 3: 推送到飞书...")
    webhook_url = None  # 如需群推送，可配置Webhook URL
    result = push_to_feishu(items, webhook_url)

    if result:
        print("
✅ 工作流完成！简报已推送至飞书文档")
    else:
        print("
⚠️ 飞书推送失败，但数据已保存至 data/summarized_items.json")

    print("="*70)
    print(f"🏁 结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)


if __name__ == "__main__":
    # 支持命令行参数：--skip-fetch 使用已有数据
    if "--skip-fetch" in sys.argv:
        print("📂 使用已有数据...")
        items = load_items_from_file("data/raw_items.json")
        if items:
            items = batch_summarize(items)
            push_to_feishu(items)
        else:
            print("⚠️ 未找到已有数据")
    else:
        main()

