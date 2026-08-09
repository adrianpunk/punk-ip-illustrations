# 角色资产包与状态

## 目录

- 运行目录与结构
- 角色状态机
- Manifest
- 注册脚本
- 路径降级

## 运行目录

优先把运行数据放在当前项目根目录：

```text
<project-root>/.punk-ip-assets/
```

没有可写项目、宿主沙箱不允许写入或用户希望跨项目复用时，回退到：

```text
~/.punk-ip-assets/
```

用户明确指定目录时遵循用户选择。不要把 Skill 安装目录当作运行目录，也不要把用户照片或生成角色写入 GitHub 仓库。

## 目录结构

```text
.punk-ip-assets/
├── current-character.json
├── characters/
│   └── <character-slug>/
│       ├── character.json
│       ├── character-sheet.png
│       ├── character-reference-clean.png
│       ├── character-spec.md
│       └── *-v2.png
└── illustrations/
    └── <article-slug>/
        ├── 01-topic.png
        └── 02-topic.png
```

`character-slug` 使用简短英文小写 kebab-case，只包含字母、数字和连字符。中文角色名保存在 manifest 的 `name` 字段，不把私人路径或照片文件名直接作为 slug。

## 状态机

- `draft`：角色资产已经生成或修订，等待用户确认；不能用于文章插图，不能设为当前角色。
- `confirmed`：用户明确确认，可用于文章插图并可设为当前角色。

每次修订都增加 `revision`，保留旧图片并把 manifest 指向最新版本。用户只说“看起来不错”但没有明确确认时，继续视为草稿；用户说“确认”“定稿”“就用这个”时才确认。

## Manifest

`character.json` 至少包含：

```json
{
  "schema_version": 1,
  "slug": "zhang-san",
  "name": "张三",
  "status": "confirmed",
  "revision": 1,
  "created_at": "2026-08-09T00:00:00+00:00",
  "updated_at": "2026-08-09T00:00:00+00:00",
  "confirmed_at": "2026-08-09T00:00:00+00:00",
  "assets": {
    "sheet": "character-sheet.png",
    "clean_reference": "character-reference-clean.png",
    "spec": "character-spec.md"
  }
}
```

`current-character.json` 只保存当前已确认角色的 slug 和 manifest 相对路径，不复制完整人物规范。

## 注册脚本

从 Skill 根目录运行。`<runtime-root>` 是前述 `.punk-ip-assets` 目录。

注册草稿并把外部生成结果复制进角色包：

```bash
python3 scripts/character_registry.py register \
  --root <runtime-root> \
  --slug zhang-san \
  --name "张三" \
  --sheet <角色设定板路径> \
  --clean-reference <干净人物参考图路径> \
  --spec <人物规范路径>
```

确认并设为当前角色：

```bash
python3 scripts/character_registry.py confirm --root <runtime-root> --slug zhang-san
```

解析当前角色：

```bash
python3 scripts/character_registry.py resolve --root <runtime-root>
```

切换到另一个已确认角色：

```bash
python3 scripts/character_registry.py activate --root <runtime-root> --slug li-si
```

列出全部角色：

```bash
python3 scripts/character_registry.py list --root <runtime-root>
```

注册并启用内置 Punk：

```bash
python3 scripts/character_registry.py register \
  --root <runtime-root> \
  --slug punk \
  --name "Punk" \
  --sheet <skill-root>/assets/punk-character-sheet.png \
  --clean-reference <skill-root>/assets/punk-character-reference-clean.png \
  --spec <skill-root>/references/character-spec.md

python3 scripts/character_registry.py confirm --root <runtime-root> --slug punk
```

内置 Punk 资产来自 Skill 安装目录，只在首次启用或资源版本升级时复制到本地角色包。

脚本不可运行时，可以手动建立同等目录和 JSON 文件，但必须保持状态规则、资产存在性检查和非覆盖版本规则。

## 路径降级

图像工具无法把文件复制到角色包或插图目录时：

1. 保留工具返回的实际绝对路径。
2. 在 manifest 中记录该实际路径，或明确告知用户角色尚未完成注册。
3. 不伪造目标文件已经写入。
4. 未能形成完整角色包时，不把角色标记为 `confirmed`。
