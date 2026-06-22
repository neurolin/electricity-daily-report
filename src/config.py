"""
电力领域情报简报 - 信源配置
涵盖：微电网与虚拟电厂、电力系统网络安全
优化：添加 arXiv API、稳定 RSS 源、行业博客、删除失效源
"""
import os

# API Keys（通过环境变量注入）
KIMI_API_KEY = os.getenv("KIMI_API_KEY", "")
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
FEISHU_DOC_TOKEN = os.getenv("FEISHU_DOC_TOKEN", "")

# 摘要配置
SUMMARY_CONFIG = {
    "max_length": 200,
    "model": "moonshot-v1-8k",
    "temperature": 0.3,
}

# ============================================================
# 信源配置 - 微电网与虚拟电厂
# ============================================================
MICROGRID_VPP_SOURCES = {
    "学术期刊": [
        {
            "name": "IEEE Transactions on Smart Grid",
            "type": "rss",
            "url": "https://ieeexplore.ieee.org/rss/TOC6476499.xml",
            "keywords": ["microgrid", "virtual power plant", "VPP", "demand response", "distributed energy"],
            "description": "IEEE智能电网顶级期刊"
        },
        {
            "name": "IEEE Transactions on Power Systems",
            "type": "rss",
            "url": "https://ieeexplore.ieee.org/rss/TOC5963165.xml",
            "keywords": ["black start", "oscillation", "stability", "power system", "restoration"],
            "description": "IEEE电力系统顶级期刊"
        },
        {
            "name": "Applied Energy",
            "type": "rss",
            "url": "https://rss.sciencedirect.com/publication/science/03062619",
            "keywords": ["microgrid", "virtual power plant", "energy market", "optimization"],
            "description": "能源系统优化、VPP经济性"
        },
        {
            "name": "Energy Conversion and Economics",
            "type": "rss",
            "url": "https://www.ecajournal.org/rss",
            "keywords": ["microgrid", "VPP", "energy conversion", "economic"],
            "description": "能源转换与经济分析"
        },
        {
            "name": "电力系统自动化",
            "type": "web",
            "url": "https://www.epae.cn/",
            "selector": ".article-list a, .news-list a",
            "keywords": ["微电网", "虚拟电厂", "黑启动", "源网荷储", "运行控制"],
            "description": "国内电力系统自动化顶级期刊"
        },
        {
            "name": "电力系统保护与控制",
            "type": "web",
            "url": "https://www.dlbh.net/",
            "selector": ".article-list a, .list-item a",
            "keywords": ["微电网", "黑启动", "保护", "控制", "故障"],
            "description": "微电网保护、黑启动策略"
        },
        {
            "name": "Nature Energy",
            "type": "rss",
            "url": "https://www.nature.com/nenergy.rss",
            "keywords": ["grid", "energy", "power", "renewable", "storage"],
            "description": "Nature子刊能源方向"
        },
        {
            "name": "IEEE Open Access Journal of Power and Energy",
            "type": "rss",
            "url": "https://ieeexplore.ieee.org/rss/TOC10054196.xml",
            "keywords": ["power", "energy", "grid", "microgrid", "renewable"],
            "description": "IEEE电力能源开放获取期刊"
        },
    ],
    "arXiv API": [
        {
            "name": "arXiv eess.SY - Microgrid/VPP",
            "type": "arxiv_api",
            "query": "cat:eess.SY AND (microgrid OR \"virtual power plant\" OR \"demand response\" OR \"energy storage\" OR \"distributed generation\")",
            "keywords": ["microgrid", "VPP", "control", "optimization", "energy"],
            "description": "arXiv系统与控制方向-微电网/VPP"
        },
        {
            "name": "arXiv eess.SY - Black Start",
            "type": "arxiv_api",
            "query": "cat:eess.SY AND (\"black start\" OR \"system restoration\" OR \"islanding\" OR \"grid forming\")",
            "keywords": ["black start", "restoration", "islanding", "grid-forming"],
            "description": "arXiv系统与控制方向-黑启动"
        },
        {
            "name": "arXiv eess.SY - Oscillation",
            "type": "arxiv_api",
            "query": "cat:eess.SY AND (oscillation OR \"small signal stability\" OR \"electromechanical oscillation\" OR \"damping\")",
            "keywords": ["oscillation", "stability", "damping", "electromechanical"],
            "description": "arXiv系统与控制方向-振荡分析"
        },
    ],
    "政策与行业": [
        {
            "name": "国家发改委 - 能源政策",
            "type": "web",
            "url": "https://www.ndrc.gov.cn/xxgk/zcfb/tz/",
            "selector": "a[href*='tz/'], .list a",
            "keywords": ["虚拟电厂", "微电网", "电力", "能源", "新型电力系统"],
            "description": "中国VPP发展顶层政策"
        },
        {
            "name": "国家能源局",
            "type": "web",
            "url": "https://www.nea.gov.cn/",
            "selector": "a[href*='xxgk/'], .news-list a",
            "keywords": ["虚拟电厂", "微电网", "新能源", "电力市场"],
            "description": "国家能源政策"
        },
        {
            "name": "北极星电力网",
            "type": "rss",
            "url": "https://news.bjx.com.cn/rss/",
            "keywords": ["微电网", "虚拟电厂", "电力", "新能源", "储能"],
            "description": "电力行业新闻"
        },
        {
            "name": "中国电力报",
            "type": "rss",
            "url": "http://www.cpnn.com.cn/rss/",
            "keywords": ["电力", "电网", "新能源", "储能"],
            "description": "电力行业权威媒体"
        },
    ],
    "市场报告与行业": [
        {
            "name": "SNS Insider - VPP市场",
            "type": "rss",
            "url": "https://www.snsinsider.com/feed/",
            "keywords": ["virtual power plant", "VPP", "microgrid", "energy"],
            "description": "全球VPP市场报告"
        },
        {
            "name": "Fortune Business Insights - VPP",
            "type": "rss",
            "url": "https://www.fortunebusinessinsights.com/rss",
            "keywords": ["virtual power plant", "energy", "market"],
            "description": "VPP市场规模分析"
        },
        {
            "name": "Wood Mackenzie - Power & Renewables",
            "type": "rss",
            "url": "https://www.woodmac.com/rss/power-and-renewables/",
            "keywords": ["power", "renewable", "grid", "energy storage"],
            "description": "伍德麦肯兹电力与可再生能源"
        },
        {
            "name": "经济观察网 - 能源",
            "type": "rss",
            "url": "https://www.eeo.com.cn/rss/energy.xml",
            "keywords": ["微电网", "虚拟电厂", "新能源", "储能"],
            "description": "国内能源财经报道"
        },
    ],
    "国际会议": [
        {
            "name": "IEEE PES General Meeting",
            "type": "web",
            "url": "https://pes-gm.org/",
            "selector": ".news a, .announcement a",
            "keywords": ["smart grid", "microgrid", "cybersecurity", "VPP"],
            "description": "IEEE PES年会"
        },
        {
            "name": "ISGT",
            "type": "web",
            "url": "https://ieee-isgt.org/",
            "selector": ".news a, .update a",
            "keywords": ["smart grid", "microgrid", "demand response"],
            "description": "IEEE智能电网创新技术会议"
        },
    ],
    "行业博客": [
        {
            "name": "NREL News",
            "type": "rss",
            "url": "https://www.nrel.gov/news/program/rss/",
            "keywords": ["microgrid", "distributed energy", "grid modernization"],
            "description": "美国可再生能源实验室"
        },
        {
            "name": "PNNL News",
            "type": "rss",
            "url": "https://www.pnnl.gov/news/rss",
            "keywords": ["grid resilience", "cybersecurity", "energy"],
            "description": "太平洋西北国家实验室"
        },
        {
            "name": "Energy Central - Microgrid",
            "type": "rss",
            "url": "https://www.energycentral.com/rss/section/microgrids",
            "keywords": ["microgrid", "distributed energy", "grid"],
            "description": "能源社区微电网专栏"
        },
        {
            "name": "Microgrid Knowledge",
            "type": "rss",
            "url": "https://microgridknowledge.com/feed/",
            "keywords": ["microgrid", "resilience", "distributed energy", "grid"],
            "description": "微电网专业媒体"
        },
        {
            "name": "Renewable Energy World",
            "type": "rss",
            "url": "https://www.renewableenergyworld.com/feed/",
            "keywords": ["renewable", "energy", "grid", "storage", "solar", "wind"],
            "description": "可再生能源行业权威"
        },
        {
            "name": "PV Magazine",
            "type": "rss",
            "url": "https://www.pv-magazine.com/feed/",
            "keywords": ["solar", "PV", "storage", "grid", "energy"],
            "description": "光伏与储能行业媒体"
        },
        {
            "name": "Utility Dive",
            "type": "rss",
            "url": "https://www.utilitydive.com/feeds/news/",
            "keywords": ["utility", "grid", "smart grid", "storage", "renewable"],
            "description": "电力公用事业行业新闻"
        },
        {
            "name": "Energy Storage News",
            "type": "rss",
            "url": "https://www.energy-storage.news/feed/",
            "keywords": ["energy storage", "battery", "grid", "renewable"],
            "description": "储能行业新闻"
        },
        {
            "name": "Clean Technica",
            "type": "rss",
            "url": "https://cleantechnica.com/feed/",
            "keywords": ["clean energy", "renewable", "storage", "EV", "grid"],
            "description": "清洁能源技术媒体"
        },
        {
            "name": "Solar Power World",
            "type": "rss",
            "url": "https://www.solarpowerworldonline.com/feed/",
            "keywords": ["solar", "PV", "storage", "inverter", "grid"],
            "description": "太阳能行业媒体"
        },
    ]
}
# ============================================================
# 信源配置 - 电力系统网络安全
# ============================================================
CYBERSECURITY_SOURCES = {
    "学术期刊": [
        {
            "name": "IEEE Transactions on Smart Grid (网络安全)",
            "type": "rss",
            "url": "https://ieeexplore.ieee.org/rss/TOC6476499.xml",
            "keywords": ["cybersecurity", "attack", "detection", "inverter", "false data"],
            "description": "智能电网攻击检测"
        },
        {
            "name": "IEEE Transactions on Information Forensics and Security",
            "type": "rss",
            "url": "https://ieeexplore.ieee.org/rss/TOC10206.xml",
            "keywords": ["encryption", "attack detection", "security", "forensics"],
            "description": "信息取证与安全"
        },
        {
            "name": "IEEE Internet of Things Journal",
            "type": "rss",
            "url": "https://ieeexplore.ieee.org/rss/TOC6488907.xml",
            "keywords": ["federated learning", "privacy", "smart grid", "IoT security"],
            "description": "联邦学习隐私保护"
        },
        {
            "name": "电力系统保护与控制 (网络安全)",
            "type": "web",
            "url": "https://www.dlbh.net/",
            "selector": ".article-list a, .list-item a",
            "keywords": ["网络攻击", "虚假数据", "FDIA", "信息物理", "安全"],
            "description": "电力信息物理系统FDIA检测"
        },
        {
            "name": "SecurityWeek - 能源安全",
            "type": "rss",
            "url": "https://www.securityweek.com/rss/energy",
            "keywords": ["energy", "power", "cybersecurity", "attack"],
            "description": "能源行业网络安全新闻"
        },
        {
            "name": "Computers & Security",
            "type": "rss",
            "url": "https://rss.sciencedirect.com/publication/science/01674048",
            "keywords": ["cybersecurity", "attack", "defense", "encryption", "SCADA"],
            "description": "计算机与安全期刊"
        },
    ],
    "arXiv API": [
        {
            "name": "arXiv cs.CR - Power System Security",
            "type": "arxiv_api",
            "query": "cat:cs.CR AND (power OR grid OR SCADA OR \"cyber-physical\" OR \"false data injection\" OR \"attack detection\")",
            "keywords": ["cybersecurity", "attack", "power system", "grid", "SCADA"],
            "description": "arXiv密码与安全-电力系统安全"
        },
        {
            "name": "arXiv cs.CR - Encryption",
            "type": "arxiv_api",
            "query": "cat:cs.CR AND (encryption OR \"homomorphic encryption\" OR \"lightweight cipher\" OR \"post-quantum\" OR \"TLS\" OR \"encrypted traffic\")",
            "keywords": ["encryption", "cipher", "cryptography", "TLS", "traffic"],
            "description": "arXiv密码与安全-加密算法"
        },
        {
            "name": "arXiv cs.CR - Attack & Defense",
            "type": "arxiv_api",
            "query": "cat:cs.CR AND (\"adversarial attack\" OR \"defense mechanism\" OR \"intrusion detection\" OR \"threat intelligence\" OR \"vulnerability\")",
            "keywords": ["attack", "defense", "intrusion", "threat", "vulnerability"],
            "description": "arXiv密码与安全-攻击防御"
        },
    ],
    "技术框架": [
        {
            "name": "MITRE ATT&CK for ICS",
            "type": "web",
            "url": "https://attack.mitre.org/matrices/ics/",
            "selector": ".matrix-item, .technique-cell",
            "keywords": ["attack", "ICS", "industrial", "tactics", "techniques"],
            "description": "工业控制系统攻击知识库"
        },
        {
            "name": "NIST Cybersecurity",
            "type": "rss",
            "url": "https://www.nist.gov/news-events/news/rss",
            "keywords": ["cybersecurity", "framework", "standard", "critical infrastructure"],
            "description": "NIST网络安全标准与新闻"
        },
    ],
    "行业博客": [
        {
            "name": "Dragos (工业网络安全)",
            "type": "rss",
            "url": "https://www.dragos.com/blog/rss/",
            "keywords": ["ICS", "industrial", "power", "attack", "threat"],
            "description": "工业网络安全威胁情报"
        },
        {
            "name": "SANS ICS Security Blog",
            "type": "rss",
            "url": "https://www.sans.org/blog/rss/ics/",
            "keywords": ["ICS", "SCADA", "power", "security", "defense"],
            "description": "SANS工业控制系统安全"
        },
        {
            "name": "SecurityWeek - 能源安全",
            "type": "rss",
            "url": "https://www.securityweek.com/rss/energy",
            "keywords": ["energy", "power", "cybersecurity", "attack"],
            "description": "能源行业网络安全新闻"
        },
        {
            "name": "Dark Reading - ICS/SCADA",
            "type": "rss",
            "url": "https://www.darkreading.com/rss.xml",
            "keywords": ["SCADA", "ICS", "critical infrastructure", "attack"],
            "description": "Dark Reading工业安全"
        },
        {
            "name": "Threatpost",
            "type": "rss",
            "url": "https://threatpost.com/feed/",
            "keywords": ["cybersecurity", "attack", "vulnerability", "threat", "critical infrastructure"],
            "description": "网络安全威胁情报"
        },
        {
            "name": "The Hacker News",
            "type": "rss",
            "url": "https://thehackernews.com/feeds/posts/default",
            "keywords": ["cybersecurity", "attack", "vulnerability", "malware", "hacking"],
            "description": "黑客新闻与网络安全"
        },
    ]
}

# 合并所有信源
ALL_SOURCES = {
    "微电网与虚拟电厂": MICROGRID_VPP_SOURCES,
    "电力系统网络安全": CYBERSECURITY_SOURCES
}

# 关键词过滤配置
RELEVANCE_KEYWORDS = {
    "微电网与虚拟电厂": [
        "微电网", "microgrid", "虚拟电厂", "virtual power plant", "VPP",
        "黑启动", "black start", "运行控制", "operation control",
        "电力市场", "electricity market", "energy market",
        "振荡分析", "oscillation analysis", "振荡抑制", "oscillation suppression",
        "分布式能源", "distributed energy", "DER", "distributed generation",
        "需求响应", "demand response",
        "构网型", "grid-forming", "grid forming", "构网型储能",
        "源网荷储", "source-network-load-storage",
        "聚合", "aggregation",
        "调度", "dispatch", "scheduling",
        "储能", "energy storage", "battery", "ESS",
        "光伏", "solar", "PV", "风电", "wind",
        "逆变器", "inverter",
        "新型电力系统", "new power system",
        "孤岛运行", "islanding", "islanded",
        "恢复", "restoration", "resilience",
        "电能质量", "power quality",
        "谐波", "harmonic",
    ],
    "电力系统网络安全": [
        "网络安全", "cybersecurity", "cyber security",
        "加密算法", "encryption", "cryptographic", "cipher", "cryptography",
        "加密流量", "encrypted traffic", "TLS", "SSL", "traffic analysis",
        "攻击", "attack", "intrusion", "breach", "adversarial",
        "防御", "defense", "protection", "mitigation", "countermeasure",
        "虚假数据注入", "false data injection", "FDIA", "false data",
        "重放攻击", "replay attack",
        "拒绝服务", "denial of service", "DoS", "DDoS",
        "隐蔽攻击", "stealthy attack", "covert attack",
        "零动态攻击", "zero dynamics attack",
        "共振攻击", "resonance attack",
        "检测", "detection", "identification", "anomaly detection",
        "弹性控制", "resilient control",
        "游戏理论", "game theory",
        "联邦学习", "federated learning",
        "差分隐私", "differential privacy",
        "SCADA", "ICS", "工业控制系统", "industrial control",
        "信息物理系统", "cyber-physical", "CPS",
        "内部威胁", "insider threat",
        "漏洞", "vulnerability",
        "威胁情报", "threat intelligence",
        "入侵检测", "intrusion detection",
        "恶意软件", "malware",
        "钓鱼", "phishing",
        "勒索软件", "ransomware",
        "侧信道", "side channel",
        "同态加密", "homomorphic encryption",
        "后量子密码", "post-quantum",
        "轻量级密码", "lightweight cipher",
    ]
}

# 飞书推送配置
FEISHU_CONFIG = {
    "doc_title_template": "电力领域情报简报 - {date}",
    "max_items_per_category": 15,
    "summary_length": 200,
}

# arXiv API 配置
ARXIV_API_URL = "http://export.arxiv.org/api/query"
