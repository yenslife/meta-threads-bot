# Meta Threads Bot

Threads 網軍機器人，使用 OpenAI Agent SDK 和網路爬蟲打造

## Feature

- ✅ 登入 Threads 並取得必要 cookie（csrftoken、sessionid 等）
- ✅ 發文到 Threads（文字貼文）
- ✅ 支援多 Agent 架構（Copywriting Agent、Posting Agent）
- ✅ 使用 OpenAI Agents SDK 協作處理貼文流程
- ✅ 基於 `uv` 進行模組安裝與執行管理

## Setup

複製 `.env.example` 並填入你的 API Key，預設只需要填入 `OPENAI_API_KEY`

```bash
cp .env.example .env
```

安裝模組

```bash
uv run pip install -e .
```

## Run example

使用互動式 CLI 與 Master Agent 對話，進行文案產生與發文操作：

```bash
uv run src/meta_threads_bot/example2.py
```

## Development

請使用 Python 3.12，建議使用 uv 建立虛擬環境：

```bash
uv venv
uv run python --version
```

安裝開發工具與 pre-commit：

```bash
uv run pip install pre-commit
uv run pre-commit install
```

提交前請先執行 pre-commit

```bash
uv run pre-commit run --all
```

## TODO

目前只有實作登入 Threads 和發文到 Threads 的功能
將來預計加入回覆留言、自動瀏覽貼文等功能

- [ ] 回覆留言 API
- [ ] 自動瀏覽貼文 API (selenium)

