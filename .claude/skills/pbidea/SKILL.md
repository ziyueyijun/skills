---
name: pbidea
description: >-
  PbIdea 框架 API 查询技能。由 /pbidea 命令手动触发。覆盖：uo_json（JSON 解析/生成/与
  DataWindow 互转）、uo_httpclient / uo_curl（HTTP 客户端、上传下载）、加密与编码
  （uo_crypto/uo_rsa/国密 SM2/SM3/SM4/base64）、数据库（uo_database/uo_recordset）、
  uo_datawindowex、uo_bson、uo_csv、uo_compress、uo_thread 等 WebSuite 组件，以及 sciter、
  web、web_client、haikang、painter 各库中的对象。
disable-model-invocation: true
---

# PbIdea 框架 API 查询

本技能把 PbIdea 框架的全部导出源码（`code/`，566 个 PB 对象：用户对象/数据窗口/窗口/函数/结构）
全文索引进一个 SQLite 数据库 `references/pbidea.db`，用脚本毫秒级检索。**核心原则：不要凭记忆
编造 PbIdea 的 API 细节，凡涉及具体函数签名、属性名、常量值（如 HttpGet=1）、组件是否存在，
一律查索引。** 索引内容直接来自框架源码本身（`.sru` 文件的外函数声明块 `type prototypes`、
中文注释、常量、事件脚本），是最权威、最完整的 API 参考。

## 运行前提（复制即用）

- 只需本技能目录中的 `references/pbidea.db`（已预构建）。
- 查询脚本只用 Python **内置** `sqlite3`（FTS5 trigram 分词器），无需安装任何第三方包；但需要
  **Python 3.11+ 运行时**（其自带 SQLite ≥3.37，支持 trigram）。
- 检查当前机器是否有 Python：`python --version`（Windows 下也可试 `py --version`）。
  **若提示找不到 `python` / `py`**：先安装 Python 3.11+（https://www.python.org/downloads/），
  否则检索脚本无法运行。
- Windows 下运行脚本时统一加 `PYTHONIOENCODING=utf-8`，否则 GBK 控制台打印中文会报编码错误。
- 整个技能目录可整体复制到任何装有 Python 3.11+ 的机器使用，无需联网、无需额外模型。

## 组件地图（先知道有什么，再检索）

PbIdea 是「基于 JSON 与 WebAPI 的 PowerBuilder 接口扩展库」，核心实现编译在
`PbIdea.dll`，PB 侧通过外函数声明调用。`references/pbidea.db` 的 `catalog` 表存了全部 566 个
对象的名称、所属库和一句中文描述；用 `list_objects.py` 可浏览，下表是主要组件速览：

| 类别 | 对象（websuite 库） | 说明 |
|---|---|---|
| JSON | `uo_json` | 核心 JSON 对象：Parse/ToString/Set/Get，级联路径如 `/0/sub/2/dj`（数组下标从 0 起） |
| JSON | `vo_json_datawindow` | DataWindow/DataStore 与 JSON 互导 |
| JSON | `uo_json_s`、`uo_bson`、`uo_csv`、`uo_config` | 标准库函数、可存二进制的 BSON、csv2json、json 格式配置文件 |
| HTTP | `uo_httpclient` + `uo_response` | WinHttp 客户端：`Request(nHttpType,url,...)`，HttpGet=1/HttpPost=2/HttpPut=3…，上传下载、BasicAuth/JWT |
| HTTP | `uo_curl`、`uo_ftp`、`uo_websocket_client`/`uo_websocket_server`、`uo_aliyun` | 基于 curl 库的客户端、FTP、WebSocket、阿里云 |
| 加密编码 | `uo_crypto`、`uo_rsa`、`uo_hmac`、`sm2utils`/`sm3utils`/`sm4utils` | openssl 算法库、RSA 加解密/签名验签、国密 SM2/SM3/SM4 |
| 数据库 | （sql 库）`uo_database`、`uo_database_pool`、`uo_recordset`、`uo_field` | 数据库访问、连接池、结果集 |
| 数据处理 | `uo_datawindowex`、`uo_dbf`、`uo_xlsx`、`uo_xml`、`uo_sqlite3` | DW 增强、DBF/xlsx/XML 读写 |
| 压缩 | `uo_compress`（zlib）、`uo_7z`、`uo_zip` | 压缩解压 |
| 系统工具 | `uo_thread`、`uo_timer`、`uo_process`、`uo_serial`、`uo_string`、`uo_map`/`uo_kv`、`uo_buffer`/`uo_blob`、`uo_biginteger`、`uo_datetime`、`uo_file`、`uo_scintilla` | 线程/定时/进程/串口/字符串/键值对/blob/大整数/日期/文件/语法编辑器 |
| UI | `uo_chart`（painter 库）、`uo_led`、`uo_cover`、`uo_datawindowex` | 图表、LED、遮罩窗口 |
| 其他库 | sciter 库 `uo_sciter*`（HTML UI）、web 库 `uo_datastore`/`uo_html`/`nvo_webreponse_*`、web_client 库 `uo_datawindow_client`、haikang 库 `uo_fingerprint`（指纹仪）/`uo_hcusb`（身份证）、pbjson 库为演示程序 | — |

需要完整清单时运行 `PYTHONIOENCODING=utf-8 python scripts/list_objects.py`（可加 pbl 名、
`--type`、`--name` 过滤）。

## 检索工作流

1. **全文检索定位（主路径）**。从用户问题里提取英文关键词（对象名、函数名、常量名）和中文
   关键词（功能描述），用 `search_db.py` 毫秒级定位命中对象：
   ```bash
   PYTHONIOENCODING=utf-8 python scripts/search_db.py Request
   PYTHONIOENCODING=utf-8 python scripts/search_db.py "uo_json Get"
   PYTHONIOENCODING=utf-8 python scripts/search_db.py 加密 签名
   ```
   多个关键词默认 AND 收窄（引号可有可无）。注意：索引用 trigram 分词器，**不支持 AND/OR 等
   布尔运算符**，需要更宽/更窄搜索时直接换关键词或增减词数。命中输出「库 / 对象名 （类型）+
   命中片段」。

2. **一次取回完整上下文**。检索时加 `--pages N`，让 `search_db.py` 在打印命中片段的同时把前 N
   个命中对象的完整源码一起输出（函数签名、中文注释、常量、事件脚本同在一个文件里互补），
   通常这一步就够作答：
   ```bash
   PYTHONIOENCODING=utf-8 python scripts/search_db.py "uo_httpclient Request" --pages 2
   ```
   若已知对象名、想直接看完整源码，用 `get_object.py`：
   ```bash
   PYTHONIOENCODING=utf-8 python scripts/get_object.py uo_json
   PYTHONIOENCODING=utf-8 python scripts/get_object.py uo_json websuite   # 同名时指定库
   ```

3. **按组件地图定位（辅助）**。若不知道从哪个关键词下手，先看「组件地图」确定对象归属，
   再 `get_object.py` 直接取该对象源码，或 `list_objects.py --name uo_` 浏览同类对象。

4. **自然作答**。基于提取的原文内容回答，但不要照抄代码措辞，也不要罗列引用。回答要像一位
   用 PbIdea 多年的 PowerBuilder 开发者面对面解答：直接给用法、给示例、给调用约定（如
   `uo_json.Get("/0/sub/2/dj", ref ld_dj)` 数组下标从 0 开始）。**最终回答不得出现任何库名、
   对象文件名、脚本命令或"出处"这类来源标识**——检索脚本内部会用到文件名，但那是工作流内部
   细节，不要泄漏给用户。也不要在正文中反复强调版本号（例如不要每句都带上"PbIdea 里"）。
   版本号仅在用户明确询问版本特性/差异时才提及。若提取内容不足以回答，扩大关键词或换对象重试。

## 为什么查询而不是外推

PbIdea 的 API 面极宽（566 个对象，函数签名、常量值、级联路径规则各不相同），且与主流语言
习惯不同（如 JSON 数组下标从 0 起、`system library "PbIdea.dll"` 外函数声明、`uo_response`
响应对象）。凭印象容易给错参数、记错常量或虚构不存在的组件。`pbidea.db` 是权威来源，按
「搜索关键词 → 取完整对象源码」两步走，多数问题毫秒级可锁定。

## 附注

- `pbidea.db` 是预构建的（从 PbIdea 框架的导出源码构建，GBK/UTF-8 自动识别解码），已随技能
  交付，可直接使用。
- 源码更新后可用 `scripts/build_db.py` 一键重建索引：
  ```bash
  PYTHONIOENCODING=utf-8 python scripts/build_db.py --source <PbIdea 源码目录>
  ```
- 索引存的是文本正文，PB 导出文件中的布局坐标、字体等属性完整保留但无实际渲染价值；函数
  签名、注释、事件脚本、常量声明完整可读。
- 查询依赖：仅 Python 内置 `sqlite3`（含 FTS5 trigram），无第三方包。