# my-agent-skillbox 規範

此檔是這個 repository 的收集、資料結構、與根目錄 README 寫法契約。Agent 與貢獻者改這個 repo 時讀這個檔，不要把政策再寫進各 skill 資料夾。

| 檔案 | 職責 |
| --- | --- |
| `AGENTS.md` | 政策。收集什麼、樹長什麼樣子、README 怎麼寫。 |
| `README.md` | 目錄。每個一級單元的用途與安裝指令。 |
| `CLAUDE.md` | 指向 `AGENTS.md`，不重複政策。 |
| `tools/check_monorepo.py` | 把下列可機械檢查的規則跑成 PASS / FAIL。 |
| 各一級資料夾 | 完整、可拆走的 skill 或 pack。 |

根目錄 `README.md` 不是第二份政策。改政策只改這個檔。

## 收集

收進這個 repo 的是 **公開 skill 單元**：GitHub 上 `EndeavorYen` 擁有、且至少含一份 `SKILL.md` 的公開 repository。

單元分兩類：

| 類別 | 判定 | 一級資料夾裡放什麼 |
| --- | --- | --- |
| Dedicated skill | repository 根目錄有 `SKILL.md` | 該 repo 的完整內容 |
| Pack | `SKILL.md` 在 plugin、`.agents/skills/`、或同等巢狀路徑 | 該 repo 的完整內容；巢狀 skill 不抽到本 repo 根目錄 |

不要收：

- 私有 repository（私有 skill 放 `my-agent-skillbox-private`）
- 沒有 `SKILL.md` 的應用程式或產品 repo
- 產品 runtime 裡嵌、無法獨立安裝的 `SKILL.md`（例如只在 `sesstalk` 裡才有意義的 skill）
- 已寫明併入另一個仍在收集範圍內之 pack 的 archive repo（例如 `claude-squad`、`claude-misc` 已併入 `claude-env`）。在根目錄 README 用一句話指向活的 pack，不要再複製一份一級資料夾

複製規則：

1. 一級資料夾名稱等於 GitHub repository 名稱，大小寫一致。
2. 複製該 repo 的完整樹，去掉巢狀 `.git`。
3. 不要改 skill / pack 內部的 `SKILL.md`、安裝腳本、或原始安裝文件，除非使用者明確要求改那個單元。
4. 新增、刪除、或重新命名一級資料夾，與更新根目錄 `README.md` 是同一次變更。
5. 變更後在本 repo 根目錄執行 `python tools/check_monorepo.py`，必須 PASS。

## 資料結構

```text
my-agent-skillbox/
├── AGENTS.md                 政策（本檔）
├── CLAUDE.md                 指向 AGENTS.md
├── README.md                 目錄
├── LICENSE
├── tools/
│   └── check_monorepo.py
└── <unit>/                   每個公開 skill 單元一個一級資料夾
    └── SKILL.md              dedicated skill：在這個位置
        或巢狀 SKILL.md        pack：留在 pack 原本的路徑
```

允許出現在根目錄的項目：`AGENTS.md`、`CLAUDE.md`、`README.md`、`LICENSE`、`.gitignore`、`tools/`、以及各 skill 單元資料夾。不要在根目錄新增共用函式庫、共用安裝器、或跨單元的 source 目錄。

獨立性：

- 每個一級資料夾必須能單獨複製出去，變成獨立 repo 後仍可依它自己的文件安裝。
- 禁止一級資料夾用相對路徑、import、或安裝器去依賴另一個一級資料夾。
- 禁止根目錄安裝器讓 skill 腳本必須呼叫它才能安裝。安裝永遠是：先 `cd` 進該資料夾，再跑該單元自己的指令。
- Pack 內的 skill、commands、hooks 留在 pack 內。把它們提升到本 repo 根目錄會打斷原本的 plugin / Codex 安裝。
- 根目錄 `tools/` 只檢查這個 monorepo，不是任何 skill 的執行期依賴。

## README 撰寫

根目錄 `README.md` 只做目錄。讀者要能從它知道每個一級單元做什麼、怎麼裝。

結構固定為這個順序：

1. 標題與兩段說明：這是公開 skill 目錄；一級資料夾互相獨立；安裝先 `cd` 再跑該單元自己的指令。
2. `## Dedicated skills`：根目錄有 `SKILL.md` 的單元。
3. `## Plugin / Codex packs`：巢狀 `SKILL.md` 的單元。
4. 一段指向 `AGENTS.md` 的規範連結，以及 `python tools/check_monorepo.py`。

每個一級單元用恰好一個三級標題，形式固定：

```markdown
### [<folder>](<folder>/)
```

`<folder>` 必須與一級資料夾名稱完全相同。不要為 pack 裡的單一 skill 另開三級標題。

每個單元標題底下依序寫：

1. **用途**：一到三句。名稱、路徑、指令保留原文；說明用繁體中文。
2. **狀態**：若來源 GitHub repo 已 archive，在用途裡寫明。若它是別的 archive repo 合併後的活來源，寫明那些 archive 的名字與它們現在落在這個資料夾的哪一層。
3. **安裝**：先寫 `cd <folder>`，再寫該單元自己文件裡的安裝指令。Windows 與 Unix 分成兩個 fence。根目錄 README 不發明第二套安裝協定；細節連到該單元自己的 README 或安裝文件。
4. **內層清單**：只有 pack 需要。用表格列出內層 skill 或 command 的名稱與一句用途。不要為內層項目寫獨立安裝指令。

同步規則：根目錄 README 的三級標題集合，必須等於含有 `SKILL.md` 的一級資料夾集合。多一個標題或少一個資料夾，都是不完整的變更。

不要在根目錄 README 寫：

- 私有 skill 的名字或路徑
- 跨單元的共用安裝器
- skill 內部協議的完整複本（那是各單元自己的 README / `SKILL.md`）
- 收集政策的完整複本（那是 `AGENTS.md`）
