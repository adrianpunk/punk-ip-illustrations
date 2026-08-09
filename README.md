# Punk IP Illustrations

**Punk 出品｜上传一张照片，创建自己的个人 IP，再让它进入每一篇文章。**

这是一个完整的 Agent Skill：先把用户上传的人物照片转换成可确认、可复用的个人 IP；角色确认后，再使用同一个 Skill 自动读取文章并生成统一的复古彩色扁平 3D 小剧场插图。

`Punk` 是这个 Skill 的品牌、作者印记和内置示例，不代表只能画 Punk。任何人都可以上传自己的照片，创建自己的角色，再让该角色进入文章、教程、工作流和观点插图。

<p align="center">
  <img src="assets/punk-character-sheet.png" width="560" alt="Punk 内置个人 IP 角色设定图">
</p>

## 效果展示

<table>
  <tr>
    <td width="50%"><img src="docs/images/poverty-template.png" alt="打破清贫模板"></td>
    <td width="50%"><img src="docs/images/value-over-price.png" alt="科研成果高于穿搭价格"></td>
  </tr>
  <tr>
    <td width="50%"><img src="docs/images/double-standard.png" alt="成功女性面对的双重标准"></td>
    <td width="50%"><img src="docs/images/article-workflow.png" alt="收集资料、筛选证据、形成判断并输出文章的流程拆解"></td>
  </tr>
</table>

## 完整流程

```text
上传人物照片
    ↓
生成主角色＋正面／左侧／背面／右侧设定板
    ↓
生成干净人物参考图和人物规范
    ↓
用户修改或确认角色
    ↓
确认后的角色成为当前 IP
    ↓
读取完整文章并自动决定配图数量
    ↓
逐张生成小剧场插图并报告插入位置
```

角色确认是唯一必须停下来等待用户的环节。文章图片方案默认自动执行，不要求用户逐张确认。

## 它会自动完成什么

- 从真人照片提取可观察的辨识特征。
- 生成主角色和正面、左侧、背面、右侧四视图。
- 生成透明或纯白背景的干净单人物参考图。
- 建立人物规范和本地角色资产包。
- 支持修改、确认、保存、列出和切换多个角色。
- 读取完整文章并按信息密度自动决定配图数量。
- 自动选择“流程拆解”或“核心动作”模式。
- 逐张生成独立的 16:9 文章插图。
- 报告每张图片的实际路径、用途和建议插入位置。

## 安装

### 让 AI Agent 自动安装

把下面这段话发送给能够访问终端和文件系统的 AI Agent：

```text
请帮我安装这个 Agent Skill：
https://github.com/adrianpunk/punk-ip-illustrations

请根据当前客户端确定正确的 Skills 安装位置。安装完成后确认 punk-ip-article-illustrations 可以使用。
```

### 手动安装到 Codex

macOS / Linux：

```bash
git clone https://github.com/adrianpunk/punk-ip-illustrations.git ~/.codex/skills/punk-ip-article-illustrations
```

Windows PowerShell：

```powershell
git clone https://github.com/adrianpunk/punk-ip-illustrations.git "$HOME\.codex\skills\punk-ip-article-illustrations"
```

如果使用其他支持 Agent Skills 的客户端，请把仓库克隆到该客户端的 Skills 目录，并保持目录名为 `punk-ip-article-illustrations`。

## 怎么使用

### 直接使用内置 Punk 角色

作者本人或希望先体验效果的用户，不需要重新创建角色：

```text
使用 $punk-ip-article-illustrations。
启用内置 Punk 角色，然后完整读取下面的文章，自动决定配图数量并直接生成：

<文章正文、文件路径或文章链接>
```

内置 Punk 已经确认，会被复制到用户本地角色包并设置为当前角色。它也是仓库效果图所使用的角色。

### 第一步：上传照片，创建个人 IP

上传一张人物清晰的照片，然后发送：

```text
使用 $punk-ip-article-illustrations。
请根据我上传的照片创建“<名字或昵称>”个人 IP。
保留我的脸型、五官比例、发型、肤色、服装、鞋子和已有配件。
```

Skill 会生成：

- 竖版角色设定板。
- 干净单人物参考图。
- `character-spec.md` 人物规范。
- 状态为 `draft` 的本地角色包。

生成完成后，Skill 会展示角色并等待确认，不会立即开始文章配图。

### 第二步：修改或确认角色

不满意时直接说明要改哪里：

```text
发型再接近原照片一点，其他特征保持不变。
```

```text
鞋子改回照片里的白色运动鞋，脸和服装不要变化。
```

满意后发送：

```text
确认这个角色，就用这一版。
```

只有明确确认后，角色才会变为 `confirmed`，并成为当前使用的个人 IP。

### 第三步：使用同一个 Skill 给文章配图

确认角色后，继续发送：

```text
继续使用 $punk-ip-article-illustrations。
请完整读取下面的文章，自动决定配图数量并直接逐张生成。
告诉我每张图片适合插在哪里：

<文章正文、文件路径或文章链接>
```

不需要重新上传人物照片。Skill 会自动读取当前已确认的角色资产。

### 为单个观点生成一张图

```text
使用 $punk-ip-article-illustrations，用当前角色给下面的观点生成一张核心动作模式正文插图：

真正的效率不是同时做更多事情，而是减少无效切换。
```

### 指定配图数量

```text
使用 $punk-ip-article-illustrations，完整读取下面的文章，并使用当前角色生成 5 张正文插图：

<文章内容>
```

### 指定表现模式

```text
使用 $punk-ip-article-illustrations，把下面的工作流生成一张流程拆解图：

收集资料 → 筛选证据 → 形成判断 → 输出文章
```

```text
使用 $punk-ip-article-illustrations，把下面的观点生成一张核心动作图：

写，是所有内容形态的底层能力。
```

## 多个角色

可以为自己、团队成员或不同品牌分别创建角色。

列出角色：

```text
使用 $punk-ip-article-illustrations，列出我已经创建的全部角色。
```

切换角色：

```text
使用 $punk-ip-article-illustrations，切换到“小明”，然后给下面的文章配图：
<文章内容>
```

只有已确认角色可以激活和用于文章配图。

## 自动配图数量

| 内容规模 | 默认数量 |
| --- | ---: |
| 单个观点或 500 字以内 | 1 张 |
| 约 500—1500 字 | 1—3 张 |
| 约 1500—3500 字 | 3—5 张 |
| 约 3500 字以上 | 4—8 张 |

数量跟随信息密度。Skill 会合并重复内容，不会为了凑数量制造无效图片；用户指定数量时优先遵循用户要求。

## 两种插图模式

### 流程拆解

适用于步骤、方法、教程和工作流。内容被压缩为 3—5 个节点，同一角色可以在不同节点重复出现，但每个分身都必须执行具体动作。

### 核心动作

适用于观点、冲突、处境和反直觉关系。画面只保留一个角色、一个核心物件或紧凑物件组、一个动作和一个可见结果。

两种模式均使用横版 16:9、纯白页面、大面积留白和复古彩色扁平 3D 小剧场风格。

## 本地文件结构

运行结果默认保存在当前项目的 `.punk-ip-assets/`：

```text
.punk-ip-assets/
├── current-character.json
├── characters/
│   └── <角色名>/
│       ├── character.json
│       ├── character-sheet.png
│       ├── character-reference-clean.png
│       └── character-spec.md
└── illustrations/
    └── <article-slug>/
        ├── 01-topic.png
        └── 02-topic.png
```

没有可写项目目录时回退到 `~/.punk-ip-assets/`。同名文件不会被覆盖，而是创建 `-v2`、`-v3` 版本。

## 安装后的最小测试

1. 上传一张人物照片，使用第一步提示创建角色。
2. 检查是否生成设定板、干净人物图和草稿角色包。
3. 发送“确认这个角色”。
4. 使用以下观点测试文章插图：

```text
使用 $punk-ip-article-illustrations，用当前角色生成一张核心动作模式插图：
真正的效率不是同时做更多事情，而是减少无效切换。
```

预期结果：角色创建阶段会等待确认；确认后生成一张独立 16:9 PNG，背景纯白，人物身份与角色包一致，回复包含实际路径和建议插入位置。

## 常见问题

| 问题 | 处理方式 |
| --- | --- |
| 角色设定板的四视图不一致 | 只修正身份漂移，重新对照原照片并保持其他特征不变 |
| 文章配图出现设定板标题或米色背景 | 移除设定板，只传干净人物参考图并强调纯白页面 |
| 人物服装或配件变化 | 重新读取 `character-spec.md`，只修正漂移项目 |
| Skill 直接开始给文章配图 | 检查角色是否已经明确确认；草稿角色不能用于配图 |
| 找不到当前角色 | 列出角色，并激活一个状态为 `confirmed` 的角色 |
| 图片中文字错误 | 减少非必要文字，使用短标签并重新生成该张 |
| 无法写入目标目录 | 保留图像工具返回的实际路径，并在交付中原样报告 |

## 隐私

- 原始人物照片默认不会复制进角色包，也不会上传到本仓库。
- 角色、文章和插图保存在用户本地，不提交到 GitHub。
- Skill 不根据照片推断姓名、职业、民族、健康、政治、宗教、性取向等敏感属性。
- 请只使用自己拥有或已经获得授权的人物照片。

## 要求

- AI Agent 支持 Agent Skills 和本地文件读写。
- 客户端具备图像生成和参考图能力；否则 Skill 只能输出提示词与保存计划。
- 使用网页文章时，Agent 需要能够获取完整正文。

## 授权

工作流、脚本和文档按 [MIT License](LICENSE) 发布。用户上传的照片、生成角色和文章插图不属于仓库内容，其权利由用户和所使用的图像服务条款决定。

- 内置 Punk 人物设定图及角色资产不包含在 MIT 授权中，详见 [LICENSE-ASSETS](LICENSE-ASSETS)。
- 工作流结构参考了 [jinchenma94/jinchenma-ip-skills](https://github.com/jinchenma94/jinchenma-ip-skills) 的开源思路。

## 关于作者

**Punk**｜中科大 MBA｜HerName 首席设计师｜Stanley 商学院执行院长

持续分享小白能看懂、复制能上手的 AI、内容与搞钱方法：[@AdrianPunk115](https://x.com/AdrianPunk115)
