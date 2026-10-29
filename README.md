WebNovel Studio · 网文工坊  一个面向网文作者的通用网文全流程写作 AI 技能（Skill）：从"不知道写什么"到"投稿零 AIGC 残留"，覆盖扫榜选题、爆款拆文、三层问答设定、大纲规划、分章写作、去AI味、多视角审稿与 AIGC 痕迹确定性校验，交付前强制零残留门禁。  核心思路：写作是工程。每个阶段产出可检查、可回滚、可复盘的文件资产；凡是能程序判定的问题（字数、断章钩子、伏笔遗漏、设定冲突、AIGC 痕迹变体），一律用脚本跑出结论，不靠"感觉"。   核心功能  功能   说明    扫榜选题   抓取番茄小说 / 七猫免费小说 / 起点中文网榜单，统计题材分布，识别红海题材与蓝海缺口，辅助确定题材与差异化卖点    爆款拆文   拆解对标书"黄金三章"与目录，提取开篇三要素、章节节奏表、钩子类型清单、爽点结构，产出可复用的节奏模板    三层问答设定   世界观 / 人物 / 冲突三层问答（每层 5-10 问），动态确定题材、核心卖点与读者画像，固化为书籍档案 book.md    大纲规划   全书大纲 + 分卷卷纲 + 前三章细纲；伏笔与悬念台账（plot_threads.md）逐条备案，章末钩子强制登记    分章写作   单章 1500-3000 字写作守则，章末钩子纪律，state.json 状态库 + RAG 式记忆检索，伏笔推进与兑现全程追踪    去AI味   Humanizer-zh 风格规则逐段改写：消除 AI 腔高频词、化抽象为具象、制造个人化表达、重构节奏分段，支持 L1 轻量 / L2 标准 / L3 深度三档    AIGC 痕迹确定性校验   脚本全量扫描（txt/md/docx 均支持，docx 自动解包 word/document.xml 复核隐藏标注），清理-重扫强制闭环，残留 > 0 禁止交付    多视角审稿   编辑视角（结构/节奏）+ 读者视角（代入/毒点）+ 数据视角（字数/钩子/伏笔）三视角轮换，每视角 Top 3 问题 + 重写闭环         安装方法  本仓库提供 A/B 双版本，两者共用同一份 SKILL.md 与 references/、scripts/，只是安装位置不同。  方式 A：编码 Agent（Claude Code / Codex 等）  # 方式 1：通过 skills 仓库安装
npx skills add webnovel-studio

# 方式 2：克隆本仓库后注册
git clone https://github.com/holy6679/Webnovel-studio.git
cd Webnovel-studio
bash scripts/install_skill.sh --agent    在 Agent 配置中注册 skills/webnovel-studio 即可触发。  方式 B：Marvis 本地安装  bash scripts/install_skill.sh --marvis <你的 Marvis 技能目录>    脚本会复制 SKILL.md、references/、scripts/ 到目标目录，部署完成后重启或刷新 Marvis 使技能生效。  也可运行 bash scripts/install_skill.sh --test 执行冒烟测试，自检扫描 / 去AI味 / 清理闭环脚本是否正常。   快速上手  安装完成后，直接对你的 AI 助手说下面任一触发语即可：  帮我扫一下番茄的榜单，选个题材写小说 —— 扫榜选题  我要开一本新书，先做设定问答 —— 三层问答设定  按大纲写第三章，注意伏笔 —— 分章写作  把我这段改得不像AI写的 —— 去AI味  投稿前扫一遍AIGC痕迹 —— AIGC 痕迹确定性校验  这本书写到第20章了，帮我做一致性检查 —— 伏笔/设定一致性校验  帮我这章审稿 —— 多视角审稿  典型流程示例  "我要开一本新书，先做设定问答"
  → 三层问答 → book.md 书籍档案
  → 大纲规划 → outline.md + 伏笔台账
  → "按大纲写第一章" → chapters/ch_001.md
  → "把我这段改得不像AI写的" → 去AI味改写
  → "帮我这章审稿" → 三视角审稿 + 重写
  → "投稿前扫一遍AIGC痕迹" → 三项校验全绿 → 交付    门禁规则：任何外部交付（复制 / 上传 / 导出）前必须重跑 AIGC 全量扫描；字数检查、一致性检查、AIGC 扫描三项全部通过才可交付。  目录结构  仓库结构  Webnovel-studio/
├── SKILL.md                  # 技能主定义（名称、描述、全流程、能力开关、触发语）
├── README.md                 # 本文档
├── LICENSE                   # MIT 许可证
├── references/               # 各阶段操作手册
│   ├── workflow.md           # 全流程操作手册（必读）
│   ├── scan-analyze.md       # 扫榜拆文方法论（Phase 1-2）
│   ├── setup-planning.md     # 三层问答与大纲规范（Phase 3-4）
│   ├── writing-consistency.md# 写作守则与一致性追踪（Phase 5）
│   ├── deai-scan.md          # 去AI味规则 + AIGC 变体清单（Phase 6）
│   └── review-validation.md  # 审稿视角与校验标准（Phase 7-8）
├── scripts/                  # 确定性校验脚本
│   ├── scan_ai_traces.py     # AIGC 痕迹全量扫描（含 docx 解包）
│   ├── clean_ai_traces.py    # AIGC 痕迹清理 + 自动重扫（强制闭环）
│   ├── deai_rules.py         # 去AI味规则引擎（段落级命中检测）
│   ├── check_consistency.py  # 伏笔 / 设定一致性检查
│   ├── wordcount_check.py    # 字数与断章钩子检查
│   └── install_skill.sh      # A/B 双版本部署脚本
├── evals/                    # 评估样例
└── assets/                   # 资源文件    每本书的工作区结构（Skill 运行时生成）  <书目录>/
├── book.md            # 书籍档案（三层问答产物）
├── outline.md         # 全书大纲 + 卷纲
├── chapters/          # 正文章节，ch_001.md 起
├── memory/            # 文件系统记忆
│   ├── world.md       # 世界观：力量体系 / 地理 / 组织 / 规则
│   ├── characters.md  # 人物卡：动机 / 关系 / 成长线
│   ├── plot_threads.md# 伏笔与悬念台账：埋设 / 兑现 / 状态
│   └── benchmark.md   # 扫榜选题报告（可选）
├── reviews/           # 审稿记录
└── state.json         # 写作状态库（当前章节 / 草稿状态 / 伏笔）    许可证  本项目基于 MIT License 开源，完整文本见 LICENSE。  SPDX-License-Identifier: MIT    Copyright (c) 2026 WebNovel Studio Authors  你可以自由使用、复制、修改、合并、发布、分发、再许可及销售本软件副本，唯需保留上述版权与许可声明。本软件按"现状"提供，不附带任何明示或默示的担保。
