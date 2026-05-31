# Oral English Practice

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE) [![Claude Code](https://img.shields.io/badge/Claude%20Code-skill-8A2BE2)](https://claude.com/code)

*[English](README.md) | 中文*

**Oral English Practice** 把 Claude App 变成一个不知疲倦的口语陪练，把 Claude Code
变成那个「什么都记得住」的教练。你开口练——真实对话 + 听力——每一次练习都会变成一份
打分报告、一份逐字记录（你卡壳、说错的地方），以及下一次的明确重点。日积月累，「跟 AI
聊天」这种转瞬即忘的事，变成一条**可量化、通往母语级流利度的上升曲线**：分数有趋势、
顽固错误被一个个揪出来、难度还会悄悄调整，始终把你顶在「够得着的边缘」。

诀窍在于把活儿拆给两个各干一半的工具：App 有「嘴」但没记性，Claude Code 有记性但没
「嘴」。这个 skill 就是中间的桥——你只需在两边各粘贴一次，剩下的归档、打分、错题入库、
画趋势、定下次计划，全交给它。

> **一次订阅，两次粘贴，长期练习。**

---

## 亮点 Highlights

**1. 一次订阅，两次粘贴，长期练习。**
不用装新 App、不用再注册、除了你已有的 Claude 订阅不花一分钱。每一轮只是两次复制粘贴——
把提示词贴出去、把报告贴回来——但它们会「复利」：几分钟的开口，攒成几周的可追踪进步，
而不是明天就忘的练习。

**2. 每次练习，一份评估报告。**
一练完就给你一张清晰的成绩单：估算的 CEFR / 雅思等级、一个「距母语 /100」的分数，以及
七个 1–10 维度——流利度、词汇、语法、发音、连贯、互动、听力。进步从此**看得见，而不只是
凭感觉**。

**3. 一个揪着你顽固错误不放的错题银行。**
每一处卡壳、语法错误、不地道的表达都被逐字记录。反复出现的模式会被「确诊」、计数，并在
每次练习中**反复操练，直到你连续不犯才归档**。

---

## 功能 Features

- 🎙️ **开箱即用的陪练提示词** —— 贴进 Claude App 就能立刻开始母语级语音练习（对话 + 听力）。
- 📊 **每次一份评分报告**：CEFR / 雅思估分、「距母语 /100」、七个 1–10 维度。
- 📈 **长期进度追踪** —— 每次练习写入 `data.csv`，带趋势图（没有 Python 就给文字版趋势）。
- 📝 **逐字错误实录** —— 每个卡壳、语法 / 词汇 / 地道度问题，内联标注并解释。
- 🏦 **错题银行** —— 反复出错的模式被确诊、计数、反复操练，攻克后归档。
- 🎚️ **自适应难度** —— 根据你上次的实际分数，告诉教练哪儿放缓、哪儿加压。
- 🎭 **完全可定制** —— 用大白话（或改一个文件）调整教练语气、话题、纠错风格。
- 🌐 **双语 + 按语言自适应** —— 中英文档齐全，skill 用你书写的语言回复你。
- 🔒 **本地优先、隐私** —— 记录只在你电脑上；无上传、无遥测、无第三方。
- 🪶 **极简依赖** —— 只要 Claude Code + Claude App；Python / matplotlib 可选（仅用于出图）。

---

## 工作原理 How it works

```
Claude App（练习场，无记性）            Claude Code + 本 skill（长期大脑）
  · 语音对话 + 听力                      · 解析报告、归档
  · 产出 标注实录 + 报告 + DATA BLOCK  →   · 写入 data.csv、画趋势
                                         · 揪出顽固弱点、写 next-focus
  ← 把 next-focus 贴回 App  ───────────   · 跨练习延续
```

1. **拿提示词** —— 在 Claude Code 里说 `/oral-english-practice`（或「我要练口语」）。它给你
   `app-prompt` 和上次的重点。
2. **练习** —— 把提示词贴进 Claude App（语音模式），聊 15–30 分钟。教练最后给你标注实录 +
   评分报告 + 一行 DATA BLOCK。
3. **记录** —— 把那一整份贴回 Claude Code。skill 自动归档、更新趋势数据、写好下次重点。
4. **复盘** —— 每隔几次，让它给你画趋势 / 复盘。

> 第一次上手？详细的手把手装机与使用步骤见 **[【先看这里】](【先看这里】.md)**。

---

## 安装 Installation

- **Windows**：双击 `install.bat`
- **macOS / Linux**：`bash install.sh`
- **手动**：把 `oral-english-practice/` 文件夹拷进 `~/.claude/skills/`

重复运行安装脚本是安全的——它不碰你的数据。

### 依赖 Requirements

**必需——仅此两个：**
- **Claude Code** —— 跑 skill（记录、错题银行、备份、诊断）
- **Claude App** —— 语音练习 + 听力

就这两个。核心功能全靠 Claude 内置的文件能力，连备份都不需要 Python（Claude 自己复制文件）。

**可选：**
- **Python 3 + `matplotlib`** —— 仅用于出 PNG 趋势图。没有也照常用，趋势会以文字版呈现；
  想要图随时 `pip install matplotlib`。

---

## 你的数据 Your data

首次使用时自动创建，放在一个名字清晰的文件夹里，你随时知道记录在哪。默认位置：
- Windows：`%USERPROFILE%\oral-english-practice-log\`
- macOS / Linux：`~/oral-english-practice-log/`

skill 第一次创建时会**把完整路径打印给你**。

**记录想放哪都行。** 两种改法：
- **最省事**：直接跟你的 Claude 说，比如「把练习记录挪到 `D:\英语\` 去」——它帮你设置好，
  并把已有记录一起搬过去。
- **手动**：在家目录建一个名为 `.oral-english-data-path` 的文件（点开头、无后缀），里面写
  一行你想要的路径（如 `D:\oral-english-practice-log`）。

### 文件 Files

| 文件 | 用途 |
|---|---|
| `app-prompt.md` | 贴进 Claude App 的提示词（教练人格 + 话题池 + 报告格式） |
| `data.csv` | 每次练习一行评分 —— 你的趋势数据集 |
| `transcripts.md` | 逐字错误实录；每个卡壳 / 错误内联标注并解释 |
| `mistakes.md` | 错题银行 —— 确诊的反复错误，带频次 + 状态，反复操练直到攻克 |
| `sessions/` | 每次完整报告（`session-NN-YYYY-MM-DD.md`） |
| `next-focus.md` | 衔接卡；含一段可直接贴进 App 的下次重点 |
| `backups/` | 每次写入前的带时间戳快照（留最近 10 份） |

### 标注标签（在 `transcripts.md` 里）

| 标签 | 含义 |
|---|---|
| [G] | 语法（时态、冠词、单复数、介词…） |
| [V] | 词汇缺口 —— 想说说不出，或用错词 |
| [N] | 不地道 —— 语法对但母语者不这么说 |
| [F] | 流利度磕绊 —— 填充词、重启、长停顿 |
| [P] | 发音 |

---

## 隐私 Privacy

- **记录只在你电脑里。** skill 没有任何联网代码——不上传、不回传、无遥测、无云同步。数据
  文件只写在本地数据目录，`.gitignore` 还保证它们不会被提交到 git。
- **但用它要通过 Claude（云端 AI）。** 练习和处理离不开 Claude Code 和 Claude App，所以你
  处理的内容（报告、语音对话）会作为正常的 Claude 使用经过 Anthropic 服务器，和你平时跟
  Claude 聊天一样——这是用 AI 模型的固有前提，不是 skill 额外传数据。
- **没有第三方。** 除了你本来就在用的 Anthropic，数据不去任何别处，也没有你练习档案的云端副本。

---

## 定制 Customizing

- **教练语气 / 话题 / 纠错风格**：改 `app-prompt.md` 里的提示词块，或直接用大白话让 Claude 帮你改。
- **打分维度**：如果你要改，务必让 DATA BLOCK 那行和 `data.csv` 表头同步，否则 skill 解析不了新报告。

---

## 分享 Sharing

整个文件夹可移植。发给朋友，他跑安装脚本（或把 `oral-english-practice/` 拖进自己的
`~/.claude/skills/`）。他的数据在他自己电脑上全新生成——**skill 是引擎，数据是个人的**——
所以你的任何记录都不会跟着传过去。

---

## 致谢 Acknowledgements

遵循 Claude 官方 `skill-creator` 最佳实践，并借鉴 `fluent` 语言学习套件的模式——错题银行、
写前备份、自适应难度信号——同时刻意保持轻量（CSV + Markdown，不上数据库），专注单人、
母语级目标。

---

## 许可证 License

基于 [MIT License](LICENSE) 发布 © 2026 XcutingUnicorn235。
