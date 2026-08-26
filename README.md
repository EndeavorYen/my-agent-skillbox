# my-agent-skillbox

公開的 agent skills。每個一級資料夾都是獨立單元，彼此沒有硬依賴。之後要把某個單元拆成獨立 repo 時，複製該資料夾即可。

安裝時先進那個資料夾，再跑它自己的安裝指令。

實測實用程度是維護者使用觀感：1 幾乎不派上用場，5 會主動拿來用。不是評測分數。

| 單元 | 用途 | 實測實用程度 |
| --- | --- | --- |
| [gentle-grill-me](gentle-grill-me/) | 壓力測試計畫，但不使用讓人覺得被看扁的措辭 | ★★★★☆ |
| [reality-slap-skill](reality-slap-skill/) | 讓建議錨在證據上，而不是跟著最新提問框架搖擺 | ★★★☆☆ |
| [claude-env](claude-env/) | Claude Code 環境、marketplace，以及 misc / squad / battle plugins | ★★☆☆☆ |
| [Bald-Patch](Bald-Patch/) | Codex anti-overbuild：最小安全 diff，並審查是否過度工程 | ★☆☆☆☆ |

## Dedicated skills

### [gentle-grill-me](gentle-grill-me/)

用 grilling 的 design tree 壓力測試計畫或決策，但不用會讓人覺得被看扁的措辭。觸發語是 `gentle grill me` 或 `/gentle-grill-me`，不會搶走原本的 `grill me`。

```powershell
cd gentle-grill-me
.\scripts\install.ps1 grok
```

```bash
cd gentle-grill-me
./scripts/install.sh grok
```

把 `grok` 換成 `claude`、`cursor` 或 `all`，會裝到對應工具。細節以 [gentle-grill-me/README.md](gentle-grill-me/README.md) 為準。

### [reality-slap-skill](reality-slap-skill/)

讓建議錨在證據上，而不是跟著最新的提問框架搖擺。回傳立場、下一步、主要風險，以及什麼證據會讓立場改變。GitHub 原 repo 已 archive；此資料夾保留完整 skill，含 companion `deep-fix`。

```powershell
cd reality-slap-skill
python scripts/install_skill.py install --method copy --force
python scripts/install_skill.py status
```

```bash
cd reality-slap-skill
python3 scripts/install_skill.py install --method copy --force
python3 scripts/install_skill.py status
```

預設裝到 `$CODEX_HOME/skills/reality-slap`（未設定時為 `~/.codex/skills/reality-slap`）。細節以 [reality-slap-skill/README.md](reality-slap-skill/README.md) 為準。

## Plugin / Codex packs

這些 repo 裡的 skill 不是根目錄單一 `SKILL.md`，而是 plugin 或 Codex pack。pack 本身仍是獨立一級資料夾，裡面的 skill 不拆到根目錄，以免打斷原本的安裝方式。

### [claude-env](claude-env/)

Claude Code 環境與 marketplace。GitHub 上的 [claude-squad](https://github.com/EndeavorYen/claude-squad) 與 [claude-misc](https://github.com/EndeavorYen/claude-misc) 已 archive，並寫明併入此 repo 的 `plugins/squad` 與 `plugins/misc`，所以這裡只放這一份活的來源。

```bash
cd claude-env
bash install.sh setup
```

Windows 用 Git Bash 跑同一組指令。細節以 [claude-env/README.md](claude-env/README.md) 為準。

| Plugin | Inner skills / commands | 用途 | 實測實用程度 |
| --- | --- | --- | --- |
| `plugins/misc` | `challenge`, `code-review`, `design-check`, `scaffold-feature`, `test-gen`, `verify`, `write-doc` | 審查、對照設計、建骨架、產測試、驗證、寫文件、挑戰提案 | ★★☆☆☆ |
| `plugins/squad` | `mission-planning`, `role-forging`, `tool-forging`, `integration`, `gate-check`, `status-report`, `retrospective` | `/squad` 七段 pipeline：RECON → PLAN → EXECUTE → INTEGRATE → VERIFY → DEBRIEF → RETRO | ★★☆☆☆ |
| `plugins/battle` | `/battle` command | 對抗式品質檢查 | ★★☆☆☆ |

### [Bald-Patch](Bald-Patch/)

Codex 用的 anti-overbuild skill：用最小安全 diff 修問題，並審查是否過度工程。GitHub 原 repo 已 archive。

```powershell
cd Bald-Patch
New-Item -ItemType Directory -Force -Path "$HOME\.agents\skills" | Out-Null
Copy-Item -Recurse .agents\skills\baldpatch-patch "$HOME\.agents\skills\"
Copy-Item -Recurse .agents\skills\baldpatch-review "$HOME\.agents\skills\"
```

```bash
cd Bald-Patch
mkdir -p "$HOME/.agents/skills"
cp -R .agents/skills/baldpatch-patch "$HOME/.agents/skills/"
cp -R .agents/skills/baldpatch-review "$HOME/.agents/skills/"
```

| Skill | 用途 | 實測實用程度 |
| --- | --- | --- |
| `baldpatch-patch` | 以最小安全 diff 實作，避免多餘依賴與無關重寫 | ★☆☆☆☆ |
| `baldpatch-review` | 審查 patch 是否過度工程，不當唯一裁判 | ★☆☆☆☆ |

細節以 [Bald-Patch/docs/installation.md](Bald-Patch/docs/installation.md) 為準。

收集範圍、資料夾形狀、以及本檔怎麼寫，見 [AGENTS.md](AGENTS.md)。確認目錄與資料夾仍對得上：

```text
python tools/check_monorepo.py
```
