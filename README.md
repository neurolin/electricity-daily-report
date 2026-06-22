⚡ 电力领域情报简报
自动抓取微电网/虚拟电厂、电力系统网络安全领域的高价值信源，使用AI生成100字摘要，推送至飞书文档。
📁 项目结构
```
power-brief/
├── .github/
│   └── workflows/
│       └── daily-brief.yml      # GitHub Actions 定时工作流
├── src/
│   ├── config.py                # 信源配置（40+信源）
│   ├── fetch_sources.py         # 信息抓取模块
│   ├── summarize.py             # AI摘要模块（Kimi API）
│   ├── feishu_push.py           # 飞书推送模块
│   └── main.py                  # 主程序
├── data/
│   ├── .gitkeep
│   ├── history.json             # 去重历史记录
│   ├── raw_items.json           # 原始抓取数据
│   └── summarized_items.json    # 摘要后数据
├── requirements.txt
└── README.md
```
🔧 配置步骤
1. Fork/Clone 仓库
```bash
git clone https://github.com/YOUR_USERNAME/power-brief.git
cd power-brief
```
2. 配置 GitHub Secrets
在仓库 Settings → Secrets and variables → Actions 中添加：
Secret Name	说明	获取方式
`KIMI_API_KEY`	Kimi AI API密钥	Moonshot AI
`FEISHU_APP_ID`	飞书应用ID	飞书开放平台
`FEISHU_APP_SECRET`	飞书应用Secret	同上
`FEISHU_DOC_TOKEN`	飞书文档Token	创建文档后从URL获取
3. 飞书应用配置
访问 飞书开放平台
创建「企业自建应用」
开启权限：
`docx:document:write`（文档写入）
`docx:document:read`（文档读取）
`im:message:send`（消息发送，可选）
发布应用并获取 `App ID` 和 `App Secret`
创建飞书文档，从URL中获取 `doc_token`（如 `doxcnxxxxxxxx`）
4. 本地测试
```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量（临时）
export KIMI_API_KEY="your_key"
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_secret"
export FEISHU_DOC_TOKEN="your_doc_token"

# 运行
python src/main.py
```
📡 信源列表
微电网与虚拟电厂（20+信源）
类型	数量	代表信源
学术期刊	8	IEEE TSG, IEEE TPS, Applied Energy, 电力系统自动化, 中国电机工程学报
政策与行业	4	国家发改委, 国家能源局, 南方电网, 国家电网
市场报告	4	SNS Insider, Fortune BI, Technavio, 经济观察网
国际会议	3	IEEE PESGM, ISGT, IPRECON 2026
YouTube/博客	3	NREL, PNNL, IEEE PES
电力系统网络安全（15+信源）
类型	数量	代表信源
学术期刊	8	IEEE TSG, IEEE TPEL, IEEE TIE, IEEE IoT-J, 电力系统保护与控制
技术框架	3	MITRE ATT&CK, DER Security, UL 3115
安全会议	2	IEEE Cybersecurity, Black Hat
行业博客	3	Dragos, SANS ICS, SecurityWeek
⏰ 运行计划
定时运行: 每天北京时间 8:00
手动触发: 支持 GitHub Actions 手动运行
调试模式: 支持 `--skip-fetch` 使用已有数据
💰 成本估算
项目	日成本	月成本
GitHub Actions	免费	免费
Kimi API (20条/天)	~¥0.06	~¥1.8
飞书	免费	免费
合计	~¥0.06	~¥1.8
📝 输出格式
飞书文档包含：
📋 标题与概述（信息统计）
🔹 微电网与虚拟电厂（按来源分类）
🔒 电力系统网络安全（按来源分类）
每条信息：📌标题 + 💡AI摘要 + 🔗链接 + 🏷️关键词标签
🔧 自定义配置
编辑 `src/config.py` 可：
添加/删除信源
修改关键词过滤规则
调整摘要长度
配置推送参数
📄 License
MIT
