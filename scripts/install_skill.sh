#!/usr/bin/env bash
# install_skill.sh — WebNovel Studio 双版本部署脚本（A + B）
# 用法:
#   A 版本（编码 Agent，如 Claude Code / Codex）:
#     npx skills add webnovel-studio   # 或放到 skills 目录后: bash install_skill.sh --agent
#   B 版本（本机 Marvis 目录）:
#     bash install_skill.sh --marvis <目标目录>
# 说明: A/B 双版本共用同一份 SKILL.md 与 references/scripts，只是安装位置不同。
set -euo pipefail

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="1.0.0"

echo "=============================================="
echo " WebNovel Studio 部署脚本 v${VERSION}"
echo " 源目录: ${SOURCE_DIR}"
echo "=============================================="

case "${1:-}" in
  --agent)
    # A 版本: 编码 Agent 环境（假设已通过 npx skills add 或本仓库即 skill 目录）
    echo "[A] 编码 Agent 版本：确认 SKILL.md 存在..."
    test -f "${SOURCE_DIR}/SKILL.md" && echo "[A] SKILL.md OK"
    test -d "${SOURCE_DIR}/references" && echo "[A] references OK"
    test -d "${SOURCE_DIR}/scripts" && echo "[A] scripts OK"
    echo "[A] 完成。在 Agent 配置中注册 skills/webnovel-studio 即可触发。"
    ;;
  --marvis)
    # B 版本: 本机 Marvis 目录（复制到用户 skill 目录）
    TARGET="${2:?用法: install_skill.sh --marvis <目标目录>}"
    mkdir -p "${TARGET}"
    cp -r "${SOURCE_DIR}/SKILL.md" "${SOURCE_DIR}/references" "${SOURCE_DIR}/scripts" "${TARGET}/"
    echo "[B] Marvis 版本已部署到: ${TARGET}"
    echo "[B] 完成。请重启/刷新 Marvis 使技能生效。"
    ;;
  --test)
    # 冒烟测试: 跑一遍脚本自检
    echo "[TEST] 运行脚本冒烟测试..."
    TMPD="$(mktemp -d)"
    printf '这是一段干净的测试文字。\n' > "${TMPD}/clean.txt"
    printf '本文内容由AI生成，仅供参考。\n' > "${TMPD}/dirty.txt"
    python3 "${SOURCE_DIR}/scripts/scan_ai_traces.py" "${TMPD}/clean.txt" && echo "  clean.txt 通过(预期0残留)"
    python3 "${SOURCE_DIR}/scripts/scan_ai_traces.py" "${TMPD}/dirty.txt" && { echo "  dirty.txt 应报残留!"; exit 1; } || echo "  dirty.txt 正确拦截"
    python3 "${SOURCE_DIR}/scripts/deai_rules.py" "${TMPD}/clean.txt" && echo "  deai_rules 通过"
    # 清理-重扫强制闭环（wms-009 对应）
    python3 "${SOURCE_DIR}/scripts/clean_ai_traces.py" "${TMPD}/dirty.txt" && echo "  clean_ai_traces 清理+重扫闭环通过" || { echo "  清理闭环失败!"; exit 1; }
    rm -rf "${TMPD}"
    echo "[TEST] 冒烟测试全部通过。"
    ;;
  *)
    echo "用法: $0 {--agent | --marvis <目标目录> | --test}"
    exit 1
    ;;
esac
