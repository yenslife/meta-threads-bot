# Meta Threads Bot

Threads 網軍機器人，使用 OpenAI Agent SDK 和網路爬蟲打造

## Feature

- ✅ 登入 Threads 並取得必要 cookie（csrftoken、sessionid 等）
- ✅ 發文到 Threads（文字貼文）
- ✅ 支援多 Agent 架構（Copywriting Agent、Posting Agent）
- ✅ 使用 OpenAI Agents SDK 協作處理貼文流程
- ✅ 基於 `uv` 進行模組安裝與執行管理

## Setup

複製 `.env.example` 並填入你的 API Key，並且根據需要填入 `OPENAI_API_KEY`、`GEMINI_BASE_URL`、`GEMINI_API_KEY`。如果不想要用 Gemini 可以在 `setup_agents.py` 中註解掉 Gemini 相關的設定

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

效果如下，使用 `gemini-2.0-flash-001` 模型

<details>
<summary>互動過程</summary>

```bash
$ uv run src/meta_threads_bot/example2.py
Enter your message: hi
Master Agent: 哈囉！有什麼我可以幫忙的嗎？你想發起什麼樣的 Threads 網軍行動呢？

Enter your message: 幫我發一些打招呼的文
Master Agent: 沒問題！你想發什麼樣的打招呼文呢？讓我轉給 Copywriting Agent 幫你寫一些，你覺得怎麼樣？

Enter your message: 好
Master Agent: 好的，請稍等，我這就轉給 Copywriting Agent 幫你準備文案。

Master Agent: Skipping item: HandoffCallItem
Handed off from Master Agent to Copywriting Agent
Copywriting Agent: 哈囉！你想發什麼樣的打招呼文呢？ 請告訴我你的想法，我會盡力幫你產生一些有趣的文案。

Enter your message: 期中考加油這類的
Copywriting Agent: 沒問題，我來為你產生一些期中考加油的文案。


Copywriting Agent: Calling a tool
Copywriting Agent: Tool call output: 期中考加油
Copywriting Agent: 我產生了以下文案，你可以參考看看：

*   期中考加油！祝大家都能考出好成績！💪
*   期中考週，一起努力！📚
*   期中考倒數，Fighting！🔥
*   祝大家期中考順利！💯
*   期中考加油！考完一起放鬆！🎉

你覺得這些文案怎麼樣呢？如果需要，我可以再產生更多不同的版本。

Enter your message: 好就這五篇
Copywriting Agent: 好的，請問你想現在就發佈這些文案嗎？

Enter your message: 請直接發佈
Copywriting Agent: 好的，我會將這些文案轉發給 Posting Agent，請稍等。

Copywriting Agent: Skipping item: HandoffCallItem
Handed off from Copywriting Agent to Posting Agent
Posting Agent: 好的，請問你需要我將哪一篇文案發佈到 Threads 呢？

Enter your message: 五篇都要發
Posting Agent: 好的，我會依序將這五篇文案發佈到 Threads。請問你需要登入嗎？如果需要，請提供你的 Threads 帳號密碼。

Enter your message: xxxxxxxx 和 xxxxxxxxxxxxxxx
🌐 正在載入登入頁面...
✅ 找到使用者名稱輸入框
✅ 找到密碼輸入框
✅ 找到登入按鈕 (通過文字內容)
👆 已點擊登入按鈕
⏳ 等待登入處理中...
✅ 登入成功!
🔗 當前網址: https://www.threads.net/
✅ 登入成功!
🍪 已取得必要的 cookies: message, csrftoken, sessionid, ds_user_id
🔒 瀏覽器已關閉
Posting Agent: 請稍等，我先使用你提供的帳號密碼登入 Threads。

Posting Agent: Calling a tool
Posting Agent: Tool call output: {'message': '成功登入，已取得 cookies 資訊，並儲存到 context 中'}
Posting Agent: 好的，Threads 登入成功。我現在將依序發佈以下五篇文案：

1.  期中考加油！祝大家都能考出好成績！💪
2.  期中考週，一起努力！📚
3.  期中考倒數，Fighting！🔥
4.  祝大家期中考順利！💯
5.  期中考加油！考完一起放鬆！🎉

請稍等一下，我會盡快完成發佈。

Posting Agent: Calling a tool
Posting Agent: Calling a tool
Posting Agent: Calling a tool
Posting Agent: Calling a tool
Posting Agent: Calling a tool
Posting Agent: Tool call output: {'message': '貼文已發文成功', 'status': 'ok', 'response_text':
'{"media":{"pk":"3610705554369801225","id":"3610705554369801225_73720191155","fbid":"1809140493757500...'}
Posting Agent: Tool call output: {'message': '貼文已發文成功', 'status': 'ok', 'response_text':
'{"media":{"pk":"3610705577673398625","id":"3610705577673398625_73720191155","fbid":"1805719001293469...'}
Posting Agent: Tool call output: {'message': '貼文已發文成功', 'status': 'ok', 'response_text':
'{"media":{"pk":"3610705597126609122","id":"3610705597126609122_73720191155","fbid":"1788497131225645...'}
Posting Agent: Tool call output: {'message': '貼文已發文成功', 'status': 'ok', 'response_text':
'{"media":{"pk":"3610705615246053909","id":"3610705615246053909_73720191155","fbid":"1792990296291780...'}
Posting Agent: Tool call output: {'message': '貼文已發文成功', 'status': 'ok', 'response_text':
'{"media":{"pk":"3610705635772809412","id":"3610705635772809412_73720191155","fbid":"1797349503571681...'}
Posting Agent: 好的，五篇文案都已經成功發佈到你的 Threads 帳號了。 還有什麼需要我幫忙的嗎？
```

</details>

![alt text](https://i.imgur.com/JQHb1oh.png)

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

## ⚠️ Warning

登入太多次可能會被封鎖，請注意

## TODO

目前只有實作登入 Threads 和發文到 Threads 的功能
將來預計加入回覆留言、自動瀏覽貼文等功能

- [ ] 回覆留言 API
- [ ] 自動瀏覽貼文 API (selenium)

