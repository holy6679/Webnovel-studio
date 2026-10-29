---
name: webnovel-studio
description: 通用网文全流程写作工坊（整合 Oh Story / webnovel-writer / Chinese Novelist / InkOS / AI-Novel-Writing-Assistant 机制）：扫榜选题、爆款拆文、三层问答设定、大纲规划、分章写作、去AI味、多视角审稿与 AIGC 痕迹确定性校验，交付前强制零残留门禁。用户说"写小说/写网文""扫榜选题""拆文""开新书做设定问答""写大纲""写第X章""改得不像AI写的""扫一遍AIGC痕迹""一致性检查""审稿"时使用。
---






# WebNovel Studio · 网文工坊

## 定位与核心理念

整合 Oh Story（文件系统记忆 + 确定性门禁 + 扫榜拆文去AI味）、webnovel-writer（状态库 RAG 伏笔追踪）、Chinese Novelist（三层问答悬念钩子自动校验）、InkOS（多 Agent 审计）、AI-Novel-Writing-Assistant（世界观 + RAG）的机制，固化为一个**通用网文**全流程 Skill。

核心理念三条：

1. **写作是工程**：选题 → 拆文 → 设定 → 大纲 → 写作 → 去AI味 → 审稿 → 校验，每个阶段产出可检查的文件资产，可回滚、可复盘。
2. **确定性门禁**：凡是可被程序判定的问题（字数、断章钩子、伏笔遗漏、AIGC 痕迹变体、设定冲突），必须用脚本跑出结论，不靠"感觉"。
3. **题材通用**：每次新书都通过三层问答动态确定题材、核心卖点与读者画像，不预设任何题材模板。

## 全流程总览

```
Phase 0  环境初始化      —— 建书目录、创建记忆/设定/状态三类文件
Phase 1  扫榜选题(可选)  —— 抓取番茄/七猫/起点榜单，锁定题材与差异化卖点
Phase 2  爆款拆文(可选)  —— 拆解对标书前三章与目录，提取节奏/钩子/情绪模板
Phase 3  三层问答初始化  —— 世界观/人物/冲突三层问答，确定本书档案
Phase 4  大纲规划        —— 全书大纲 + 分卷卷纲 + 前三章细纲，钩子备案
Phase 5  分章写作        —— 按细纲逐章写初稿，遵守写作守则
Phase 6  去AI味          —— 按 Humanizer-zh 规则逐段改写，消除AI腔
Phase 7  多视角审稿      —— 编辑/读者/数据三个视角审稿并重写
Phase 8  自动校验        —— 运行确定性脚本：字数/钩子/一致性/AIGC痕迹，零残留才交付
```

**门禁规则**：Phase 8 必须全部通过才能交付；任何外部交付文件（复制/上传/导出）前必须跑 AIGC 全量扫描。禁止跳过门禁直接交付。

## 目录结构规范（每本书）

Skill 工作区默认根：`skills/.../webnovel-studio/workspace/`（或按宿主环境配置）。

```
<书目录>/
├── book.md            # 书籍档案（三层问答产物）
├── outline.md         # 全书大纲 + 卷纲
├── chapters/          # 正文章节，ch_001.md 起，单章文件
├── memory/            # 文件系统记忆（Oh Story 机制）
│   ├── world.md       # 世界观：力量体系/地理/组织/规则
│   ├── characters.md  # 人物卡：动机/关系/成长线
│   └── plot_threads.md# 伏笔与悬念台账：埋设/兑现/状态
├── reviews/           # 审稿记录
└── state.json         # 写作状态库（webnovel-writer 机制）
```

`state.json` 最小结构：

```json
{
  "book": "<书名>",
  "genre": "<题材>",
  "current_chapter": 0,
  "total_chapters": 0,
  "draft_mode": true,
  "last_scan": {"date": "", "ai_trace_count": 0},
  "open_threads": []
}
```

## 目录引用

| 文件 | 用途 |
|------|------|
| `references/workflow.md` | 各阶段详细操作手册（必读） |
| `references/scan-analyze.md` | Phase 1-2 扫榜拆文方法 |
| `references/setup-planning.md` | Phase 3-4 三层问答与大纲规范 |
| `references/writing-consistency.md` | Phase 5 写作守则与一致性追踪 |
| `references/deai-scan.md` | Phase 6 去AI味规则 + AIGC 变体清单 |
| `references/review-validation.md` | Phase 7-8 审稿视角与校验标准 |
| `scripts/scan_ai_traces.py` | AIGC 痕迹全量扫描（含 docx 解包） |
| `scripts/clean_ai_traces.py` | AIGC 痕迹自动清理 + 清理后自动重扫（强制闭环） |
| `scripts/deai_rules.py` | 去AI味规则引擎（段落级命中检测） |
| `scripts/check_consistency.py` | 伏笔/设定一致性检查 |
| `scripts/wordcount_check.py` | 字数与断章钩子检查 |
| `scripts/install_skill.sh` | A/B 双版本部署脚本 |

## 能力开关

用户确认"能力全保留"，默认全部启用：

- [x] ① 扫榜拆文（可选阶段，可跳过）
- [x] ② 设定问答 + 大纲
- [x] ③ 长篇写作 + 一致性追踪
- [x] ④ 去AI味 + AIGC 全量扫描（**交付前强制**）
- [x] ⑤ 多视角审稿 + 自动校验

## 强制约束

1. **AIGC 零残留**：所有交付文件必须通过 `scan_ai_traces.py`，docx 需解包 `document.xml` 复核；任何转换/重写后必须重扫。清理场景直接跑 `clean_ai_traces.py`（自动清理 + 自动重扫强制闭环），残留 > 0 禁止交付。
2. **不承诺过稿**：去AI味与扫榜只是提高过稿概率的辅助手段，Skill 不能替代平台审核结果。
3. **确定性优先**：存在脚本可判定的检查项时，不得以主观判断代替。
4. **通用网文**：不得将任何题材设定为默认锁定，每本书必须完成三层问答。
5. **协议安全**：整合各开源 Skill 机制时仅吸收思想与流程，不复制 GPL/AGPL 源码（InkOS AGPL-3.0、webnovel-writer GPL-3.0 有传染风险，只参考机制；MIT 的 Oh Story / Chinese Novelist 可借鉴更充分）。

## 触发语（示例）

- "帮我扫一下番茄的榜单，选个题材写小说"
- "我要开一本新书，先做设定问答"
- "按大纲写第三章，注意伏笔"
- "把我这段改得不像AI写的"
- "投稿前扫一遍AIGC痕迹"
- "这本书写到第20章了，帮我做一致性检查"

## License

This Skill is licensed under the MIT License. The complete license text is included in [LICENSE](LICENSE).

SPDX-License-Identifier: MIT
