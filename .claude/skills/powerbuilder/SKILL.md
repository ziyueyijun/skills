---
name: powerbuilder
description: >-
  PowerBuilder 官方开发文档查询技能。由 /powerbuilder 命令手动触发。覆盖：PowerScript 语言
  （语法/语句/事件/函数/数据类型）、DataWindow 与 DataStore（对象属性/表达式函数/方法/常量/
  事务对象）、窗口与控件（Window/ListView/TreeView/Tab 等，含属性与事件）、数据库连接
  （ODBC/OLE DB/直连/连接参考）、部署到 .NET、应用技术（OOP/XML/RichText/COM/邮件）、安装与
  发布公告。
disable-model-invocation: true
---

# PowerBuilder 官方文档查询

本技能把 SAP PowerBuilder 的 16 份官方文档（共约 6800 页）的全文索引进一个 SQLite 数据库
`references/pb_docs.db`，用脚本毫秒级检索。**核心原则：不要凭记忆编造 PowerBuilder 的 API
细节，凡涉及具体函数签名、属性名、枚举值、语法，一律查索引。**

## 运行前提（复制即用）

- 只需本技能目录中的 `references/pb_docs.db`（已预构建）。
- 查询脚本只用 Python **内置** `sqlite3`（FTS5），无需安装任何第三方包；但需要一个
  **Python 3.11+ 运行时**。
- 检查当前机器是否有 Python：`python --version`（Windows 下也可试 `py --version`）。
- **若提示找不到 `python` / `py`**：说明该机器未安装 Python，请先安装 Python 3.11+
  （https://www.python.org/downloads/），否则 `search_db.py` / `get_pages.py` 无法运行。
- 整个技能目录可整体复制到任何装有 Python 3.11+ 的机器使用，无需联网、无需额外模型。

## 文档清单（主题）

| 主题 | 页数 |
|---|---|
| 桌面专业版发布公告 | 18 |
| 企业版发布公告 | 26 |
| 桌面专业版安装 | 38 |
| 企业版安装 | 42 |
| 应用技术：OOP/PowerScript/XML/RichText/COM/.NET 客户端等 | 744 |
| 连接数据库：如何配置各类连接 | 260 |
| 连接参考：ODBC/OLE DB/直连等接口细节 | 278 |
| DataWindow 编程指南：概念与用法 | 232 |
| DataWindow 参考：表达式/对象属性/方法/常量 | 1052 |
| 部署到 .NET | 312 |
| 扩展参考：扩展对象/PB 扩展 | 350 |
| 入门指南：工作区/应用/对象/调试 | 276 |
| 原生接口编程指南与参考 | 274 |
| 新特性 | 38 |
| 对象与控件：Window/控件/菜单/属性与事件 | 608 |
| PowerScript 参考：语言/语句/事件/函数 | 1236 |
| 用户指南 | 1060 |

## 检索工作流

1. **全文检索定位（主路径）**。从用户问题里提取英文关键词（函数名、属性名、语法关键字），
   用 `search_db.py` 毫秒级定位命中页：
   ```bash
   python scripts/search_db.py Modify
   python scripts/search_db.py "SetTransObject AND Retrieve" 20
   ```
   命中输出「文件名 + 页码 + 片段」。多词默认 AND，可用 OR 扩查，短语加引号。
   Windows 下用 `PYTHONIOENCODING=utf-8`。

2. **一次取回完整上下文**。检索时加 `--pages N`，让 `search_db.py` 在打印命中片段的同时，
   把前 N 个命中的完整页文本一起输出（函数签名、代码示例常跨页互补），通常这一步就够作答：
   ```bash
   python scripts/search_db.py "SetTransObject" 3 --pages 1
   ```
   若还需要命中页相邻的更多页，再单独用 `get_pages.py`：
   ```bash
   python scripts/get_pages.py 08_datawindow_reference 760 765
   ```

3. **按主题归属（辅助）**。若不知道查什么关键词、或想按主题浏览，用「文档清单」了解各主题
   范围，再结合检索精确定位。检索命中会直接给出文件名和页码。

4. **自然作答**。基于提取的原文内容回答，但不要照抄文档措辞，也不要罗列引用。回答要像一位
   资深 PowerBuilder 开发者面对面解答：直接用、不机械、不学术腔。**最终回答不得出现任何
   文件名、文档名、页码或"出处：xx"这类来源标识**——检索脚本内部会用到文件名，但那是工作流
   内部细节，不要泄漏给用户。也不要在正文中反复强调版本号（例如不要每句都带上
   "PowerBuilder 里"）。版本号仅在用户明确询问版本特性/差异时才提及。若提取内容不足以
   回答，扩大关键词或页码范围重试。

## 为什么查询而不是外推

PowerBuilder 的函数签名、属性名、枚举值、语法细节极多，且与主流语言不同（如
`dw_1.Modify()`、`GetItemStatus()`、`PowerString` 等）。凭印象容易给错参数或记错属性名。
索引是权威来源，按"搜索索引 → 取完整页"两步走，多数问题毫秒级可锁定位。

## 附注

- `pb_docs.db` 是预构建的（从官方文档 提取全文后用 SQLite FTS5 建索引），已随技能交付，
  可直接使用，也可整体复制到其他机器。
- 索引存的是文本正文，丢失少量表格对齐和图片，但正文、代码、签名完整可读。
- 查询依赖：仅 Python 内置 `sqlite3`（含 FTS5），无第三方包。