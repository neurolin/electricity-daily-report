"""
电力领域情报简报 - 信源配置
涵盖：微电网与虚拟电厂、电力系统网络安全
"""
import os

# API Keys（通过环境变量注入）
KIMI_API_KEY = os.getenv("KIMI_API_KEY", "")
FEISHU_APP_ID = os.getenv("FEISHU_APP_ID", "")
FEISHU_APP_SECRET = os.getenv("FEISHU_APP_SECRET", "")
FEISHU_DOC_TOKEN = os.getenv("FEISHU_DOC_TOKEN", "")

# 摘要配置
SUMMARY_CONFIG = {
    "max_length": 100,  # 摘要字数
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
            "description": "IEEE智能电网顶级期刊，侧重运行控制、VPP调度、需求响应"
        },
        {
            "name": "IEEE Transactions on Power Systems",
            "type": "rss",
            "url": "https://ieeexplore.ieee.org/rss/TOC5963165.xml",
            "keywords": ["black start", "oscillation", "stability", "power system", "restoration"],
            "description": "IEEE电力系统顶级期刊，侧重稳定分析、振荡、黑启动"
        },
        {
            "name": "Applied Energy",
            "type": "rss",
            "url": "https://rss.sciencedirect.com/publication/science/03062619",
            "keywords": ["microgrid", "virtual power plant", "energy market", "optimization"],
            "description": "能源系统优化、VPP经济性、市场机制"
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
            "name": "中国电机工程学报",
            "type": "web",
            "url": "https://www.pcsee.ac.cn/",
            "selector": ".article-item a, .content-list a",
            "keywords": ["微电网", "新能源", "振荡", "稳定性", "并网"],
            "description": "中国电机工程学会主办，电力系统稳定、新能源并网"
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
            "name": "电工技术学报",
            "type": "web",
            "url": "https://www.cjee.cn/",
            "selector": ".article-item a, .paper-list a",
            "keywords": ["微电网", "逆变器", "构网型", "储能", "控制"],
            "description": "微电网逆变器控制、构网型储能"
        },
        {
            "name": "arXiv eess.SY (系统与控制)",
            "type": "rss",
            "url": "http://export.arxiv.org/rss/eess.SY",
            "keywords": ["microgrid", "VPP", "control", "optimization", "energy"],
            "description": "预印本平台系统与控制方向"
        },
    ],
    "政策与行业": [
        {
            "name": "国家发改委 - 能源政策",
            "type": "web",
            "url": "https://www.ndrc.gov.cn/xxgk/zcfb/tz/",
            "selector": "a[href*='tz/'], .list a",
            "keywords": ["虚拟电厂", "微电网", "电力", "能源", "新型电力系统"],
            "description": "中国VPP发展顶层政策发布平台"
        },
        {
            "name": "国家能源局",
            "type": "web",
            "url": "https://www.nea.gov.cn/",
            "selector": "a[href*='xxgk/'], .news-list a",
            "keywords": ["虚拟电厂", "微电网", "新能源", "电力市场"],
            "description": "国家能源政策与规划"
        },
        {
            "name": "南方电网技术",
            "type": "web",
            "url": "https://www.csg.cn/",
            "selector": ".news-list a, .article-list a",
            "keywords": ["微电网", "虚拟电厂", "智能电网", "配电网"],
            "description": "南方电网技术动态与年度报告"
        },
        {
            "name": "国家电网",
            "type": "web",
            "url": "https://www.sgcc.com.cn/",
            "selector": ".news-list a, .list a",
            "keywords": ["微电网", "配电网", "新能源", "储能"],
            "description": "国家电网技术动态"
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
            "description": "VPP市场规模与增长分析"
        },
        {
            "name": "Technavio - 微电网",
            "type": "web",
            "url": "https://www.technavio.com/report/microgrid-market-industry-analysis",
            "selector": ".report-summary, .news-item",
            "keywords": ["microgrid", "market", "growth"],
            "description": "微电网市场增长分析"
        },
        {
            "name": "经济观察网 - 能源",
            "type": "rss",
            "url": "https://www.eeo.com.cn/rss/energy.xml",
            "keywords": ["微电网", "虚拟电厂", "新能源", "储能"],
            "description": "国内能源行业财经报道"
        },
        {
            "name": "雪球 - 电力板块",
            "type": "rss",
            "url": "https://xueqiu.com/hots/topic/rss",
            "keywords": ["虚拟电厂", "东方电子", "微电网", "电力"],
            "description": "A股电力板块投资分析"
        },
    ],
    "国际会议": [
        {
            "name": "IEEE PES General Meeting",
            "type": "web",
            "url": "https://pes-gm.org/",
            "selector": ".news a, .announcement a",
            "keywords": ["smart grid", "microgrid", "cybersecurity", "VPP"],
            "description": "IEEE电力与能源学会年会"
        },
        {
            "name": "ISGT (Innovative Smart Grid Technologies)",
            "type": "web",
            "url": "https://ieee-isgt.org/",
            "selector": ".news a, .update a",
            "keywords": ["smart grid", "microgrid", "demand response"],
            "description": "IEEE智能电网创新技术会议"
        },
        {
            "name": "IPRECON 2026",
            "type": "web",
            "url": "https://iprecon.org/",
            "selector": ".news a, .announcement a",
            "keywords": ["blockchain", "cybersecurity", "VPP", "distributed energy"],
            "description": "设有VPP和网络安全专门Track"
        },
    ],
    "YouTube/博客": [
        {
            "name": "NREL (National Renewable Energy Laboratory)",
            "type": "rss",
            "url": "https://www.nrel.gov/news/program/rss/",
            "keywords": ["microgrid", "distributed energy", "grid modernization"],
            "description": "美国可再生能源实验室"
        },
        {
            "name": "PNNL (Pacific Northwest National Laboratory)",
            "type": "rss",
            "url": "https://www.pnnl.gov/news/rss",
            "keywords": ["grid resilience", "cybersecurity", "energy"],
            "description": "太平洋西北国家实验室"
        },
        {
            "name": "IEEE Power & Energy Society",
            "type": "rss",
            "url": "https://www.ieee-pes.org/rss",
            "keywords": ["power", "energy", "smart grid", "conference"],
            "description": "IEEE PES学术讲座与技术趋势"
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
            "description": "智能电网攻击检测、逆变器网络安全"
        },
        {
            "name": "IEEE Transactions on Power Electronics",
            "type": "rss",
            "url": "https://ieeexplore.ieee.org/rss/TOC63.xml",
            "keywords": ["cybersecurity", "resilience", "microgrid", "defense"],
            "description": "电力电子系统网络弹性、微电网多层防御"
        },
        {
            "name": "IEEE Transactions on Industrial Electronics",
            "type": "rss",
            "url": "https://ieeexplore.ieee.org/rss/TOC41.xml",
            "keywords": ["cybersecurity", "differential privacy", "control", "industrial"],
            "description": "工业控制系统安全、差分隐私保护"
        },
        {
            "name": "IEEE Internet of Things Journal",
            "type": "rss",
            "url": "https://ieeexplore.ieee.org/rss/TOC6488907.xml",
            "keywords": ["federated learning", "privacy", "smart grid", "IoT security"],
            "description": "联邦学习隐私保护、智能电网通信安全"
        },
        {
            "name": "电力系统保护与控制 (网络安全)",
            "type": "web",
            "url": "https://www.dlbh.net/",
            "selector": ".article-list a, .list-item a",
            "keywords": ["网络攻击", "虚假数据", "FDIA", "信息物理", "安全"],
            "description": "电力信息物理系统FDIA检测、虚假数据注入攻击"
        },
        {
            "name": "中国电机工程学报 (网络安全)",
            "type": "web",
            "url": "https://www.pcsee.ac.cn/",
            "selector": ".article-item a, .content-list a",
            "keywords": ["网络安全", "攻击", "防御", "数据驱动", "安全防御"],
            "description": "新型电力系统安全防御体系"
        },
        {
            "name": "南方电网技术 (网络安全)",
            "type": "web",
            "url": "https://www.csg.cn/",
            "selector": ".news-list a, .article-list a",
            "keywords": ["网络安全", "内部威胁", "CPS", "电力系统"],
            "description": "电力CPS内部威胁研究"
        },
        {
            "name": "arXiv cs.CR (密码与安全)",
            "type": "rss",
            "url": "http://export.arxiv.org/rss/cs.CR",
            "keywords": ["encryption", "cybersecurity", "attack", "power system", "grid"],
            "description": "密码学与网络安全预印本"
        },
        {
            "name": "IEEE Transactions on Information Forensics and Security",
            "type": "rss",
            "url": "https://ieeexplore.ieee.org/rss/TOC10206.xml",
            "keywords": ["encryption", "attack detection", "security", "forensics"],
            "description": "信息取证与安全顶级期刊"
        },
    ],
    "技术框架与标准": [
        {
            "name": "MITRE ATT&CK for ICS",
            "type": "web",
            "url": "https://attack.mitre.org/matrices/ics/",
            "selector": ".matrix-item, .technique-cell",
            "keywords": ["attack", "ICS", "industrial", "tactics", "techniques"],
            "description": "工业控制系统攻击知识库"
        },
        {
            "name": "DER Security Corp",
            "type": "web",
            "url": "https://www.dersecurity.com/",
            "selector": ".vulnerability-item, .news a",
            "keywords": ["DER", "vulnerability", "security", "distributed energy"],
            "description": "分布式能源网络安全漏洞数据库"
        },
        {
            "name": "UL Solutions - AI安全",
            "type": "web",
            "url": "https://www.ul.com/resources/ul-3115",
            "selector": ".resource-item, .news a",
            "keywords": ["AI safety", "UL 3115", "certification", "security"],
            "description": "AI赋能电力产品的安全标准"
        },
    ],
    "会议与论坛": [
        {
            "name": "IEEE Cybersecurity and AI-Based Systems",
            "type": "web",
            "url": "https://ieee-cybersecurity.org/",
            "selector": ".news a, .announcement a",
            "keywords": ["cybersecurity", "AI", "power", "energy", "attack"],
            "description": "电力、核能单元网络安全专门议题"
        },
        {
            "name": "Black Hat / DEF CON (电力相关)",
            "type": "rss",
            "url": "https://www.blackhat.com/rss",
            "keywords": ["power", "grid", "SCADA", "ICS", "attack"],
            "description": "顶级安全会议电力系统攻击研究"
        },
    ],
    "行业博客与资讯": [
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
    ]
}

# 合并所有信源
ALL_SOURCES = {
    "微电网与虚拟电厂": MICROGRID_VPP_SOURCES,
    "电力系统网络安全": CYBERSECURITY_SOURCES
}

# 关键词过滤配置（用于内容相关性评分）
RELEVANCE_KEYWORDS = {
    "微电网与虚拟电厂": [
        "微电网", "microgrid", "虚拟电厂", "virtual power plant", "VPP",
        "黑启动", "black start", "运行控制", "operation control",
        "电力市场", "electricity market", "energy market",
        "振荡分析", "oscillation analysis", "振荡抑制", "oscillation suppression",
        "分布式能源", "distributed energy", "DER",
        "需求响应", "demand response",
        "构网型", "grid-forming", "构网型储能",
        "源网荷储", "source-network-load-storage",
        "聚合", "aggregation",
        "调度", "dispatch",
        "储能", "energy storage", "battery",
        "光伏", "solar", "风电", "wind",
        "逆变器", "inverter",
        "新型电力系统", "new power system"
    ],
    "电力系统网络安全": [
        "网络安全", "cybersecurity", "cyber security",
        "加密算法", "encryption", "cryptographic", "cipher",
        "加密流量", "encrypted traffic", "TLS", "SSL",
        "攻击", "attack", "intrusion", "breach",
        "防御", "defense", "protection", "mitigation",
        "虚假数据注入", "false data injection", "FDIA",
        "重放攻击", "replay attack",
        "拒绝服务", "denial of service", "DoS", "DDoS",
        "隐蔽攻击", "stealthy attack", "covert attack",
        "零动态攻击", "zero dynamics attack",
        "共振攻击", "resonance attack",
        "检测", "detection", "identification",
        "弹性控制", "resilient control",
        "游戏理论", "game theory",
        "联邦学习", "federated learning",
        "差分隐私", "differential privacy",
        "SCADA", "ICS", "工业控制系统",
        "信息物理系统", "cyber-physical", "CPS",
        "内部威胁", "insider threat",
        "漏洞", "vulnerability",
        "威胁情报", "threat intelligence"
    ]
}

# 飞书推送配置
FEISHU_CONFIG = {
    "doc_title_template": "📋 电力领域情报简报 - {date}",
    "max_items_per_category": 15,  # 每个分类最多推送条数
    "summary_length": 100,
}

