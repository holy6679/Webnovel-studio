#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wordcount_check.py — 字数与断章钩子检查
用法:
    python wordcount_check.py <章节文件或书目录> [--min 1500] [--max 3000]
检查:
  1. 正文字数（去除空白）是否在目标区间
  2. 章末钩子特征：末段存在悬念词/转折词/未完成动作（简化启发式）
  3. 单段超 200 字提示（去AI味规则联动）
退出码: 0=通过  1=未通过  2=参数错误
"""
import sys, re, json
from pathlib import Path

HOOK_WORDS = ["但", "却", "突然", "然而", "就在这时", "下一秒", "没想到", "竟然",
              "他/她猛地", "一个声音", "脚步声", "门被推开", "黑影", "金光", "系统提示",
              "？", "!", "……"]

def strip_ws(text: str) -> str:
    return re.sub(r"\s+", "", text)

def hook_hint(text: str) -> bool:
    tail = text[-120:]
    return any(w in tail for w in HOOK_WORDS)

def check_file(path: Path, min_w, max_w):
    text = path.read_text(encoding="utf-8", errors="ignore")
    count = len(strip_ws(text))
    issues = []
    if count < min_w:
        issues.append(f"字数不足: {count} < {min_w}")
    if count > max_w:
        issues.append(f"字数超限: {count} > {max_w}")
    if not hook_hint(text):
        issues.append("章末疑似无钩子（末段未命中钩子特征词）")
    # 单段超 200 字提示
    paras = [p for p in text.split("\n\n") if p.strip()]
    long_paras = sum(1 for p in paras if len(strip_ws(p)) > 200)
    if long_paras:
        issues.append(f"存在 {long_paras} 个超长段落(>200字)，建议拆分")
    return count, issues

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(2)
    min_w, max_w = 1500, 3000
    target = None
    i = 0
    while i < len(args):
        if args[i] == "--min" and i + 1 < len(args):
            min_w = int(args[i + 1]); i += 2
        elif args[i] == "--max" and i + 1 < len(args):
            max_w = int(args[i + 1]); i += 2
        else:
            target = args[i]; i += 1
    if not target:
        print("[ERROR] 未指定目标文件/目录")
        sys.exit(2)

    path = Path(target)
    files = [path] if path.is_file() else sorted((path / "chapters").glob("ch_*.md"))
    if not files:
        print("[ERROR] 未找到章节文件")
        sys.exit(2)

    print("=" * 50)
    print("字数与断章钩子检查报告")
    print(f"区间: {min_w}-{max_w}")
    failed = False
    for f in files:
        cnt, issues = check_file(f, min_w, max_w)
        status = "FAIL" if issues else "PASS"
        if issues:
            failed = True
        print(f"  [{status}] {f.name} 字数={cnt}" + (f"  {'; '.join(issues)}" if issues else ""))
    print("=" * 50)
    print("结论: " + ("未通过，需调整后重跑。" if failed else "全部通过。"))
    sys.exit(1 if failed else 0)

if __name__ == "__main__":
    main()
