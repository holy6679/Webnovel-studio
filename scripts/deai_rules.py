#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
deai_rules.py — 去AI味规则引擎（段落级 AI 腔命中检测）
用法:
    python deai_rules.py <文本文件> [--report <输出报告路径>]
输出: 命中行号 + 命中类别 + 建议。退出码: 0=未命中  1=有命中(需改写)  2=错误
"""
import sys, re, json
from pathlib import Path

# 规则库：类别 -> 正则特征
RULES = {
    "万能副词连发": [r"(缓缓|轻轻|静静|微微|慢慢|淡淡)地", r"地(缓缓|轻轻|静静|微微|慢慢|淡淡)"],
    "抽象概括句": [r"空气中弥漫着", r"内心五味杂陈", r"时间仿佛凝固", r"一种说不出的", r"五味杂陈"],
    "强行文艺": [r"如诗如画", r"岁月静好", r"水墨画", r"诗意(般|地|的)"],
    "排比铺陈": [r"(不是[^。]{1,20}而是[^。]{1,20}){2,}", r"既[^。，]{1,15}又[^。，]{1,15}，既[^。，]{1,15}又"],
    "生硬书面语": [r"显而易见", r"综上所述", r"值得一提的是", r"与此同时", r"不可否认"],
    "翻译腔": [r"他看起来似乎", r"这听起来像是", r"似乎……的样子", r"某种程度(上)?而言"],
    "强抒情泛滥": [r"(不禁|忍不住)心潮澎湃", r"眼眶(一热|微红|湿润)", r"热泪盈眶"],
}

def scan_file(path: Path) -> list:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    hits = []
    for lineno, line in enumerate(lines, 1):
        for cat, patterns in RULES.items():
            for p in patterns:
                m = re.findall(p, line)
                if m:
                    hits.append({"line": lineno, "category": cat, "pattern": p,
                                 "snippet": line.strip()[:80]})
    return hits

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    target = Path(sys.argv[1])
    report_path = None
    if "--report" in sys.argv:
        i = sys.argv.index("--report")
        if i + 1 < len(sys.argv):
            report_path = Path(sys.argv[i + 1])
    if not target.is_file():
        print(f"[ERROR] 文件不存在: {target}")
        sys.exit(2)

    hits = scan_file(target)
    print("=" * 50)
    print("去AI味规则引擎报告")
    print(f"文件: {target}  命中: {len(hits)}")
    if hits:
        print("-" * 50)
        for h in hits:
            print(f"  [{h['line']}行][{h['category']}] {h['snippet']}")
        print("-" * 50)
        print("建议: 按 references/deai-scan.md 的'化抽象为具象/制造个人化表达'规则改写后重跑。")
        if report_path:
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(json.dumps({"file": str(target), "hits": hits},
                                              ensure_ascii=False, indent=2), encoding="utf-8")
        sys.exit(1)
    print("结论: 无 AI 腔命中，通过。")
    sys.exit(0)

if __name__ == "__main__":
    main()
