[English](README.md) · `中文说明`
# ai-trace-remover

> 一个去 AI 味（去机器味）skill——核心是 **检测与量化 AI 痕迹** 与 **补回活人感**。
> 内置检测器负责让痕迹可见、可量化：AI 模式命中、0–100 人话指数、必须清零的
> 硬禁令、声音五条；改写由 Agent 手工完成，保住作者的声音，而不是用一套模板
> 换另一套。

**免责声明**：本仓库包含作者为自动化科研工作流而开发的辅助工具。它不是经过同行评审的学术项目。部分样板代码或实用脚本可能在 AI 辅助下生成，并经过作者高层面的审查与修改整合。作者对任何第三方代码问题不承担责任，但承诺及时处理任何合理的诉求。
<!-- TOC depthFrom:2 -->

- [ai-trace-remover](#ai-trace-remover)
  - [设计原则与核心特征](#设计原则与核心特征)
  - [下载与安装](#下载与安装)
  - [快速开始](#快速开始)
  - [测试与覆盖率](#测试与覆盖率)
  - [项目结构](#项目结构)
  - [作为 Agent 技能挂载使用](#作为-agent-技能挂载使用)
  - [开源协议](#开源协议)
  - [报告问题与反馈](#报告问题与反馈)

<!-- END_TOC -->

ai-trace-remover 是通用的去 AI 味 skill，中英文通吃。它去掉让文字读起来像模型直出的
那些痕迹，并给出一个量化分数，让成稿只在痕迹清掉、背后还有真人时才能交付。
模式分类与例句为原创；before/after 语料由自撰句子和公有领域教材、公有领域经典小说
拼成，不复制任何其他去 AI 味 skill 的代码。

两条腿，缺一不可：**洗得掉机器味**（词面 + 结构模式库、0–100 评分、必须清零
的硬禁令）与**补得上活人感**（创作纪律、七遍改稿、声音五条）。只删套话不补
具体，只会把"AI 体"变成"新闻通稿"——背后仍然没有人。

```
输入文本  （中文或英文）
        |
        v
   +---------------------------+
   | scan (src/core/engine.py) |
   |  词面命中              |--> 0-100 分（中文人话指数 / 英文 AI 味分）
   |  结构计数              |
   |  硬禁令规则            |--> 阻断交稿项（必须清零）
   |  声音五条              |--> 五项人工核对
   +---------------------------+
        |
        v
   Markdown / JSON 报告       （Agent 手工改写后，再复跑一遍）
```

**唯一需要记住的规则：引擎只检测、只量化——绝不代改。** 词面干净不等于"有
人味"；声音五条与冷读四问是 Agent 的活。两把相反的尺子不要混用：中文给
0–100 **人话指数**（越高越人话），英文给 **AI 味分**（越高越像 AI）。

---

## 设计原则与核心特征

- **触发即执行**：命中"让文字像人写的 / 去 AI 味 / 打个 AI 味分"即整套触发
  ——先扫描、再手工改写、再复扫；只描述痕迹而不跑检测器，视为失败。
- **只检测、不改写**：`src/core/` 引擎让痕迹可见、可量化；改写是 Agent 按
  `references/` 做的事，保住作者的声音，而不是用新模板替换旧模板。
- **纯标准库**：无安装、无联网、无第三方依赖。`python -m src.cli` 在
  Windows / macOS / Linux 上直接跑。
- **两把相反的尺子**：中文 0–100 **人话指数**（越高越人话），英文 **AI 味分**
  （越高越像 AI）；方向相反，绝不混用。
- **硬禁令阻断交稿**：一小撮"成稿绝对不能出现"的规则（破折号、提示性冒号、
  翻案腔、商业黑话、结尾升华、英文口水/谄媚/cutoff 免责）。命中任一项，
  分数再高也不能交稿。
- **声音五条**：具体数字、具体名词、不确定性、说话人在场、节奏变化（仅参考）；
  前四条脚本量化，节奏只作参考，交稿前五项须人工全过。

### 三条路径（速览）

本技能是一条"去执行"的指令，不是一份供总结的文档：命中触发条件就**必须
运行检测器**并报告它发现了什么——用对痕迹的描述来作答是一种**任务失败**，
不是结果。完整步骤以 `SKILL.md` 为准，要点如下：

1. **按用户要什么选路径**：从零写有活人感的中文 → **A · 创作**；已有成稿
   嫌像机器写的 → **B · 去味改写**；只想检测、打个分 → **C · 只检测**。
2. **路径 A（创作）**：先过材料关（非虚构长稿动笔前至少列五件具体、
   可核验的材料），再"带着人"写第一稿，再走七遍改稿，最后跑检测器。
3. **路径 B（改写）**：扫描定位，按优先级（`A4 → A3 → A6 → A1 → A7 → A8`）
   改写，补具体与不确定性，复跑到硬禁令清零且人话指数 ≥ 85（中文）。
4. **路径 C（只检测）**：跑一次、出一份报告、给 Top 3 建议，不顺手改写
   （除非用户追加要求）。
5. **交稿门槛不是全部**：85 分但声音五条没过，仍要改；数字不替人工判断。

---

## 下载与安装

获取本技能共有**四种**标准方式：

**方式一 —— Windows 可执行文件（无需 Python）**

**Releases** 页发布 `ai-trace-remover-<version>-windows.exe`，一个由
`build_dist.py --exe` 构建的单文件 Windows 二进制，内置了完整检测器与 CLI：

```bash
ai-trace-remover.exe 稿件.md --score-only
ai-trace-remover.exe 稿件.md -o report.md
```

Windows 二进制面向没有 Python 的用户；macOS / Linux 请用下面的源码包方式，
它仅依赖标准库即可运行。

**方式二 —— 源码包（推荐，全平台）**

从 **Releases** 页下载 `ai-trace-remover-<version>.zip`，解压即用，无需
安装器：

```bash
unzip ai-trace-remover-1.0.0.zip
cd ai-trace-remover-1.0.0            # 整个技能就是这一个文件夹
python -m src.cli 稿件.md
```

无构建步骤、无依赖。`python -m src.cli` 在 Windows / macOS / Linux 上直接跑
（Python 3.9+）。

**方式三 —— 让 Agent 自行获取**

把下面这段指令复制给 Agent，它会自动定位本技能、从 **Releases** 页下载并
替你装好：

> 请访问 https://github.com/JiamingShi-JsPhys/ai-trace-remover，阅读仓库根目录的 `README.md`，并按照其中的说明下载或安装本技能。

你只需要把技能名告诉 Agent，剩下的交给它。

**方式四 —— 克隆仓库**

```bash
git clone https://github.com/JiamingShi-JsPhys/ai-trace-remover.git
cd ai-trace-remover
```

环境要求：Python 3.9+。无第三方依赖——检测器与 CLI 仅使用标准库实现。
（`pytest` 可选，仅供测试套件使用。）

---

## 快速开始

```bash
cd ai-trace-remover

# 0. （可选）单行摘要，供流水线：分数 / 等级 / 能否交稿
python -m src.cli 稿件.md --score-only

# 1. Markdown 报告到 stdout
python -m src.cli 稿件.md

# 2. 机器可读 JSON（供下游工具的契约）
python -m src.cli 稿件.md --json

# 3. 管道，不写临时文件
cat 稿件.md | python -m src.cli -

# 4. 报告写文件
python -m src.cli 稿件.md -o report.md
```

其他命令：

```bash
python -m src.cli 稿件.md --json -o reports/<name>.json   # JSON 写到文件
python -m src.cli --version                                # ai-trace-remover 1.0.0
```

输出示例：

```
score: 38/100  level: 重度 AI 味  hard_bans=2  can_ship=no
```

看到 `can_ship=yes` 时，硬禁令已清零且（中文）人话指数 ≥ 85——可以交稿。
看到 `can_ship=no` 时，清掉硬禁令、按优先级改写 Top 命中，再复跑；引擎绝不
代改。

### 一次健康会话中的工作流

```
你把稿件交给 Agent（或要一个分数）
        |
        v
   +-----------+      +---------------------------------------+
   |  扫描     |----->| Markdown / JSON 报告                |
   | (src.cli) |      |  命中 + 分数 + 硬禁令 + 声音五条    |
   +-----------+      +---------------------------------------+
        |
        v  （Agent 按 references/ 手工改写）
   +-----------+
   |  复扫     |  -->  硬禁令清零 + 人话指数 ≥ 85 -> 交稿
   +-----------+
```

目标是让稿件对自己的痕迹保持诚实：检测器让痕迹可见、可量化，Agent 用具体与
声音修正，第二遍扫描在交稿前证明修正到位。

### 分步调用（作为 Python 库使用）

```python
from src.core import scan

text = open("稿件.md", encoding="utf-8").read()
report = scan(text, "稿件.md")
print(report.score, report.ai_taste_score)
print(report.hard_failures, report.can_ship())
```

---

## 测试与覆盖率

```bash
pytest                                            # 运行全部测试
pytest --cov=src --cov-report=term-missing        # 带覆盖率报告
```

当前测试套件共 52 个用例，覆盖率约 85%（目标 >= 80%）。

---

## 项目结构

```
ai-trace-remover/
+---- SKILL.md              # 技能入口（YAML 元数据 + 执行指南）
+---- README.md
+---- README_zh.md          # 中文镜像
+---- LICENSE               # MIT
+---- CHANGELOG.md
+---- CITATION.cff
+---- pyproject.toml        # 打包与工具配置
+---- requirements.txt      # 空（纯 stdlib）
+---- src/
|   +---- __init__.py       # __version__
|   +---- cli.py            # CLI：scan / --json / --score-only / -o
|   `---- core/
|       +---- __init__.py
|       +---- engine.py     # scan()：分层检查 + 评分 + 报告
|       +---- patterns_zh.py # 中文词库（A1-A10 + 结构）
|       +---- patterns_en.py # 英文词库（E1-E24）
|       +---- hard_bans.py   # 阻断交稿的"成稿绝对不能出现"规则
|       `---- sound_rules.py # 声音五条
+---- references/
|   +---- ai-patterns-zh.md   # 中文全量词库 + 改写对照
|   +---- ai-patterns-en.md   # 英文全量词库 + 改写对照
|   +---- scoring-rubric.md   # 0-100 算法、等级、交稿门槛
|   +---- revision.md         # 七遍改稿 + 声音五条 + 绝对禁词表
|   `---- example-diff.md     # 4 个跨语言 before/after 场景
`---- tests/
    +---- conftest.py
    +---- test_engine.py      # 中 / 英 / 混合扫描
    +---- test_hard_bans.py   # 硬禁令
    +---- test_cli.py         # 退出码与渲染
    `---- test_skill_docs.py  # 文档契约
```

---

## 作为 Agent 技能挂载使用

本项目是一个自包含的 Agent Skill 包。`SKILL.md` 包含 YAML 元数据
（`name` / `description` / `version` / `author` / `license` / `entry_point`），
并附带"Execution steps"执行指南。只需将本文件夹指向任何 AI Agent
Harness。当用户的需求命中本技能适用范围时，Agent 会读取 `SKILL.md` 中的执行
步骤并调用 `python -m src.cli`（技能的加载取决于 Agent 对适用范围的识别，
并不保证每次对话都会触发）。

给 Agent 的一条重要约定：检测器只检测、只量化——绝不代改。Agent 按
`references/` 手工改写后，**必须复跑检测器**，证明硬禁令清零且（中文稿件）
人话指数已达 85，成稿才能交付。词面干净就报"有人味"、而不跑声音五条，是
一种失败模式，不是捷径。

你也可以直接在 Python 中调用引擎：

```python
from src.core import scan
report = scan(open("稿件.md", encoding="utf-8").read(), "稿件.md")
print(report.score, report.hard_failures)
```

---

## 开源协议

MIT License，详见 [LICENSE](LICENSE)。

---

## 报告问题与反馈

首选：在本仓库的 **Issues** 页面提交问题（对于安全漏洞问题的报告，使用备选
方案）。

备选（仅供报告安全漏洞问题）：发送邮件至 `jiamingshi_git@outlook.com`

- **邮件主题**：必须包含前缀 `agent-skill_report`，并注明具体技能与简要问题。
  - 示例：`agent-skill_report ai-trace-remover: 硬禁令正则把领域必需术语误判为黑话`
- **邮件正文**：必须包含复现步骤、预期行为、实际行为以及运行环境（操作系统、
  Python 版本、相关依赖安装状态）。
- 针对"干净稿件被误判阻断"的严重报告，请附上稿件与生成的报告，便于核对模式
  是否误伤。
- 提交清晰、可复现 Issue 或 Pull Request 的贡献者，将被列入下个版本发布说明
  的致谢名单。
